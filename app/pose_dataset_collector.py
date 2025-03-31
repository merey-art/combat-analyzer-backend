import cv2
import mediapipe as mp
import json

LABEL_KEYS = {
    ord('1'): 'Guard',
    ord('2'): 'Mount',
    ord('3'): 'Side Control',
    ord('4'): 'Back Control',
    ord('5'): 'Submission'
}

mp_pose = mp.solutions.pose
pose = mp_pose.Pose()
cap = cv2.VideoCapture("test_videos/example.mp4")

out_file = open("pose_dataset.jsonl", "w")

while cap.isOpened():
    ret, frame = cap.read()
    if not ret:
        break

    rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = pose.process(rgb)

    if results.pose_landmarks:
        landmarks = results.pose_landmarks.landmark
        keypoints = []
        for lm in landmarks:
            keypoints.extend([lm.x, lm.y, lm.z])

        frame_disp = frame.copy()
        cv2.putText(frame_disp, "Press 1-5 to label: 1-Guard, 2-Mount, 3-Side, 4-Back, 5-Sub", (10, 30),
                    cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
        cv2.imshow("Labeling", frame_disp)

        key = cv2.waitKey(0)
        if key == 27:  # ESC to quit
            break
        if key in LABEL_KEYS:
            sample = {
                "label": LABEL_KEYS[key],
                "keypoints": keypoints
            }
            out_file.write(json.dumps(sample) + "\n")

cap.release()
out_file.close()
cv2.destroyAllWindows()
