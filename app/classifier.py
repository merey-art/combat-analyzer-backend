def classify_position(landmarks):
    keypoints = {lm.name: [lm.x, lm.y, lm.z] for lm in landmarks.landmark}

    left_hip = keypoints.get("LEFT_HIP")
    right_hip = keypoints.get("RIGHT_HIP")
    left_knee = keypoints.get("LEFT_KNEE")
    right_knee = keypoints.get("RIGHT_KNEE")

    if left_hip and right_hip and left_knee and right_knee:
        hip_avg_y = (left_hip[1] + right_hip[1]) / 2
        knee_avg_y = (left_knee[1] + right_knee[1]) / 2
        if hip_avg_y < knee_avg_y:
            return "Mount/Top"
        else:
            return "Guard/Bottom"
    return "Unknown"