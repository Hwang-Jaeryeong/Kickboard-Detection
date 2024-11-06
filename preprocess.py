import json
import os
import shutil

# Get user-specific paths
json_folder_path = input("Enter the path to the folder containing JSON files: ")
output_folder_path = input("Enter the output folder path for YOLO txt files: ")
jpg_source_folders = input("Enter the paths to the folders with .jpg files (comma-separated): ").split(',')
txt_source_folders = input("Enter the paths to the folders with .txt files (comma-separated): ").split(',')
destination_folder = input("Enter the destination folder path for the merged files: ")
replace_folder_path = input("Enter the folder path to modify labels (for 28 to 0): ")
additional_source_folder = input("Enter the path to an additional source folder to copy to the destination: ")

# Set up default image dimensions
image_width = 1920
image_height = 1080

# Class mapping
class_mapping = {
    '28': 0,  # kickboard (정상 킥보드 사용자)
    '1': 1,   # ped_road (도로 환경 area_code 1)
    '2': 2,   # cross (도로 환경 area_code 2)
    '3': 3    # helmet (안전모)
}

# Create output directory if it doesn't exist
os.makedirs(output_folder_path, exist_ok=True)

# Convert JSON annotations to YOLO format
def convert_to_yolo_format(json_file, output_txt_file):
    with open(json_file, 'r') as f:
        data = json.load(f)

    with open(output_txt_file, 'w') as txt_file:
        annotations = data['annotations']
        for pm in annotations.get('PM', []):
            pm_code = pm['PM_code']
            if pm_code in class_mapping:
                class_id = class_mapping[pm_code]
                x_min, y_min, bbox_width, bbox_height = pm['points']
                x_center = (x_min + bbox_width / 2) / image_width
                y_center = (y_min + bbox_height / 2) / image_height
                width = bbox_width / image_width
                height = bbox_height / image_height
                txt_file.write(f"{class_id} {x_center} {y_center} {width} {height}\n")

        for environment in annotations.get('environment', []):
            area_code = environment['area_code']
            if area_code in class_mapping:
                class_id = class_mapping[area_code]
                points = environment['points']
                x_coords = [p[1] for p in points]
                y_coords = [p[0] for p in points]
                x_min, x_max = min(x_coords), max(x_coords)
                y_min, y_max = min(y_coords), max(y_coords)
                bbox_width = x_max - x_min
                bbox_height = y_max - y_min
                x_center = (x_min + x_max) / 2 / image_width
                y_center = (y_min + y_max) / 2 / image_height
                width = bbox_width / image_width
                height = bbox_height / image_height
                txt_file.write(f"{class_id} {x_center} {y_center} {width} {height}\n")

# Process each JSON file in the folder
for json_file_name in os.listdir(json_folder_path):
    if json_file_name.endswith('.json'):
        json_file_path = os.path.join(json_folder_path, json_file_name)
        output_txt_file_path = os.path.join(output_folder_path, json_file_name.replace('.json', '.txt'))
        convert_to_yolo_format(json_file_path, output_txt_file_path)

print("JSON to YOLO format conversion completed.")

# Function to copy files with a specific extension
def copy_files(source_folders, destination_folder, extension):
    for folder in source_folders:
        for file_name in os.listdir(folder):
            if file_name.endswith(extension):
                source_path = os.path.join(folder, file_name)
                destination_path = os.path.join(destination_folder, file_name)
                shutil.copy(source_path, destination_path)
                print(f"Copied {file_name} to {destination_folder}.")

# Copy .jpg and .txt files to the destination folder
os.makedirs(destination_folder, exist_ok=True)
copy_files(jpg_source_folders, destination_folder, '.jpg')
copy_files(txt_source_folders, destination_folder, '.txt')
print("All .jpg and .txt files have been copied to the destination folder.")

# Remove unmatched .txt files
def remove_unmatched_txt_files(folder_path):
    files = os.listdir(folder_path)
    jpg_files = {os.path.splitext(f)[0] for f in files if f.endswith('.jpg')}
    txt_files = {os.path.splitext(f)[0] for f in files if f.endswith('.txt')}
    unmatched_txt_files = txt_files - jpg_files
    for txt_file in unmatched_txt_files:
        txt_file_path = os.path.join(folder_path, txt_file + '.txt')
        os.remove(txt_file_path)
        print(f"Deleted unmatched txt file: {txt_file}.txt")

remove_unmatched_txt_files(destination_folder)
print("Unmatched txt files have been deleted.")

# Modify .txt files in the specified folder to replace label 28 with 0
def modify_txt_labels(folder_path, old_label, new_label):
    for file_name in os.listdir(folder_path):
        if file_name.endswith('.txt'):
            file_path = os.path.join(folder_path, file_name)
            with open(file_path, 'r') as file:
                lines = file.readlines()
            modified_lines = [line.replace(f"{old_label} ", f"{new_label} ") for line in lines]
            with open(file_path, 'w') as file:
                file.writelines(modified_lines)
            print(f"Updated labels in {file_name} from {old_label} to {new_label}.")

modify_txt_labels(replace_folder_path, '28', '0')
print("Label modification completed.")

# Copy additional files to the destination folder
copy_files([additional_source_folder], destination_folder, '')
print("All files from the additional source folder have been copied to the destination folder.")
