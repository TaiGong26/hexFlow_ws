from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    clock_source = DeclareLaunchArgument(
        'clock_source',
        default_value='ptp',
        description='Clock source for timestamps: ptp (Hex PTP clock) or ros (rclpy Time).',
    )

    sim_node = Node(
        package='hex_flow_ros_mujoco',
        executable='hex-mujoco-e3-desktop',
        name='mujoco_e3_desktop',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'headless': False,
            'state_rate': 1000.0,
            'clock_source': LaunchConfiguration('clock_source'),
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
        executable='hex-template-e3-desktop',
        name='template_e3_desktop',
        output='screen',
        emulate_tty=True,
        remappings=[
            ('left_arm_state', '/mujoco_e3_desktop/left_arm_state'),
            ('left_arm_ctrl', '/mujoco_e3_desktop/left_arm_ctrl'),
            ('left_grip_state', '/mujoco_e3_desktop/left_grip_state'),
            ('left_grip_ctrl', '/mujoco_e3_desktop/left_grip_ctrl'),
            ('right_arm_state', '/mujoco_e3_desktop/right_arm_state'),
            ('right_arm_ctrl', '/mujoco_e3_desktop/right_arm_ctrl'),
            ('right_grip_state', '/mujoco_e3_desktop/right_grip_state'),
            ('right_grip_ctrl', '/mujoco_e3_desktop/right_grip_ctrl'),
            ('keys', '/teleop_keyboard/keyboard'),
        ],
    )

    return LaunchDescription([clock_source, sim_node, teleop_node, template_node])