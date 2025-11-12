#app.py
from ultralytics import YOLO

model = YOLO(r"E:\model train\train\backend\weights\final.pt")
# print(model.info(detailed=True))
print("Classes:", model.names)
print("Number of classes:", len(model.names))
