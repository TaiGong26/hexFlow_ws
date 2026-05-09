from launch import LaunchDescription
from launch_ros.actions import Node, PushRosNamespace
from launch.actions import GroupAction
from launch.conditions import IfCondition
from launch.actions import DeclareLaunchArgument
from launch.substitutions import LaunchConfiguration


def generate_launch_description():

    robot_type = DeclareLaunchArgument(
        'robot_type',
        default_value='archer_y6',
        description='Robot type: archer_y6 or e3_desktop.',
    )

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
            condition=IfCondition(  
                LaunchConfiguration('robot_type')),
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
        robot_type,
        sim_group,
        template_node,
    ])
