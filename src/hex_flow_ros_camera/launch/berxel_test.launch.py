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
        default_value='400',
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

    serial_number = DeclareLaunchArgument(
        'serial_number',
        description='Camera serial number (empty=auto).',
    )

    exposure = DeclareLaunchArgument(
        'exposure',
        default_value='10000',
        description='Exposure value.',
    )

    gain = DeclareLaunchArgument(
        'gain',
        default_value='100',
        description='Gain value.',
    )

    color_encoding = DeclareLaunchArgument(
        'color_encoding',
        default_value='bgr8',
        description='Color image encoding.',
    )

    depth_encoding = DeclareLaunchArgument(
        'depth_encoding',
        default_value='mono16',
        description='Depth image encoding.',
    )

    cam_node = Node(
        package='hex_flow_ros_camera',
        executable='hex-cam-berxel',
        name='cam_berxel',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'frame_rate': LaunchConfiguration('frame_rate'),
            'height': LaunchConfiguration('height'),
            'width': LaunchConfiguration('width'),
            'cam_buffer_size': LaunchConfiguration('cam_buffer_size'),
            'sens_ts': LaunchConfiguration('sens_ts'),
            'serial_number': LaunchConfiguration('serial_number'),
            'exposure': LaunchConfiguration('exposure'),
            'gain': LaunchConfiguration('gain'),
            'color_encoding': LaunchConfiguration('color_encoding'),
            'depth_encoding': LaunchConfiguration('depth_encoding'),
        }],
        remappings=[
            ('color', '/cam_berxel/color'),
            ('depth', '/cam_berxel/depth'),
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
            'cam_buffer_size': LaunchConfiguration('cam_buffer_size'),
            'sens_ts': LaunchConfiguration('sens_ts'),
            'color_encoding': LaunchConfiguration('color_encoding'),
        }],
        remappings=[
            ('color', '/cam_berxel/color'),
            ('depth', '/cam_berxel/depth'),
        ],
    )

    return LaunchDescription([
        frame_rate,
        height,
        width,
        cam_buffer_size,
        sens_ts,
        serial_number,
        exposure,
        gain,
        color_encoding,
        depth_encoding,
        cam_node,
        test_node,
    ])