from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    host = DeclareLaunchArgument(
        'host',
        default_value='0.0.0.0',
        description='Robot controller IP address.',
    )

    port = DeclareLaunchArgument(
        'port',
        default_value='8439',
        description='Robot controller port.',
    )

    ctrl_rate = DeclareLaunchArgument(
        'ctrl_rate',
        default_value='500.0',
        description='Control loop rate (Hz).',
    )

    state_buffer_size = DeclareLaunchArgument(
        'state_buffer_size',
        default_value='200',
        description='State buffer size.',
    )

    sens_ts = DeclareLaunchArgument(
        'sens_ts',
        default_value='false',
        description='Use device clock for timestamps.',
    )

    led_buffer_size = DeclareLaunchArgument(
        'led_buffer_size',
        default_value='10',
        description='LED command buffer size.',
    )

    robot_node = Node(
        package='hex_flow_ros_robot',
        executable='hex-robot-hello-y6',
        name='robot_hello_y6',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'host': LaunchConfiguration('host'),
            'port': LaunchConfiguration('port'),
            'ctrl_rate': LaunchConfiguration('ctrl_rate'),
            'state_buffer_size': LaunchConfiguration('state_buffer_size'),
            'sens_ts': LaunchConfiguration('sens_ts'),
            'led_buffer_size': LaunchConfiguration('led_buffer_size'),
        }],
        remappings=[
            ('arm_state', '/robot_hello_y6/arm_state'),
            ('grip_joy', '/robot_hello_y6/grip_joy'),
            ('grip_led_ctrl', '/robot_hello_y6/grip_led_ctrl'),
        ],
    )

    return LaunchDescription([
        host,
        port,
        ctrl_rate,
        state_buffer_size,
        sens_ts,
        led_buffer_size,
        robot_node,
    ])