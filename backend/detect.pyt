from ultralytics import YOLO

model = YOLO("yolov8n.pt")   # small network; Ultralytics will auto-download if missing
results = model.predict(source="images/bus.jpg", save=True)  # saves annotated image
print(results)