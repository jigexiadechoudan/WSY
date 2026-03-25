import numpy as np

class PoseFeatureExtractor:
    """
    Service for extracting features from MediaPipe Pose landmarks.
    Focuses on key angles and relative positions relevant to Opera movements.
    """
    
    def __init__(self):
        # Define key joints mapping based on MediaPipe Pose
        self.JOINTS = {
            'nose': 0,
            'left_shoulder': 11,
            'right_shoulder': 12,
            'left_elbow': 13,
            'right_elbow': 14,
            'left_wrist': 15,
            'right_wrist': 16,
            'left_pinky': 17,
            'right_pinky': 18,
            'left_index': 19,
            'right_index': 20,
            'left_thumb': 21,
            'right_thumb': 22,
            'left_hip': 23,
            'right_hip': 24,
            'left_knee': 25,
            'right_knee': 26,
            'left_ankle': 27,
            'right_ankle': 28
        }

    def _calculate_angle(self, a, b, c):
        """
        Calculate angle between three points (b is the vertex).
        Points are [x, y, z] or [x, y].
        """
        a = np.array(a)
        b = np.array(b)
        c = np.array(c)
        
        # Vectors ba and bc
        ba = a - b
        bc = c - b
        
        # Calculate cosine angle
        cosine_angle = np.dot(ba, bc) / (np.linalg.norm(ba) * np.linalg.norm(bc) + 1e-6)
        angle = np.arccos(np.clip(cosine_angle, -1.0, 1.0))
        
        return np.degrees(angle)

    def extract_features(self, landmarks):
        """
        Extract relevant features from a list of 33 landmarks.
        Input: List of dicts {'x': float, 'y': float, 'z': float, 'visibility': float}
        Output: Dictionary of features (angles, positions)
        """
        if not landmarks or len(landmarks) < 33:
            return None
            
        # Convert to simple list of [x, y] for easier calculation
        # We focus on 2D angles for visual feedback mostly, z can be used for advanced checks
        points = [[l['x'], l['y']] for l in landmarks]
        
        features = {}
        
        # 1. Arm Angles (Elbow Extension)
        # Shoulder - Elbow - Wrist
        features['left_elbow_angle'] = self._calculate_angle(
            points[self.JOINTS['left_shoulder']],
            points[self.JOINTS['left_elbow']],
            points[self.JOINTS['left_wrist']]
        )
        
        features['right_elbow_angle'] = self._calculate_angle(
            points[self.JOINTS['right_shoulder']],
            points[self.JOINTS['right_elbow']],
            points[self.JOINTS['right_wrist']]
        )
        
        # 2. Shoulder Angles (Arm Lift relative to torso)
        # Hip - Shoulder - Elbow
        features['left_shoulder_angle'] = self._calculate_angle(
            points[self.JOINTS['left_hip']],
            points[self.JOINTS['left_shoulder']],
            points[self.JOINTS['left_elbow']]
        )
        
        features['right_shoulder_angle'] = self._calculate_angle(
            points[self.JOINTS['right_hip']],
            points[self.JOINTS['right_shoulder']],
            points[self.JOINTS['right_elbow']]
        )
        
        # 3. Wrist/Hand Orientation (Basic check for "Orchid Hand" or "Palm")
        # Elbow - Wrist - Index
        features['left_wrist_angle'] = self._calculate_angle(
            points[self.JOINTS['left_elbow']],
            points[self.JOINTS['left_wrist']],
            points[self.JOINTS['left_index']]
        )
        
        features['right_wrist_angle'] = self._calculate_angle(
            points[self.JOINTS['right_elbow']],
            points[self.JOINTS['right_wrist']],
            points[self.JOINTS['right_index']]
        )

        # 4. Body Alignment (Shoulder Tilt)
        # Calculate slope between shoulders
        dy = points[self.JOINTS['right_shoulder']][1] - points[self.JOINTS['left_shoulder']][1]
        dx = points[self.JOINTS['right_shoulder']][0] - points[self.JOINTS['left_shoulder']][0]
        features['shoulder_slope'] = dy / (dx + 1e-6) # Avoid division by zero
        
        return features

    def normalize_landmarks(self, landmarks):
        """
        Normalize landmarks to be centered at hip center and scaled by torso size.
        Useful for DTW comparison.
        """
        if not landmarks:
            return []
            
        points = np.array([[l['x'], l['y']] for l in landmarks])
        
        # 1. Center at mid-hip
        left_hip = points[self.JOINTS['left_hip']]
        right_hip = points[self.JOINTS['right_hip']]
        center = (left_hip + right_hip) / 2
        points = points - center
        
        # 2. Scale by torso size (distance between shoulders and hips)
        # Approximate torso height as avg distance from shoulder to hip
        left_torso = np.linalg.norm(points[self.JOINTS['left_shoulder']] - points[self.JOINTS['left_hip']])
        right_torso = np.linalg.norm(points[self.JOINTS['right_shoulder']] - points[self.JOINTS['right_hip']])
        scale = (left_torso + right_torso) / 2
        
        if scale > 0:
            points = points / scale
            
        return points.tolist()

pose_extractor = PoseFeatureExtractor()
