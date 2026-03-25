
class StandardPoseLibrary:
    """
    Library of standard Opera poses (movements/stances) for comparison.
    Each pose defines target angles and acceptable thresholds.
    """
    
    def __init__(self):
        # Dictionary of standard poses
        # Format:
        # 'pose_name': {
        #   'description': "Brief description",
        #   'target_angles': {
        #       'joint_name': (target_angle_degrees, tolerance_degrees)
        #   },
        #   'alignment_checks': {
        #       'check_name': (target_value, tolerance)
        #   }
        # }
        self.POSES = {
            'orchid_hand_left': {
                'name': '兰花指 (左)',
                'description': '左手兰花指，手腕柔和弯曲，食指微微上翘',
                'target_angles': {
                    'left_wrist_angle': (160, 20), # Wrist slightly bent/straight but fluid
                    'left_elbow_angle': (120, 30), # Elbow not fully straight, relaxed
                    'left_shoulder_angle': (80, 20) # Arm lifted but not too high
                },
                'alignment_checks': {
                    'shoulder_slope': (0, 0.1) # Shoulders relatively level
                }
            },
            'cloud_hand_right': {
                'name': '云手 (右)',
                'description': '右手云手起势，手臂圆润划弧',
                'target_angles': {
                    'right_elbow_angle': (100, 20), # Elbow bent significantly for curve
                    'right_shoulder_angle': (90, 20), # Arm out to side
                    'right_wrist_angle': (150, 25)  # Wrist fluid
                },
                'alignment_checks': {}
            },
            'liang_xiang': {
                'name': '亮相 (定格)',
                'description': '英气亮相，双臂张开，气沉丹田',
                'target_angles': {
                    'left_elbow_angle': (160, 20), # Arms extended but not locked
                    'right_elbow_angle': (160, 20),
                    'left_shoulder_angle': (85, 15), # Arms near shoulder height
                    'right_shoulder_angle': (85, 15)
                },
                'alignment_checks': {
                    'shoulder_slope': (0, 0.15) # Shoulders level
                }
            }
        }

    def get_pose(self, pose_name):
        return self.POSES.get(pose_name)

    def list_poses(self):
        return list(self.POSES.keys())

pose_library = StandardPoseLibrary()
