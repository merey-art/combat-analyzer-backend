def frame_to_timestamp(frame_idx, fps):
    total_sec = int(frame_idx / fps)
    mins = total_sec // 60
    secs = total_sec % 60
    return f"{mins:02}:{secs:02}"