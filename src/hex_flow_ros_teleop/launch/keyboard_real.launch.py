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

    clock_source = DeclareLaunchArgument(
        'clock_source',
        default_value='driver_timestamp',
        description='Timestamp source: driver_timestamp (hardware clock) or ros (system clock).',
    )

    kb_node = Node(
        package='hex_flow_ros_teleop',
        executable='hex-teleop-keyboard',
        name='teleop_keyboard',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'device_path': LaunchConfiguration('device_path'),
            'clock_source': LaunchConfiguration('clock_source'),
        }],
        remappings=[
            ('keyboard', '/teleop_keyboard/keyboard'),
        ],
    )

    return LaunchDescription([
        device_path,
        clock_source,
        kb_node,
    ])