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

    cam_path = DeclareLaunchArgument(
        'cam_path',
        default_value='/dev/video0',
        description='Camera device path.',
    )

    exposure = DeclareLaunchArgument(
        'exposure',
        default_value='100',
        description='Exposure value.',
    )

    temperature = DeclareLaunchArgument(
        'temperature',
        default_value='4000',
        description='Color temperature (white balance).',
    )

    color_encoding = DeclareLaunchArgument(
        'color_encoding',
        default_value='bgr8',
        description='Color image encoding.',
    )

    clock_source = DeclareLaunchArgument(
        'clock_source',
        default_value='driver_timestamp',
        description='Timestamp source: driver_timestamp (hardware clock) or ros (system clock).',
    )

    cam_node = Node(
        package='hex_flow_ros_camera',
        executable='hex-cam-usb',
        name='cam_usb',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'frame_rate': LaunchConfiguration('frame_rate'),
            'height': LaunchConfiguration('height'),
            'width': LaunchConfiguration('width'),
            'cam_buffer_size': LaunchConfiguration('cam_buffer_size'),
            'sens_ts': LaunchConfiguration('sens_ts'),
            'cam_path': LaunchConfiguration('cam_path'),
            'exposure': LaunchConfiguration('exposure'),
            'temperature': LaunchConfiguration('temperature'),
            'color_encoding': LaunchConfiguration('color_encoding'),
        }],
        remappings=[
            ('color', '/cam_usb/color'),
        ],
    )

    test_node = Node(
        package='hex_flow_ros_camera',
        executable='hex-cam-usb-test',
        name='cam_usb_test',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'rate_hz': 30.0,
            'cam_buffer_size': LaunchConfiguration('cam_buffer_size'),
            'sens_ts': LaunchConfiguration('sens_ts'),
            'color_encoding': LaunchConfiguration('color_encoding'),
            'clock_source': LaunchConfiguration('clock_source'),
        }],
        remappings=[
            ('color', '/cam_usb/color'),
        ],
    )

    return LaunchDescription([
        frame_rate,
        height,
        width,
        cam_buffer_size,
        sens_ts,
        cam_path,
        exposure,
        temperature,
        color_encoding,
        clock_source,
        cam_node,
        test_node,
    ])