from launch import LaunchDescription
from launch_ros.actions import Node, PushRosNamespace
from launch.actions import DeclareLaunchArgument, GroupAction
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    headless = DeclareLaunchArgument(
        'headless',
        default_value='false',
        description='Run Mujoco without GUI window.',
    )

    head_cam = DeclareLaunchArgument(
        'head_cam_type',
        default_value='empty',
        description='Head camera type (empty/usb/realsense/berxel).',
    )

    left_cam = DeclareLaunchArgument(
        'left_cam_type',
        default_value='empty',
        description='Left arm camera type.',
    )

    right_cam = DeclareLaunchArgument(
        'right_cam_type',
        default_value='empty',
        description='Right arm camera type.',
    )

    sim_group = GroupAction([
        PushRosNamespace('sim'),
        Node(
            package='hex_flow_ros',
            executable='hex-mujoco-e3-desktop',
            name='mujoco_e3_desktop',
            output='screen',
            emulate_tty=True,
            parameters=[{
                'headless': LaunchConfiguration('headless'),
                'head_cam_type': LaunchConfiguration('head_cam_type'),
                'left_cam_type': LaunchConfiguration('left_cam_type'),
                'right_cam_type': LaunchConfiguration('right_cam_type'),
                'state_rate': 1000.0,
                'cam_rate': 30.0,
            }],
            remappings=[
                ('left_arm_state', 'left_arm_state'),
                ('left_arm_ctrl', 'left_arm_ctrl'),
                ('left_grip_state', 'left_grip_state'),
                ('left_grip_ctrl', 'left_grip_ctrl'),
                ('right_arm_state', 'right_arm_state'),
                ('right_arm_ctrl', 'right_arm_ctrl'),
                ('right_grip_state', 'right_grip_state'),
                ('right_grip_ctrl', 'right_grip_ctrl'),
                ('head_color', 'head_color'),
                ('head_depth', 'head_depth'),
                ('left_color', 'left_color'),
                ('left_depth', 'left_depth'),
                ('right_color', 'right_color'),
                ('right_depth', 'right_depth'),
                ('obj_pose', 'obj_pose'),
                ('reset', 'reset'),
            ],
        ),
    ])

    return LaunchDescription([
        headless,
        head_cam,
        left_cam,
        right_cam,
        sim_group,
    ])
