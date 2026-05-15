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

    joy_node = Node(
        package='hex_flow_ros_teleop',
        executable='hex-teleop-joystick',
        name='teleop_joystick',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'clock_source': LaunchConfiguration('clock_source'),
        }],
        remappings=[('joy', 'teleop_joystick/joy')],
    )

    test_node = Node(
        package='hex_flow_ros_teleop',
        executable='hex-teleop-joystick-test',
        name='teleop_joystick_test',
        output='screen',
        emulate_tty=True,
        remappings=[
            ('joy', 'teleop_joystick/joy'),
        ],
    )

    return LaunchDescription([clock_source, joy_node, test_node])
