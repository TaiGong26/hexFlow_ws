from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    frame_rate = DeclareLaunchArgument(
        'frame_rate',
        default_value='30',
        description='Camera frame rate (Hz).',
    )

    height = DeclareLaunchArgument(
        'height',
        default_value='480',
        description='Image height (px).',
    )

    width = DeclareLaunchArgument(
        'width',
        default_value='640',
        description='Image width (px).',
    )

    cam_buffer_size = DeclareLaunchArgument(
        'cam_buffer_size',
        default_value='8',
        description='Camera buffer size.',
    )

    sens_ts = DeclareLaunchArgument(
        'sens_ts',
        default_value='false',
        description='Use device clock for timestamps.',
    )

    color_encoding = DeclareLaunchArgument(
        'color_encoding',
        default_value='bgr8',
        description='Color image encoding.',
    )

    cam_node = Node(
        package='hex_flow_ros_camera',
        executable='hex-cam-dummy',
        name='cam_dummy',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'frame_rate': LaunchConfiguration('frame_rate'),
            'height': LaunchConfiguration('height'),
            'width': LaunchConfiguration('width'),
            'cam_buffer_size': LaunchConfiguration('cam_buffer_size'),
            'sens_ts': LaunchConfiguration('sens_ts'),
            'color_encoding': LaunchConfiguration('color_encoding'),
        }],
        remappings=[
            ('color', '/cam_dummy/color'),
        ],
    )

    return LaunchDescription([
        frame_rate,
        height,
        width,
        cam_buffer_size,
        sens_ts,
        color_encoding,
        cam_node,
    ])
