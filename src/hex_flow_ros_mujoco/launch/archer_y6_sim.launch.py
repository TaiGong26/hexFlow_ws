from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
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

    state_buffer_size = DeclareLaunchArgument(
        'state_buffer_size',
        default_value='200',
        description='State buffer size.',
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

    sim_node = Node(
        package='hex_flow_ros_mujoco',
        executable='hex-mujoco-archer-y6',
        name='mujoco_archer_y6',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'headless': LaunchConfiguration('headless'),
            'state_rate': LaunchConfiguration('state_rate'),
            'state_buffer_size': LaunchConfiguration('state_buffer_size'),
            'cam_buffer_size': LaunchConfiguration('cam_buffer_size'),
            'sens_ts': LaunchConfiguration('sens_ts'),
            'cam_rate': 30.0,
            'camera_type': 'usb',
        }],
        remappings=[
            ('arm_state', '/mujoco_archer_y6/arm_state'),
            ('arm_ctrl', '/mujoco_archer_y6/arm_ctrl'),
            ('grip_state', '/mujoco_archer_y6/grip_state'),
            ('grip_ctrl', '/mujoco_archer_y6/grip_ctrl'),
        ],
    )

    teleop_keyboard_node = Node(
        package='hex_flow_ros_teleop',
        executable='hex-teleop-keyboard',
        name='teleop_keyboard',
        output='screen',
        emulate_tty=True,
        condition=IfCondition(LaunchConfiguration('enable_keyboard')),
        remappings=[
            ('keyboard', '/teleop_keyboard/keyboard'),
        ],
    )

    teleop_joystick_node = Node(
        package='hex_flow_ros_teleop',
        executable='hex-teleop-joystick',
        name='teleop_joystick',
        output='screen',
        emulate_tty=True,
        condition=IfCondition(LaunchConfiguration('enable_joystick')),
        remappings=[
            ('joy', '/teleop_joystick/joy'),
        ],
    )

    return LaunchDescription([
        headless,
        state_rate,
        state_buffer_size,
        cam_buffer_size,
        sens_ts,
        sim_node,
        teleop_keyboard_node,
        teleop_joystick_node,
    ])