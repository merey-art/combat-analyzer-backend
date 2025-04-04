import cv2
import os
from app.pose_estimator import detect_pose
from app.overlay import draw_pose
from app.classifier import classify_position
from app.utils import frame_to_timestamp
from app.models import SessionLocal, VideoEvent

def process_video(video_path, filename):
    cap = cv2.VideoCapture(video_path)
    width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
    fps = cap.get(cv2.CAP_PROP_FPS)

    output_path = f"static/processed_{os.path.basename(video_path)}"
    out = cv2.VideoWriter(output_path, cv2.VideoWriter_fourcc(*'mp4v'), fps, (width, height))

    db = SessionLocal()
    SKIP_FRAMES = 5
    frame_idx = 0

    while cap.isOpened():
        ret, frame = cap.read()
        if not ret:
            break

        if frame_idx % SKIP_FRAMES != 0:
            frame_idx += 1
            continue

        landmarks = detect_pose(frame)
        if landmarks:
            label = classify_position(landmarks)
            timestamp = frame_to_timestamp(frame_idx, fps)

            event = VideoEvent(filename=filename, frame=frame_idx, position=label, timestamp=timestamp)
            db.add(event)

            frame = draw_pose(frame, landmarks, label, timestamp)

        out.write(frame)
        frame_idx += 1

    cap.release()
    out.release()
    db.commit()
    db.close()

    return output_path
