from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    robot_node = Node(
        package='hex_flow_ros_robot',
        executable='hex-robot-firefly-y6',
        name='robot_firefly_y6',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'host': '192.168.1.100',
            'port': 8439,
        }],
        remappings=[
            ('arm_state', 'robot_firefly_y6/arm_state'),
            ('grip_state', 'robot_firefly_y6/grip_state'),
            ('arm_ctrl', 'robot_firefly_y6/arm_ctrl'),
            ('grip_ctrl', 'robot_firefly_y6/grip_ctrl'),
        ],
    )

    test_node = Node(
        package='hex_flow_ros_robot',
        executable='hex-robot-firefly-y6-test',
        name='robot_firefly_y6_test',
        output='screen',
        emulate_tty=True,
        parameters=[{'rate_hz': 100.0, 'arm_ctrl_mode': 'pos'}],
        remappings=[
            ('arm_state', 'robot_firefly_y6/arm_state'),
            ('arm_ctrl', 'robot_firefly_y6/arm_ctrl'),
            ('grip_state', 'robot_firefly_y6/grip_state'),
        ],
    )

    return LaunchDescription([robot_node, test_node])
