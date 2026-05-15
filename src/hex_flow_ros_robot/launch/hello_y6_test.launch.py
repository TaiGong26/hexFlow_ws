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

    clock_source = DeclareLaunchArgument(
        'clock_source',
        default_value='ptp',
        description='Clock source for timestamps: ptp (Hex PTP clock) or ros (rclpy Time).',
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
            'clock_source': LaunchConfiguration('clock_source'),
        }],
        remappings=[
            ('arm_state', 'robot_hello_y6/arm_state'),
            ('grip_joy', 'robot_hello_y6/grip_joy'),
            ('grip_led_ctrl', 'robot_hello_y6/grip_led_ctrl'),
        ],
    )

    test_node = Node(
        package='hex_flow_ros_robot',
        executable='hex-robot-hello-y6-test',
        name='robot_hello_y6_test',
        output='screen',
        emulate_tty=True,
        parameters=[{'rate_hz': 10.0}],
        remappings=[
            ('arm_state', 'robot_hello_y6/arm_state'),
            ('grip_joy', 'robot_hello_y6/grip_joy'),
            ('grip_led_ctrl', 'robot_hello_y6/grip_led_ctrl'),
        ],
    )


    return LaunchDescription([
        host,
        port,
        clock_source,
        robot_node,
        test_node
        ])
