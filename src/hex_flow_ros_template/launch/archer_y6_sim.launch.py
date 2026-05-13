from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    sim_node = Node(
        package='hex_flow_ros_mujoco',
        executable='hex-mujoco-archer-y6',
        name='mujoco_archer_y6',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'headless': False,
            'state_rate': 500.0,
            'camera_type': 'usb',
        }],
        remappings=[
            ('arm_state', '/mujoco_archer_y6/arm_state'),
            ('arm_ctrl', '/mujoco_archer_y6/arm_ctrl'),
            ('grip_state', '/mujoco_archer_y6/grip_state'),
            ('grip_ctrl', '/mujoco_archer_y6/grip_ctrl'),
        ],
    )

    teleop_node = Node(
        package='hex_flow_ros_teleop',
        executable='hex-teleop-keyboard',
        name='teleop_keyboard',
        output='screen',
        emulate_tty=True,
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
            ('arm_state', '/mujoco_archer_y6/arm_state'),
            ('arm_ctrl', '/mujoco_archer_y6/arm_ctrl'),
            ('grip_state', '/mujoco_archer_y6/grip_state'),
            ('grip_ctrl', '/mujoco_archer_y6/grip_ctrl'),
            ('keys', '/teleop_keyboard/keyboard'),
        ],
    )

    return LaunchDescription([
        sim_node,
        teleop_node,
        template_node,
    ])
