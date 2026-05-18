from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    device_path = DeclareLaunchArgument(
        'device_path',
        default_value='',
        description='Device path (empty=auto-detect).',
    )

    xbox_view_joy = DeclareLaunchArgument(
        'xbox_view_joy',
        default_value='false',
        description='Enable debug output.',
    )

    clock_source = DeclareLaunchArgument(
        'clock_source',
        default_value='driver_timestamp',
        description='Timestamp source: driver_timestamp (hardware clock) or ros (system clock).',
    )

    joy_node = Node(
        package='hex_flow_ros_teleop',
        executable='hex-teleop-joystick',
        name='teleop_joystick',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'device_path': LaunchConfiguration('device_path'),
            'xbox_view_joy': LaunchConfiguration('xbox_view_joy'),
            'clock_source': LaunchConfiguration('clock_source'),
        }],
        remappings=[
            ('joy', '/teleop_joystick/joy'),
        ],
    )

    return LaunchDescription([
        device_path,
        xbox_view_joy,
        clock_source,
        joy_node,
    ])
