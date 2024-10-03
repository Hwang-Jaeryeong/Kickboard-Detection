from ultralytics import YOLO
import argparse

# Create an argument parser
parser = argparse.ArgumentParser(description="Model Training Script")

parser.add_argument('--data', type=str, required=True, help='Path to the dataset YAML file')
parser.add_argument('--name', type=str, required=True, help='Name of the experiment')
parser.add_argument('--project', type=str, required=True, help='Project name or directory to save results')
parser.add_argument('--epochs', type=int, required=True, help='Number of epochs to train')
parser.add_argument('--imgsz', type=int, default=640, help='Image size (default = 640)')
parser.add_argument('--batch', type=int, default=16, help='Batch size (default = 16)')
parser.add_argument('--lr', type=float, default=0.01, help='Initial learning rate (default = 0.01)')

# Parse the arguments
args = parser.parse_args()

# Load the YOLO model
model = YOLO('yolov8s.pt')

# Train with given arguments
model.train(
    data=args.data,
    epochs=args.epochs,
    imgsz=args.imgsz,
    batch=args.batch,
    name=args.name,
    project=args.project,
    save_period=1,
    lr0=args.lr
)
