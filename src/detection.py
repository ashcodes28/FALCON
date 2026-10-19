import cv2
import torch
import time
from datetime import datetime, timezone
from ultralytics import YOLO

from biodiversity_engine import (
    Detection,
    AerialSample,
    BiodiversityAuditLedger,
    calculate_faunal_indices,
    CLASS_NAMES,
)

# === CONFIG ===
MODEL_PATH = r'../embed/best.pt'
VIDEO_PATH = r'../embed/test.mp4'
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
CONFIDENCE_THRESHOLD = 0.25
PARCEL_ID = "PARCEL-DEMO-001"

# === INITIALIZE AUDIT LEDGER ===
ledger = BiodiversityAuditLedger(parcel_id=PARCEL_ID, operator_id="FALCON_UAV_PILOT")

# === LOAD MODEL ===
print(f"Using device: {DEVICE}")
model = YOLO(MODEL_PATH).to(DEVICE)
names = model.names if hasattr(model, 'names') else CLASS_NAMES

# === LOAD VIDEO ===
cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    print("Error: Could not open video source.")
    exit()

frame_idx = 0
sample_interval = 30  # Record an audit block every 30 frames (~1 sec at 30 fps)

# === MAIN LOOP ===
while True:
    ret, frame = cap.read()
    if not ret:
        break

    frame_idx += 1
    results = model(frame, device=DEVICE, verbose=False)
    r = results[0]

    current_detections = []
    if r.boxes is not None and r.boxes.conf is not None:
        classes = r.boxes.cls.cpu().numpy()
        confs = r.boxes.conf.cpu().numpy()
        xyxy = r.boxes.xyxy.cpu().numpy()

        valid_indices = []
        for i, (cls_id, conf, box) in enumerate(zip(classes, confs, xyxy)):
            if conf >= CONFIDENCE_THRESHOLD:
                valid_indices.append(i)
                c_name = names.get(int(cls_id), str(int(cls_id)))
                current_detections.append(
                    Detection(
                        class_id=int(cls_id),
                        class_name=c_name,
                        confidence=float(conf),
                        box=tuple(box.tolist()),
                    )
                )

        r.boxes = r.boxes[valid_indices]

    # Periodic audit block generation
    if frame_idx % sample_interval == 0 and current_detections:
        sample = AerialSample(
            sample_id=f"FRAME_{frame_idx:06d}",
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            latitude=40.7128 + (frame_idx * 0.00001),  # Simulated transect drift
            longitude=-74.0060 + (frame_idx * 0.00001),
            altitude_meters=5.0,
            detections=current_detections,
        )
        ledger.record_sample(sample)

    # Render frame with bounding boxes
    annotated_frame = r.plot()

    # Overlay live Ecological HUD
    instant_metrics = calculate_faunal_indices(current_detections)
    hud_lines = [
        f"FALCON Ecological Audit | Parcel: {PARCEL_ID}",
        f"Shannon Diversity (H'): {instant_metrics['shannon_index']:.3f}",
        f"Pollinator-to-Pest Ratio: {instant_metrics['pollinator_to_pest_ratio']:.2f}",
        f"Soil Fauna Score: {instant_metrics['soil_bioturbation_score']:.1f}",
        f"Audit Ledger Blocks: {len(ledger.blocks)} | Valid: {ledger.verify_integrity()}",
    ]

    y_offset = 30
    for line in hud_lines:
        cv2.putText(
            annotated_frame,
            line,
            (15, y_offset),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.6,
            (0, 255, 120),
            2,
            cv2.LINE_AA,
        )
        y_offset += 24

    cv2.imshow("FALCON - Terrestrial Biodiversity Audit", annotated_frame)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# === CLEANUP & AUDIT REPORT EXPORT ===
cap.release()
cv2.destroyAllWindows()

if ledger.blocks:
    cert = ledger.export_certificate()
    with open("audit_certificate.json", "w", encoding="utf-8") as f:
        import json
        json.dump(cert, f, indent=2)
    with open("audit_transect.geojson", "w", encoding="utf-8") as f:
        import json
        json.dump(ledger.export_geojson(), f, indent=2)
    print("\n[FALCON] Exported audit_certificate.json and audit_transect.geojson")
    print(f"[FALCON] Chain integrity: {cert['chain_valid']} | Final Hash: {cert['ledger_final_hash']}")
