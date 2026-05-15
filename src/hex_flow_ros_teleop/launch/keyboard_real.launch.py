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

    kb_node = Node(
        package='hex_flow_ros_teleop',
        executable='hex-teleop-keyboard',
        name='teleop_keyboard',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'device_path': LaunchConfiguration('device_path'),
        }],
        remappings=[
            ('keyboard', '/teleop_keyboard/keyboard'),
        ],
    )

    return LaunchDescription([
        device_path,
        kb_node,
    ])