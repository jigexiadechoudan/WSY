import requests
import json
import numpy as np

# 模拟的 MediaPipe landmarks 数据 (33个点)
# 这是一个简单的站立姿势，手臂自然下垂
def create_mock_landmarks(pose_type="neutral"):
    landmarks = []
    
    # 基本点位 (x, y, z, visibility)
    # MediaPipe landmarks range: 0.0 - 1.0
    
    # Head
    for _ in range(11):
        landmarks.append({"x": 0.5, "y": 0.1, "z": 0.0, "visibility": 0.9})
        
    if pose_type == "neutral":
        # Shoulders
        landmarks.append({"x": 0.6, "y": 0.2, "z": 0.0, "visibility": 0.9}) # 11 left
        landmarks.append({"x": 0.4, "y": 0.2, "z": 0.0, "visibility": 0.9}) # 12 right
        
        # Elbows (Straight down)
        landmarks.append({"x": 0.65, "y": 0.35, "z": 0.0, "visibility": 0.9}) # 13 left
        landmarks.append({"x": 0.35, "y": 0.35, "z": 0.0, "visibility": 0.9}) # 14 right
        
        # Wrists (Straight down)
        landmarks.append({"x": 0.7, "y": 0.5, "z": 0.0, "visibility": 0.9}) # 15 left
        landmarks.append({"x": 0.3, "y": 0.5, "z": 0.0, "visibility": 0.9}) # 16 right
        
    elif pose_type == "orchid_hand_perfect":
        # Simulate a perfect "Orchid Hand Left"
        # Target: Left Wrist 160°, Left Elbow 120°, Left Shoulder 80°
        
        # Shoulders (Level)
        landmarks.append({"x": 0.6, "y": 0.2, "z": 0.0, "visibility": 0.9}) # 11 left
        landmarks.append({"x": 0.4, "y": 0.2, "z": 0.0, "visibility": 0.9}) # 12 right
        
        # Left Arm (Simulating angles)
        # Shoulder -> Elbow (Angle ~80 deg from hip vertical)
        landmarks.append({"x": 0.75, "y": 0.25, "z": 0.0, "visibility": 0.9}) # 13 left elbow
        
        # Right Arm (Neutral)
        landmarks.append({"x": 0.35, "y": 0.35, "z": 0.0, "visibility": 0.9}) # 14 right elbow
        
        # Left Wrist (Elbow angle ~120)
        landmarks.append({"x": 0.85, "y": 0.15, "z": 0.0, "visibility": 0.9}) # 15 left wrist
        
        # Right Wrist (Neutral)
        landmarks.append({"x": 0.3, "y": 0.5, "z": 0.0, "visibility": 0.9}) # 16 right wrist

    # Hands (17-22)
    for _ in range(6):
        landmarks.append({"x": 0.0, "y": 0.0, "z": 0.0, "visibility": 0.9})
        
    # Body (23-32)
    # Hips
    landmarks.append({"x": 0.55, "y": 0.5, "z": 0.0, "visibility": 0.9}) # 23 left
    landmarks.append({"x": 0.45, "y": 0.5, "z": 0.0, "visibility": 0.9}) # 24 right
    
    # Legs
    for _ in range(8):
        landmarks.append({"x": 0.5, "y": 0.8, "z": 0.0, "visibility": 0.9})
        
    # Ensure 33 points
    while len(landmarks) < 33:
        landmarks.append({"x": 0.0, "y": 0.0, "z": 0.0, "visibility": 0.9})
        
    return landmarks

def test_api(pose_type="neutral", target_pose="orchid_hand_left"):
    url = "http://localhost:8002/api/v1/vision/analyze-pose"
    
    payload = {
        "landmarks": create_mock_landmarks(pose_type),
        "target_pose": target_pose
    }
    
    try:
        response = requests.post(url, json=payload)
        print(f"\n--- Testing Pose: {pose_type} vs Target: {target_pose} ---")
        print(f"Status Code: {response.status_code}")
        if response.status_code == 200:
            data = response.json()
            print(f"Score: {data['score']}")
            print(f"Feedback: {data['feedback']}")
            print(f"Details: {data['details']}")
        else:
            print(f"Error: {response.text}")
    except Exception as e:
        print(f"Request Failed: {e}")

if __name__ == "__main__":
    # Test 1: Neutral pose vs Orchid Hand (Should be low score)
    test_api("neutral", "orchid_hand_left")
    
    # Test 2: Perfect pose vs Orchid Hand (Should be high score)
    # Note: The mock coordinates are rough approximations, score might not be 100 but should be higher
    test_api("orchid_hand_perfect", "orchid_hand_left")
