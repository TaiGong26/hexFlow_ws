from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    kb_node = Node(
        package='hex_flow_ros_teleop',
        executable='hex-teleop-keyboard',
        name='teleop_keyboard',
        output='screen',
        emulate_tty=True,
        remappings=[('keyboard', 'teleop_keyboard/keyboard')],
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
    return LaunchDescription([kb_node, test_node])
