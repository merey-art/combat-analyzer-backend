### app/classifier.py
import torch # type: ignore
import torch.nn as nn # type: ignore
import numpy as np
import json
import os
from app.pose_estimator import detect_pose
from app.classifier import classify_position
from app.utils import frame_to_timestamp
from app.models import SessionLocal, VideoEvent
from app.overlay import draw_pose


# Load label classes
with open("label_classes.json", "r") as f:
    LABELS = json.load(f)

# Define the same model architecture as in training
class PoseClassifier(nn.Module):
    def __init__(self, input_size=99, num_classes=len(LABELS)):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(input_size, 128),
            nn.ReLU(),
            nn.Linear(128, 64),
            nn.ReLU(),
            nn.Linear(64, num_classes)
        )

    def forward(self, x):
        return self.net(x)

# Load the model
model = PoseClassifier()
model.load_state_dict(torch.load("pose_classifier.pt", map_location=torch.device('cpu')))
model.eval()

# Prediction function
def classify_position(landmarks):
    keypoints = []
    for lm in landmarks.landmark:
        keypoints.extend([lm.x, lm.y, lm.z])
    
    if len(keypoints) != 99:
        return "Unknown"

    with torch.no_grad():
        input_tensor = torch.tensor([keypoints], dtype=torch.float32)
        logits = model(input_tensor)
        pred_idx = torch.argmax(logits, dim=1).item()
        return LABELS[pred_idx]