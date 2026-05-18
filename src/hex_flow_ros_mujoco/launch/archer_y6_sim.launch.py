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

    cam_rate = DeclareLaunchArgument(
        'cam_rate',
        default_value='30.0',
        description='Camera publish rate (Hz).',
    )

    camera_type = DeclareLaunchArgument(
        'camera_type',
        default_value='usb',
        description='Camera type (empty/usb/realsense/berxel).',
    )

    clock_source = DeclareLaunchArgument(
        'clock_source',
        default_value='driver_timestamp',
        description='Timestamp source: driver_timestamp (hardware clock) or ros (system clock).',
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
            'cam_rate': LaunchConfiguration('cam_rate'),
            'camera_type': LaunchConfiguration('camera_type'),
            'clock_source': LaunchConfiguration('clock_source'),
        }],
        remappings=[
            ('arm_state', '/mujoco_archer_y6/arm_state'),
            ('arm_ctrl', '/mujoco_archer_y6/arm_ctrl'),
            ('grip_state', '/mujoco_archer_y6/grip_state'),
            ('grip_ctrl', '/mujoco_archer_y6/grip_ctrl'),
        ],
    )


    return LaunchDescription([
        headless,
        state_rate,
        state_buffer_size,
        cam_buffer_size,
        sens_ts,
        cam_rate,
        camera_type,
        clock_source,
        sim_node,
    ])