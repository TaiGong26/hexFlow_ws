from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    cam_node = Node(
        package='hex_flow_ros',
        executable='hex-cam-dummy',
        name='cam_dummy',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'frame_rate': 30,
            'height': 480,
            'width': 640,
        }],
        remappings=[
            ('color', 'cam_dummy/color'),
        ],
    )

    test_node = Node(
        package='hex_flow_ros',
        executable='hex-cam-dummy-test',
        name='cam_dummy_test',
        output='screen',
        emulate_tty=True,
        parameters=[{
        'rate_hz': 30.0,
        'cam_buffer_size': 8,
        'sens_ts': False,
        'color_encoding': 'bgr8',
    }],
        remappings=[
            ('color', 'cam_dummy/color'),
        ],
    )

    return LaunchDescription([cam_node, test_node])
