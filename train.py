from ultralytics import YOLO

DATA = input("Path to the dataset YAML file: ")
NAME = input("Name of the experiment: ")
PROJECT = input("Project name or directory to save results: ")
EPOCHS = int(input("Number of epochs to train: "))
IMGSZ = int(input("Image size: "))
BATCH = int(input("Batch size: "))
LR = float(input("Initial learning rate: "))
AUG = input("Augment? (y/n): ")

# Change this to desired version
model = YOLO('yolov8s.pt')

# Train with given arguments
model.train(
    data=DATA,
    epochs=EPOCHS,
    imgsz=IMGSZ,
    batch=BATCH,
    name=NAME,
    project=PROJECT,
    save_period=1,
    lr0=LR,
    augment=AUG
)
