from launch import LaunchDescription
from launch_ros.actions import Node, PushRosNamespace
from launch.actions import GroupAction


def generate_launch_description():
    sim_group = GroupAction([
        PushRosNamespace('sim'),
        Node(
            package='hex_flow_ros',
            executable='hex-mujoco-archer-y6',
            name='mujoco_archer_y6',
            output='screen',
            emulate_tty=True,
            parameters=[{
                'headless': False,
                'state_rate': 500.0,
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
        ),
    ])

    template_node = Node(
        package='hex_flow_template_ros',
        executable='hex-template-archer-y6',
        name='template_archer_y6',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'rate_hz': 500.0,
            'arrive_threshold': 0.06,
        }],
        remappings=[
            ('arm_state', '/sim/arm_state'),
            ('arm_ctrl', '/sim/arm_ctrl'),
            ('grip_state', '/sim/grip_state'),
            ('grip_ctrl', '/sim/grip_ctrl'),
            ('keys', '/teleop/keyboard'),
        ],
    )

    return LaunchDescription([
        sim_group,
        teleop_group,
        template_node,
    ])
