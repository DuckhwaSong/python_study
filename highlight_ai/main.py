from ultralytics import YOLO
import cv2
import torch

# YOLOv8 모델 로드 (여기서는 'yolov8n'을 사용합니다)
model = YOLO('yolov8m.pt')

# GPU 사용 여부 확인
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

# 입력 동영상 및 출력 동영상 경로
input_video_path = 'video_in.mp4'
output_video_path = 'video_out.mp4'

# 동영상 파일 열기
cap = cv2.VideoCapture(input_video_path)

# 동영상 정보 가져오기
fps = cap.get(cv2.CAP_PROP_FPS)
width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # 코덱 설정 (MP4 형식)



# 출력 동영상 파일 설정
out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))

# 프레임별로 객체 감지 수행
while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    # YOLO 모델을 통해 객체 감지 수행
    #results = model.predict(frame)
    # YOLO 모델을 통해 객체 감지 수행 (GPU 사용)
    results = model.predict(frame, device=device)    

    # 감지된 객체를 프레임에 표시
    for result in results[0].boxes:
        # 경계 상자 좌표와 레이블 및 신뢰도 가져오기
        x1, y1, x2, y2 = map(int, result.xyxy[0])  # 경계 상자 좌표
        label = result.cls  # 클래스 라벨 ID
        confidence = result.conf.item()  # 신뢰도를 float로 변환

        # 클래스 라벨 ID를 실제 이름으로 변환
        class_name = model.names[int(label)]

        # 경계 상자와 레이블 텍스트 추가
        cv2.rectangle(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)
        cv2.putText(frame, f"{class_name} {confidence:.2f}", (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

    # 수정된 프레임을 출력 동영상에 저장
    out.write(frame)

# 모든 리소스 해제
cap.release()
out.release()

print(f"Object-detection video saved as {output_video_path}")