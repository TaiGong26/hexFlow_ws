from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():

    sim_node = Node(
        package='hex_flow_ros',
        executable='hex-mujoco-e3-desktop',
        name='mujoco_e3_desktop',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'state_rate': 1000.0,
            'headless': False,
        }],
    )

    test_node = Node(
        package='hex_flow_ros',
        executable='hex-mujoco-e3-desktop-test',
        name='mujoco_e3_desktop_test',
        output='screen',
        emulate_tty=True,
        parameters=[{'rate_hz': 100.0, 'arm_ctrl_mode': 'pos'}],
        remappings=[
            ('left_arm_state', 'mujoco_e3_desktop/left_arm_state'),
            ('left_arm_ctrl', 'mujoco_e3_desktop/left_arm_ctrl'),
            ('right_arm_state', 'mujoco_e3_desktop/right_arm_state'),
            ('right_arm_ctrl', 'mujoco_e3_desktop/right_arm_ctrl'),
        ],
    )

    return LaunchDescription([sim_node, test_node])
