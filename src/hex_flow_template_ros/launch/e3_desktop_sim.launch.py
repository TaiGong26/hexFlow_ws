from launch import LaunchDescription
from launch_ros.actions import Node, PushRosNamespace
from launch.actions import GroupAction


def generate_launch_description():

    sim_group = GroupAction([
        PushRosNamespace('sim'),
        Node(
            package='hex_flow_ros',
            executable='hex-mujoco-e3-desktop',
            name='mujoco_e3_desktop',
            output='screen',
            emulate_tty=True,
            parameters=[{
                'headless': False,
                'state_rate': 1000.0,
            }],
        ),
    ])

    template_node = Node(
        package='hex_flow_template_ros',
        executable='hex-template-e3-desktop',
        name='template_e3_desktop',
        output='screen',
        emulate_tty=True,
        remappings=[
            ('left_arm_state', '/sim/left_arm_state'),
            ('left_arm_ctrl', '/sim/left_arm_ctrl'),
            ('left_grip_state', '/sim/left_grip_state'),
            ('left_grip_ctrl', '/sim/left_grip_ctrl'),
            ('right_arm_state', '/sim/right_arm_state'),
            ('right_arm_ctrl', '/sim/right_arm_ctrl'),
            ('right_grip_state', '/sim/right_grip_state'),
            ('right_grip_ctrl', '/sim/right_grip_ctrl'),
            ('keys', '/teleop/keyboard'),
        ],
    )

    teleop_group = GroupAction([
        PushRosNamespace('teleop'),
        Node(
            package='hex_flow_ros',
            executable='hex-teleop-keyboard',
            name='teleop_keyboard',
            output='screen',
            emulate_tty=True,
        ),
    ])

    return LaunchDescription([sim_group, teleop_group, template_node])
