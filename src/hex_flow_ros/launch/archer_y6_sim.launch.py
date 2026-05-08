from launch import LaunchDescription
from launch_ros.actions import Node, PushRosNamespace
from launch.actions import DeclareLaunchArgument, GroupAction
from launch.substitutions import LaunchConfiguration
from launch.conditions import IfCondition


def generate_launch_description():

    headless = DeclareLaunchArgument(
        'headless',
        default_value='false',
        description='Run Mujoco without GUI window.',
    )

    state_rate = DeclareLaunchArgument(
        'state_rate',
        default_value='1000.0',
        description='State publish rate (Hz).',
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

    sim_group = GroupAction([
        PushRosNamespace('sim'),
        Node(
            package='hex_flow_ros',
            executable='hex-mujoco-archer-y6',
            name='mujoco_archer_y6',
            output='screen',
            emulate_tty=True,
            parameters=[{
                'headless': LaunchConfiguration('headless'),
                'state_rate': LaunchConfiguration('state_rate'),
                'cam_rate': 30.0,
                'camera_type': 'usb',
            }],
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
        headless,
        state_rate,
        enable_keyboard,
        enable_joystick,
        sim_group,
        teleop_group,
    ])
