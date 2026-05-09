from launch import LaunchDescription
from launch_ros.actions import Node, PushRosNamespace
from launch.actions import GroupAction, DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    host = DeclareLaunchArgument(
        'host',
        default_value='192.168.1.100',
        description='Robot controller IP address.',
    )

    port = DeclareLaunchArgument(
        'port',
        default_value='8439',
        description='Robot controller port.',
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
            ('arm_state', '/robot/arm_state'),
            ('arm_ctrl', '/robot/arm_ctrl'),
            ('grip_state', '/robot/grip_state'),
            ('grip_ctrl', '/robot/grip_ctrl'),
            ('keys', '/teleop/keyboard'),
        ],
    )

    return LaunchDescription([
        host,
        port,
        robot_group,
        teleop_group,
        template_node,
    ])
