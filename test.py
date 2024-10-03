import cv2
import os
from ultralytics import YOLO

def main():
    file_path = input("Path to the file for inference: ")
    model_path = input("Path to your model: ")
    
    detector = YOLO(model_path)
    
    if not os.path.exists(file_path):
        print(f"Error: The file '{file_path}' does not exist.")
        return
    
    # 확장자명 확인 (이미지/동영상 분류)
    file_extension = os.path.splitext(file_path)[1].lower()
    image_extensions = ['.jpg', '.jpeg']
    video_extensions = ['.mp4', '.mov']

    # 추론
    try:
        results = detector(file_path)
    except Exception as e:
        print(f"Error: Failed to run detector. Details: {e}")
        return

    result = results[0]
    
    # 이미지
    if file_extension in image_extensions:
        img = cv2.imread(file_path)
        if img is None:
            print(f"Error: Unable to load image. Check the file path and try again.")
            return

        # 이미지에 바운딩 박스 그리기
        draw_boxes_and_labels(img, result)
        cv2.imshow("Detected Image", img)
        cv2.waitKey(0)
        cv2.destroyAllWindows()

    # 영상
    elif file_extension in video_extensions:
        cap = cv2.VideoCapture(file_path)

        if not cap.isOpened():
            print(f"Error: Unable to open video file. Check the file path and try again.")
            return

        while cap.isOpened():
            ret, frame = cap.read()
            if not ret:
                break

            # 각 프레임을 대상으로 추론
            results = detector(frame)
            result = results[0]

            draw_boxes_and_labels(frame, result)
            cv2.imshow("Detected Video", frame)
            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        cap.release()
        cv2.destroyAllWindows()

    else:
        print("Error: Unsupported file format. Please provide an image or video file.")
        return


def draw_boxes_and_labels(img, result):
    for box in result.boxes:
        helmet_detected = False

        # 좌표, 확률, 클래스 아이디, 클래스 이름 추출
        x1, y1, x2, y2 = map(int, box.xyxy[0])
        conf = box.conf[0]
        class_id = int(box.cls[0])
        class_name = result.names[class_id]

        if class_name == 'helmet':
            helmet_detected = True
        elif class_name == 'no_helmet':
            helmet_detected = False

        # 헬멧 착용 여부에 따라 색깔 및 레이블 결정
        color = (0, 255, 0) if helmet_detected else (0, 0, 255)
        label = f"{class_name}: {conf:.2f}"

        # 바운딩 박스 그리기
        cv2.rectangle(img, (x1, y1), (x2, y2), color, 2)
        cv2.putText(img, label, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, color, 2)


if __name__ == "__main__":
    main()
