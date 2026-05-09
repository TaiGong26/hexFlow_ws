from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    cam_node = Node(
        package='hex_flow_ros_camera',
        executable='hex-cam-berxel',
        name='cam_berxel',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'frame_rate': 30,
            'height': 400,
            'width': 640,
        }],
        remappings=[
            ('color', 'cam_berxel/color'),
            ('depth', 'cam_berxel/depth'),
        ],
    )

    test_node = Node(
        package='hex_flow_ros_camera',
        executable='hex-cam-berxel-test',
        name='cam_berxel_test',
        output='screen',
        emulate_tty=True,
        parameters=[{
        'rate_hz': 30.0,
        'cam_buffer_size': 8,
        'sens_ts': False,
        'color_encoding': 'bgr8',
    }],
        remappings=[
            ('color', 'cam_berxel/color'),
            ('depth', 'cam_berxel/depth'),
        ],
    )

    return LaunchDescription([cam_node, test_node])
