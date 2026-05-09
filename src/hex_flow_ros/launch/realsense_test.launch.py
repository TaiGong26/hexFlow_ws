from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    cam_node = Node(
        package='hex_flow_ros',
        executable='hex-cam-realsense',
        name='cam_realsense',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'frame_rate': 30,
            'height': 480,
            'width': 640,
        }],
    )

    test_node = Node(
        package='hex_flow_ros',
        executable='hex-cam-realsense-test',
        name='cam_realsense_test',
        output='screen',
        emulate_tty=True,
        parameters=[{'rate_hz': 30.0}],
        remappings=[
            ('color', 'cam_realsense/color'),
            ('depth', 'cam_realsense/depth'),
        ],
    )

    return LaunchDescription([cam_node, test_node])
