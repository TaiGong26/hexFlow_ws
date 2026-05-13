from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


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

    head_cam = DeclareLaunchArgument(
        'head_cam_type',
        default_value='empty',
        description='Head camera type (empty/usb/realsense/berxel).',
    )

    left_cam = DeclareLaunchArgument(
        'left_cam_type',
        default_value='empty',
        description='Left arm camera type.',
    )

    right_cam = DeclareLaunchArgument(
        'right_cam_type',
        default_value='empty',
        description='Right arm camera type.',
    )

    sim_node = Node(
        package='hex_flow_ros_mujoco',
        executable='hex-mujoco-e3-desktop',
        name='mujoco_e3_desktop',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'headless': LaunchConfiguration('headless'),
            'state_rate': LaunchConfiguration('state_rate'),
            'state_buffer_size': LaunchConfiguration('state_buffer_size'),
            'cam_buffer_size': LaunchConfiguration('cam_buffer_size'),
            'sens_ts': LaunchConfiguration('sens_ts'),
            'head_cam_type': LaunchConfiguration('head_cam_type'),
            'left_cam_type': LaunchConfiguration('left_cam_type'),
            'right_cam_type': LaunchConfiguration('right_cam_type'),
            'cam_rate': 30.0,
        }],
        remappings=[
            ('left_arm_state', '/mujoco_e3_desktop/left_arm_state'),
            ('left_arm_ctrl', '/mujoco_e3_desktop/left_arm_ctrl'),
            ('left_grip_state', '/mujoco_e3_desktop/left_grip_state'),
            ('left_grip_ctrl', '/mujoco_e3_desktop/left_grip_ctrl'),
            ('right_arm_state', '/mujoco_e3_desktop/right_arm_state'),
            ('right_arm_ctrl', '/mujoco_e3_desktop/right_arm_ctrl'),
            ('right_grip_state', '/mujoco_e3_desktop/right_grip_state'),
            ('right_grip_ctrl', '/mujoco_e3_desktop/right_grip_ctrl'),
        ],
    )

    return LaunchDescription([
        headless,
        state_rate,
        state_buffer_size,
        cam_buffer_size,
        sens_ts,
        head_cam,
        left_cam,
        right_cam,
        sim_node,
    ])
