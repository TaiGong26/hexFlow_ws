from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    clock_source = DeclareLaunchArgument(
        'clock_source',
        default_value='ptp',
        description='Clock source for timestamps: ptp (Hex PTP clock) or ros (rclpy Time).',
    )

    sim_node = Node(
        package='hex_flow_ros_mujoco',
        executable='hex-mujoco-archer-y6',
        name='mujoco_archer_y6',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'state_rate': 500.0,
            'headless': False,
            'camera_type': 'usb',
            'clock_source': LaunchConfiguration('clock_source'),
        }],
        remappings=[
            ('arm_state', 'mujoco_archer_y6/arm_state'),
            ('grip_state', 'mujoco_archer_y6/grip_state'),
            ('obj_pose', 'mujoco_archer_y6/obj_pose'),
            ('color', 'mujoco_archer_y6/color'),
            ('depth', 'mujoco_archer_y6/depth'),
            ('arm_ctrl', 'mujoco_archer_y6/arm_ctrl'),
            ('grip_ctrl', 'mujoco_archer_y6/grip_ctrl'),
            ('reset', 'mujoco_archer_y6/reset'),
        ],
    )

    test_node = Node(
        package='hex_flow_ros_mujoco',
        executable='hex-mujoco-archer-y6-test',
        name='mujoco_archer_y6_test',
        output='screen',
        emulate_tty=True,
        parameters=[{'rate_hz': 100.0, 'arm_ctrl_mode': 'pos'}],
        remappings=[
            ('arm_state', 'mujoco_archer_y6/arm_state'),
            ('arm_ctrl', 'mujoco_archer_y6/arm_ctrl'),
        ],
    )

    return LaunchDescription([clock_source, sim_node, test_node])
