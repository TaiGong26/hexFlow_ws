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

    left_robot = Node(
        package='hex_flow_ros',
        executable='hex-robot-archer-y6',
        name='robot_left_arm',
        namespace='robot/left',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'host': LaunchConfiguration('host'),
            'port': 8439,
        }],
    )

    right_robot = Node(
        package='hex_flow_ros',
        executable='hex-robot-archer-y6',
        name='robot_right_arm',
        namespace='robot/right',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'host': LaunchConfiguration('host'),
            'port': 9439,
        }],
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

    template_node = Node(
        package='hex_flow_template_ros',
        executable='hex-template-e3-desktop',
        name='template_e3_desktop',
        output='screen',
        emulate_tty=True,
        remappings=[
            ('left_arm_state', '/robot/left/arm_state'),
            ('left_arm_ctrl', '/robot/left/arm_ctrl'),
            ('left_grip_state', '/robot/left/grip_state'),
            ('left_grip_ctrl', '/robot/left/grip_ctrl'),
            ('right_arm_state', '/robot/right/arm_state'),
            ('right_arm_ctrl', '/robot/right/arm_ctrl'),
            ('right_grip_state', '/robot/right/grip_state'),
            ('right_grip_ctrl', '/robot/right/grip_ctrl'),
            ('keys', '/teleop/keyboard'),
        ],
    )

    return LaunchDescription([
        host,
        left_robot,
        right_robot,
        teleop_group,
        template_node,
    ])
