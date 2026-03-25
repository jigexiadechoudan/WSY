from .pose_analysis_service import pose_extractor
from .standard_pose_library import pose_library
import numpy as np

class PoseComparator:
    """
    Compares user pose features against standard poses.
    Calculates similarity scores and generates feedback.
    """
    
    def __init__(self):
        pass

    def compare_pose(self, user_features, target_pose_name):
        """
        Compare user features with a target pose from the library.
        Returns:
            - score (0-100)
            - feedback (list of strings)
            - details (dict of specific joint scores)
        """
        target_pose = pose_library.get_pose(target_pose_name)
        if not target_pose:
            return 0, ["未找到目标动作"], {}
            
        score_total = 0
        checks_count = 0
        feedback = []
        details = {}
        
        # 1. Check Angles
        if 'target_angles' in target_pose:
            for joint, (target_angle, tolerance) in target_pose['target_angles'].items():
                if joint in user_features:
                    user_angle = user_features[joint]
                    diff = abs(user_angle - target_angle)
                    
                    # Calculate score for this joint
                    # If within tolerance, 100%. If outside, decay.
                    if diff <= tolerance:
                        joint_score = 100
                    else:
                        # Decay: lose 5 points for every degree outside tolerance
                        # But keep minimum score of 0
                        penalty = (diff - tolerance) * 5
                        joint_score = max(0, 100 - penalty)
                    
                    score_total += joint_score
                    checks_count += 1
                    details[joint] = joint_score
                    
                    # Generate specific feedback for low scores
                    if joint_score < 80:
                        joint_name_cn = self._get_joint_name_cn(joint)
                        if user_angle < target_angle:
                            feedback.append(f"{joint_name_cn} 太弯了，请伸直一点")
                        else:
                            feedback.append(f"{joint_name_cn} 太直了，请弯曲一点")

        # 2. Check Alignment (Optional, e.g. shoulder slope)
        if 'alignment_checks' in target_pose:
            for check, (target_val, tolerance) in target_pose['alignment_checks'].items():
                if check in user_features:
                    user_val = user_features[check]
                    diff = abs(user_val - target_val)
                    
                    if diff <= tolerance:
                        check_score = 100
                    else:
                        penalty = (diff - tolerance) * 200 # Higher penalty for small float diffs
                        check_score = max(0, 100 - penalty)
                        
                    score_total += check_score
                    checks_count += 1
                    details[check] = check_score
                    
                    if check_score < 80 and check == 'shoulder_slope':
                        feedback.append("肩膀不平，请保持双肩水平")

        # Final Score
        final_score = 0
        if checks_count > 0:
            final_score = int(score_total / checks_count)
            
        if final_score >= 90:
            feedback.insert(0, "动作非常标准！")
        elif final_score >= 70:
            feedback.insert(0, "动作不错，细节还需微调。")
        else:
            feedback.insert(0, "动作差异较大，请跟随屏幕调整。")
            
        return final_score, feedback, details

    def _get_joint_name_cn(self, joint_key):
        mapping = {
            'left_wrist_angle': '左手腕',
            'right_wrist_angle': '右手腕',
            'left_elbow_angle': '左手肘',
            'right_elbow_angle': '右手肘',
            'left_shoulder_angle': '左肩膀',
            'right_shoulder_angle': '右肩膀'
        }
        return mapping.get(joint_key, joint_key)

pose_comparator = PoseComparator()
