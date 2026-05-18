from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument, OpaqueFunction
from launch.substitutions import LaunchConfiguration

def launch_setup(context):
    """在 OpaqueFunction 内部获取参数，并进行类型强转，确保传给节点的类型绝对正确"""
    
    # 1. 强制转为字符串：解决纯数字序列号变成整型的问题
    serial_number = str(context.launch_configurations['serial_number'])
    
    # 2. 强制转为整型：保证即使传入字符串也能变成数字
    frame_rate = int(context.launch_configurations['frame_rate'])
    height = int(context.launch_configurations['height'])
    width = int(context.launch_configurations['width'])
    cam_buffer_size = int(context.launch_configurations['cam_buffer_size'])
    
    # 3. 强制转为布尔型：处理命令行传入 'true'/'false' 的情况
    sens_ts_raw = context.launch_configurations['sens_ts']
    if isinstance(sens_ts_raw, str):
        sens_ts = sens_ts_raw.lower() in ['true', '1']
    else:
        sens_ts = bool(sens_ts_raw)

    # 4. 正常的字符串参数（无需特殊处理）
    color_encoding = context.launch_configurations['color_encoding']
    depth_encoding = context.launch_configurations['depth_encoding']
    clock_source = context.launch_configurations['clock_source']

    cam_node = Node(
        package='hex_flow_ros_camera',
        executable='hex-cam-realsense',
        name='cam_realsense',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'frame_rate': frame_rate,
            'height': height,
            'width': width,
            'cam_buffer_size': cam_buffer_size,
            'sens_ts': sens_ts,
            'serial_number': serial_number,  # 现在它一定是字符串了
            'color_encoding': color_encoding,
            'depth_encoding': depth_encoding,
        }],
        remappings=[
            ('color', '/cam_realsense/color'),
            ('depth', '/cam_realsense/depth'),
        ],
    )

    test_node = Node(
        package='hex_flow_ros_camera',
        executable='hex-cam-realsense-test',
        name='cam_realsense_test',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'rate_hz': 30.0,
            'cam_buffer_size': cam_buffer_size,
            'sens_ts': sens_ts,
            'color_encoding': color_encoding,
            'clock_source': clock_source,
        }],
        remappings=[
            ('color', '/cam_realsense/color'),
            ('depth', '/cam_realsense/depth'),
        ],
    )

    return [cam_node, test_node]



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

    serial_number = DeclareLaunchArgument(
        'serial_number',
        default_value='',
        description='Camera serial number (empty=auto).',
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

    clock_source = DeclareLaunchArgument(
        'clock_source',
        default_value='driver_timestamp',
        description='Timestamp source: driver_timestamp (hardware clock) or ros (system clock).',
    )

    cam_node = Node(
        package='hex_flow_ros_camera',
        executable='hex-cam-realsense',
        name='cam_realsense',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'frame_rate': LaunchConfiguration('frame_rate'),
            'height': LaunchConfiguration('height'),
            'width': LaunchConfiguration('width'),
            'cam_buffer_size': LaunchConfiguration('cam_buffer_size'),
            'sens_ts': LaunchConfiguration('sens_ts'),
            'serial_number': LaunchConfiguration('serial_number'),
            'color_encoding': LaunchConfiguration('color_encoding'),
            'depth_encoding': LaunchConfiguration('depth_encoding'),
        }],
        remappings=[
            ('color', '/cam_realsense/color'),
            ('depth', '/cam_realsense/depth'),
        ],
    )

    test_node = Node(
        package='hex_flow_ros_camera',
        executable='hex-cam-realsense-test',
        name='cam_realsense_test',
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
            ('color', '/cam_realsense/color'),
            ('depth', '/cam_realsense/depth'),
        ],
    )

    return LaunchDescription([
        frame_rate,
        height,
        width,
        cam_buffer_size,
        sens_ts,
        serial_number,
        color_encoding,
        depth_encoding,
        clock_source,
        cam_node,
        test_node,
    ])