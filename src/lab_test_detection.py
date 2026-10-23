import cv2
import torch
from ultralytics import YOLO

from biodiversity_engine import (
    CLASS_NAMES,
    GUILD_POLLINATORS,
    GUILD_BIOCONTROL,
    GUILD_SOIL_DETRITIVORES,
    GUILD_HERBIVORES,
)

# === CONFIG ===
MODEL_PATH = r'../embed/best.pt'
VIDEO_PATH = r'../embed/Lab_Test.mp4'
DEVICE = 'cuda' if torch.cuda.is_available() else 'cpu'
CONFIDENCE_THRESHOLD = 0.25

# Guild isolation mode: 'ALL', 'POLLINATORS', 'BIOCONTROL', 'SOIL_FAUNA', 'HERBIVORES'
ISOLATION_GUILD = 'ALL'

# === LOAD MODEL ===
print(f"Using device: {DEVICE}")
model = YOLO(MODEL_PATH).to(DEVICE)
names = model.names if hasattr(model, 'names') else CLASS_NAMES

# === LOAD VIDEO ===
cap = cv2.VideoCapture(VIDEO_PATH)
if not cap.isOpened():
    print("Error: Could not open video.")
    exit()

while True:
    ret, frame = cap.read()
    if not ret:
        break

    results = model(frame, device=DEVICE, verbose=False)
    r = results[0]

    filtered_indices = []

    if r.boxes is not None and r.boxes.conf is not None:
        classes = r.boxes.cls.cpu().numpy()
        confs = r.boxes.conf.cpu().numpy()

        for i, (cls_id, conf) in enumerate(zip(classes, confs)):
            cls_name = names.get(int(cls_id), str(int(cls_id)))

            if conf < CONFIDENCE_THRESHOLD:
                continue

            # Optional Guild-specific isolation filter
            if ISOLATION_GUILD == 'POLLINATORS' and cls_name not in GUILD_POLLINATORS:
                continue
            elif ISOLATION_GUILD == 'BIOCONTROL' and cls_name not in GUILD_BIOCONTROL:
                continue
            elif ISOLATION_GUILD == 'SOIL_FAUNA' and cls_name not in GUILD_SOIL_DETRITIVORES:
                continue
            elif ISOLATION_GUILD == 'HERBIVORES' and cls_name not in GUILD_HERBIVORES:
                continue

            filtered_indices.append(i)

        r.boxes = r.boxes[filtered_indices]

    annotated_frame = r.plot()
    cv2.putText(
        annotated_frame,
        f"Guild Filter: {ISOLATION_GUILD} | Detections: {len(filtered_indices)}",
        (15, 30),
        cv2.FONT_HERSHEY_SIMPLEX,
        0.7,
        (0, 255, 120),
        2,
        cv2.LINE_AA,
    )
    cv2.imshow("FALCON Guild Isolation Lab Test", annotated_frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()
