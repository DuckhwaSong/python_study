from ultralytics import YOLO
import cv2
import torch
import numpy

print(numpy.__version__)

# YOLOv8 모델 로드 (여기서는 'yolov8n'을 사용합니다)
model = YOLO('yolov8m.pt')

# GPU 사용 여부 확인
device = 'cuda' if torch.cuda.is_available() else 'cpu'
print(f"Using device: {device}")

# 입력 동영상 경로
input_video_path = 'video_in2.mp4'

# 동영상 파일 열기
cap = cv2.VideoCapture(input_video_path)
fps = cap.get(cv2.CAP_PROP_FPS)  # 동영상의 FPS(프레임 속도)
frame_count = 0  # 프레임 번호 추적
total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))   # 총 프레임수
process_percent = 0;    # 진행율

# 프레임별로 객체 감지 수행
while cap.isOpened():
    # 프레임 카운트 증가
    frame_count += 1

    ret, frame = cap.read()
    if not ret: break

    # 프레임 건너뛰기
    if frame_count % 29 != 0: continue
    print(f"frame : {frame_count}")

    # 현재 프레임에 해당하는 시간을 계산 (초 단위)
    frame_time = frame_count / fps
    time_str = f"Time: {frame_time:.2f} sec"
    print(f"Processing frame : {frame_time:.2f} seconds")

    # 진행율 계산&출력
    process_percent = frame_count / total_frames * 100
    print(f"Processing % : {frame_time:.2f} process_percent")

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

    # 프레임을 화면에 표시
    cv2.imshow('YOLOv8 Object Detection', frame)

    # 'q' 키를 누르면 종료
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# 모든 리소스 해제
cap.release()
cv2.destroyAllWindows()
