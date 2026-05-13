from launch import LaunchDescription
from launch_ros.actions import Node
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    host = DeclareLaunchArgument(
        'host',
        default_value='192.168.1.100',
        description='Robot controller IP address.',
    )

    left_robot = Node(
        package='hex_flow_ros_robot',
        executable='hex-robot-archer-y6',
        name='robot_left_arm',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'host': LaunchConfiguration('host'),
            'port': 8439,
        }],
        remappings=[
            ('arm_state', '/robot_left_arm/arm_state'),
            ('arm_ctrl', '/robot_left_arm/arm_ctrl'),
            ('grip_state', '/robot_left_arm/grip_state'),
            ('grip_ctrl', '/robot_left_arm/grip_ctrl'),
        ],
    )

    right_robot = Node(
        package='hex_flow_ros_robot',
        executable='hex-robot-archer-y6',
        name='robot_right_arm',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'host': LaunchConfiguration('host'),
            'port': 9439,
        }],
        remappings=[
            ('arm_state', '/robot_right_arm/arm_state'),
            ('arm_ctrl', '/robot_right_arm/arm_ctrl'),
            ('grip_state', '/robot_right_arm/grip_state'),
            ('grip_ctrl', '/robot_right_arm/grip_ctrl'),
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
        executable='hex-template-e3-desktop',
        name='template_e3_desktop',
        output='screen',
        emulate_tty=True,
        remappings=[
            ('left_arm_state', '/robot_left_arm/arm_state'),
            ('left_arm_ctrl', '/robot_left_arm/arm_ctrl'),
            ('left_grip_state', '/robot_left_arm/grip_state'),
            ('left_grip_ctrl', '/robot_left_arm/grip_ctrl'),
            ('right_arm_state', '/robot_right_arm/arm_state'),
            ('right_arm_ctrl', '/robot_right_arm/arm_ctrl'),
            ('right_grip_state', '/robot_right_arm/grip_state'),
            ('right_grip_ctrl', '/robot_right_arm/grip_ctrl'),
            ('keys', '/teleop_keyboard/keyboard'),
        ],
    )

    return LaunchDescription([
        host,
        left_robot,
        right_robot,
        teleop_node,
        template_node,
    ])
