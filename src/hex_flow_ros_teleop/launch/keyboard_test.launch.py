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

    kb_node = Node(
        package='hex_flow_ros_teleop',
        executable='hex-teleop-keyboard',
        name='teleop_keyboard',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'clock_source': LaunchConfiguration('clock_source'),
        }],
        remappings=[
            ('keyboard', 'teleop_keyboard/keyboard'),
        ],
    )

    test_node = Node(
        package='hex_flow_ros_teleop',
        executable='hex-teleop-keyboard-test',
        name='teleop_keyboard_test',
        output='screen',
        emulate_tty=True,
        remappings=[
            ('keyboard', 'teleop_keyboard/keyboard'),
        ],
    )
    return LaunchDescription([clock_source, kb_node, test_node])
