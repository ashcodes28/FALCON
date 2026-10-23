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
    calculate_green_credits,
    CLASS_NAMES,
)

# === CONFIG ===
MODEL_PATH = r'../embed/best.pt'
VIDEO_PATH = r'../embed/test.mp4'
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
CONFIDENCE_THRESHOLD = 0.25
PARCEL_ID = "PARCEL-DEMO-001"
AREA_HECTARES = 10.0
BASELINE_SCORE = 0.20  # Standard agricultural baseline

# === INITIALIZE AUDIT LEDGER ===
ledger = BiodiversityAuditLedger(
    parcel_id=PARCEL_ID,
    area_hectares=AREA_HECTARES,
    baseline_score=BASELINE_SCORE,
    operator_id="FALCON_UAV_PILOT",
)

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

    # Overlay live Ecological & Green Credit HUD
    instant_faunal = calculate_faunal_indices(current_detections)
    instant_gcu = calculate_green_credits(
        instant_faunal,
        area_hectares=AREA_HECTARES,
        baseline_score=BASELINE_SCORE,
    )

    hud_lines = [
        f"FALCON Green Credit Audit | Parcel: {PARCEL_ID} ({AREA_HECTARES} ha)",
        f"Certified Credits: {instant_gcu['net_green_credits']:.2f} GCU | {instant_gcu['credit_tier'].split(' ')[0]}",
        f"Quality Score (Q): {instant_gcu['ecological_quality_score']:.3f} | Net Uplift: +{instant_gcu['net_uplift']:.3f}",
        f"Shannon Index (H'): {instant_faunal['shannon_index']:.2f} | PPR: {instant_faunal['pollinator_to_pest_ratio']:.2f}",
        f"Audit Blocks: {len(ledger.blocks)} | SHA-256 Ledger: {'VALID' if ledger.verify_integrity() else 'CORRUPT'}",
    ]

    y_offset = 30
    for line in hud_lines:
        cv2.putText(
            annotated_frame,
            line,
            (15, y_offset),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.55,
            (0, 255, 120),
            2,
            cv2.LINE_AA,
        )
        y_offset += 24

    cv2.imshow("FALCON - Terrestrial Biodiversity & Green Credit Audit", annotated_frame)
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

    accounting = cert["green_credit_accounting"]
    print("\n[FALCON] Exported audit_certificate.json and audit_transect.geojson")
    print(f"[FALCON] Certified Green Credits: {accounting['net_green_credit_units_awarded']:.2f} GCU ({accounting['accreditation_tier']})")
    print(f"[FALCON] Chain integrity: {cert['cryptographic_verification']['ledger_chain_valid']} | Final Hash: {cert['cryptographic_verification']['final_block_hash']}")
