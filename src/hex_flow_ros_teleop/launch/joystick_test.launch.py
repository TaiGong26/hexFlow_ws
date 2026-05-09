from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    joy_node = Node(
        package='hex_flow_ros_teleop',
        executable='hex-teleop-joystick',
        name='teleop_joystick',
        output='screen',
        emulate_tty=True,
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

    return LaunchDescription([joy_node, test_node])
