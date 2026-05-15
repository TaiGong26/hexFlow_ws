from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    host = DeclareLaunchArgument(
        'host',
        default_value='192.168.1.100',
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
        executable='hex-robot-archer-y6',
        name='robot_archer_y6',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'host': LaunchConfiguration('host'),
            'port': LaunchConfiguration('port'),
            'clock_source': LaunchConfiguration('clock_source'),
        }],
        remappings=[
            ('arm_state', '/robot_archer_y6/arm_state'),
            ('arm_ctrl', '/robot_archer_y6/arm_ctrl'),
            ('grip_state', '/robot_archer_y6/grip_state'),
            ('grip_ctrl', '/robot_archer_y6/grip_ctrl'),
        ],
    )

    teleop_node = Node(
        package='hex_flow_ros_teleop',
        executable='hex-teleop-keyboard',
        name='teleop_keyboard',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'clock_source': LaunchConfiguration('clock_source'),
        }],
        remappings=[
            ('keyboard', '/teleop_keyboard/keyboard'),
        ],
    )

    template_node = Node(
        package='hex_flow_ros_template',
        executable='hex-template-archer-y6',
        name='template_archer_y6',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'rate_hz': 500.0,
            'arrive_threshold': 0.06,
        }],
        remappings=[
            ('arm_state', '/robot_archer_y6/arm_state'),
            ('arm_ctrl', '/robot_archer_y6/arm_ctrl'),
            ('grip_state', '/robot_archer_y6/grip_state'),
            ('grip_ctrl', '/robot_archer_y6/grip_ctrl'),
            ('keys', '/teleop_keyboard/keyboard'),
        ],
    )

    return LaunchDescription([
        host,
        port,
        clock_source,
        robot_node,
        teleop_node,
        template_node,
    ])
