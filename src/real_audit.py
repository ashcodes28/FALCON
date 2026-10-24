from ultralytics import YOLO
from biodiversity_engine import Detection, AerialSample, BiodiversityAuditLedger
from datetime import datetime, timezone

# 1. Load your working YOLO model
model = YOLO('YOLOv11n - Model Weights/best.pt')

# 2. Initialize the cryptographic audit ledger for a real parcel
ledger = BiodiversityAuditLedger(parcel_id="AGRI-PARCEL-KAGGLE-TEST", operator_id="FALCON_UAV_PILOT")

# 3. Run inference on a batch of real images from your Kaggle validation set
# (You can point this to 'data/valid/images' or a subset of it)
results = model.predict(source='data/valid/images/', conf=0.25, stream=True)

all_detections = []
for i, r in enumerate(results):
    current_detections = []
    if r.boxes is not None and r.boxes.conf is not None:
        classes = r.boxes.cls.cpu().numpy()
        confs = r.boxes.conf.cpu().numpy()
        xyxy = r.boxes.xyxy.cpu().numpy()

        for cls_id, conf, box in zip(classes, confs, xyxy):
            c_name = model.names[int(cls_id)]
            current_detections.append(
                Detection(
                    class_id=int(cls_id),
                    class_name=c_name,
                    confidence=float(conf),
                    box=tuple(box.tolist())
                )
            )
    
    # If detections were found in this image, log them as a waypoint sample
    if current_detections:
        sample = AerialSample(
            sample_id=f"KAGGLE_IMG_{i:04d}",
            timestamp_utc=datetime.now(timezone.utc).isoformat(),
            latitude=13.0827 + (i * 0.00001),  # Mock latitude drift for testing
            longitude=80.2707 + (i * 0.00001), # Mock longitude drift
            altitude_meters=5.0,
            detections=current_detections
        )
        ledger.record_sample(sample)

# 4. Export the real audit certificate and GeoJSON map
if ledger.blocks:
    import json
    with open("real_audit_certificate.json", "w", encoding="utf-8") as f:
        json.dump(ledger.export_certificate(), f, indent=2)
    with open("real_audit_transect.geojson", "w", encoding="utf-8") as f:
        json.dump(ledger.export_geojson(), f, indent=2)
    print(f"\n[FALCON] Successfully generated real audit from {len(ledger.blocks)} image waypoints!")
else:
    print("[FALCON] No detections crossed the confidence threshold in the tested images.")