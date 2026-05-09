from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    cam_node = Node(
        package='hex_flow_ros',
        executable='hex-cam-usb',
        name='cam_usb',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'frame_rate': 30,
            'height': 480,
            'width': 640,
        }],
        remappings=[
            ('color', 'cam_usb/color'),
        ],
    )

    test_node = Node(
        package='hex_flow_ros',
        executable='hex-cam-usb-test',
        name='cam_usb_test',
        output='screen',
        emulate_tty=True,
        parameters=[{'rate_hz': 30.0}],
        remappings=[
            ('color', 'cam_usb/color'),
        ],
    )

    return LaunchDescription([cam_node, test_node])
