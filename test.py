from model import detector
import cv2

def main():
    img_path = input("Enter the image path: ")
    
    try:
        results = detector(img_path)
    except Exception as e:
        print(f"Error: Failed to run detector on the image. Details: {e}")
        return 
    
    result = results[0]
    
    img = cv2.imread(img_path) 
    
    if img is None: 
        print(f"Error: Unable to load image. Check the file path and try again.")
        return 
    
    for box in result.boxes:
        helmet_detected = False
        
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        conf = box.conf[0]
        class_id = int(box.cls[0])
        class_name = result.names[class_id]
        
        # adjust this according to actual classes
        if class_name == 'helmet': 
            helmet_detected = True
        
        elif class_name == 'no_helmet':
            helmet_detected = False
            
        color = (0, 255, 0) if helmet_detected else (0, 0, 255)
        label = f"{class_name}: {conf:.2f}"
        
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)
        
    cv2.imshow("Detected Image", img)
    cv2.waitKey(0)
    cv2.destroyAllWindows()
    
if __name__ == "__main__":
    main()