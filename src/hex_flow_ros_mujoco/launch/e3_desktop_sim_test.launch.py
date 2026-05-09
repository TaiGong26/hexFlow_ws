from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    sim_node = Node(
        package='hex_flow_ros_mujoco',
        executable='hex-mujoco-e3-desktop',
        name='mujoco_e3_desktop',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'state_rate': 1000.0,
            'headless': False,
        }],
        remappings=[
            ('left_arm_state', 'mujoco_e3_desktop/left_arm_state'),
            ('right_arm_state', 'mujoco_e3_desktop/right_arm_state'),
            ('left_grip_state', 'mujoco_e3_desktop/left_grip_state'),
            ('right_grip_state', 'mujoco_e3_desktop/right_grip_state'),
            ('obj_pose', 'mujoco_e3_desktop/obj_pose'),
            ('head_color', 'mujoco_e3_desktop/head_color'),
            ('head_depth', 'mujoco_e3_desktop/head_depth'),
            ('left_color', 'mujoco_e3_desktop/left_color'),
            ('left_depth', 'mujoco_e3_desktop/left_depth'),
            ('right_color', 'mujoco_e3_desktop/right_color'),
            ('right_depth', 'mujoco_e3_desktop/right_depth'),
            ('left_arm_ctrl', 'mujoco_e3_desktop/left_arm_ctrl'),
            ('right_arm_ctrl', 'mujoco_e3_desktop/right_arm_ctrl'),
            ('left_grip_ctrl', 'mujoco_e3_desktop/left_grip_ctrl'),
            ('right_grip_ctrl', 'mujoco_e3_desktop/right_grip_ctrl'),
            ('reset', 'mujoco_e3_desktop/reset'),
        ],
    )

    test_node = Node(
        package='hex_flow_ros_mujoco',
        executable='hex-mujoco-e3-desktop-test',
        name='mujoco_e3_desktop_test',
        output='screen',
        emulate_tty=True,
        parameters=[{'rate_hz': 100.0, 'arm_ctrl_mode': 'pos'}],
        remappings=[
            ('left_arm_state', 'mujoco_e3_desktop/left_arm_state'),
            ('left_arm_ctrl', 'mujoco_e3_desktop/left_arm_ctrl'),
            ('right_arm_state', 'mujoco_e3_desktop/right_arm_state'),
            ('right_arm_ctrl', 'mujoco_e3_desktop/right_arm_ctrl'),
        ],
    )

    return LaunchDescription([sim_node, test_node])
