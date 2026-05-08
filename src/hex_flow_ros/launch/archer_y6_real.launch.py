from launch import LaunchDescription
from launch_ros.actions import Node, PushRosNamespace
from launch.actions import DeclareLaunchArgument, GroupAction
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition


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

    enable_keyboard = DeclareLaunchArgument(
        'enable_keyboard',
        default_value='false',
        description='Whether to enable the keyboard teleop node.',
    )

    enable_joystick = DeclareLaunchArgument(
        'enable_joystick',
        default_value='false',
        description='Whether to enable the joystick teleop node.',
    )

    robot_group = GroupAction([
        PushRosNamespace('robot'),
        Node(
            package='hex_flow_ros',
            executable='hex-robot-archer-y6',
            name='robot_archer_y6',
            output='screen',
            emulate_tty=True,
            parameters=[{
                'host': LaunchConfiguration('host'),
                'port': LaunchConfiguration('port'),
                'ctrl_rate': LaunchConfiguration('ctrl_rate'),
            }],
            remappings=[
                ('arm_state', 'arm_state'),
                ('grip_state', 'grip_state'),
                ('arm_ctrl', 'arm_ctrl'),
                ('grip_ctrl', 'grip_ctrl'),
            ],
        ),
    ])

    teleop_group = GroupAction([
        PushRosNamespace('teleop'),
        Node(
            package='hex_flow_ros',
            executable='hex-teleop-keyboard',
            name='teleop_keyboard',
            output='screen',
            emulate_tty=True,
            condition=IfCondition(LaunchConfiguration('enable_keyboard')),
        ),
        Node(
            package='hex_flow_ros',
            executable='hex-teleop-joystick',
            name='teleop_joystick',
            output='screen',
            emulate_tty=True,
            condition=IfCondition(LaunchConfiguration('enable_joystick')),
        ),
    ])

    return LaunchDescription([
        host,
        port,
        ctrl_rate,
        enable_keyboard,
        enable_joystick,
        robot_group,
        teleop_group,
    ])
