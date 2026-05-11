from launch import LaunchDescription
from launch_ros.actions import Node


def generate_launch_description():
    
    host = DeclareLaunchArgument(
        'host',
        default_value='0.0.0.0',
        description='Robot controller IP address.',
    )
    
    
    robot_node = Node(
        package='hex_flow_ros_robot',
        executable='hex-robot-hello-y6',
        name='robot_hello_y6',
        output='screen',
        emulate_tty=True,
        parameters=[{
            'host': LaunchConfiguration('host'),
            'port': 8439,
        }],
        remappings=[
            ('arm_state', 'robot_hello_y6/arm_state'),
            ('grip_joy', 'robot_hello_y6/grip_joy'),
            ('grip_led_ctrl', 'robot_hello_y6/grip_led_ctrl'),
        ],
    )

    test_node = Node(
        package='hex_flow_ros_robot',
        executable='hex-robot-hello-y6-test',
        name='robot_hello_y6_test',
        output='screen',
        emulate_tty=True,
        parameters=[{'rate_hz': 10.0}],
        remappings=[
            ('arm_state', 'robot_hello_y6/arm_state'),
            ('grip_joy', 'robot_hello_y6/grip_joy'),
            ('grip_led_ctrl', 'robot_hello_y6/grip_led_ctrl'),
        ],
    )


    return LaunchDescription([
        host,
        robot_node, 
        test_node
        ])
