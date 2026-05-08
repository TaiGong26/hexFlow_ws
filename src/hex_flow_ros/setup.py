import os
from glob import glob

from setuptools import setup, find_packages

package_name = 'hex_flow_ros'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name, f'{package_name}.interface', f'{package_name}.node'],
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
         glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='Dong Zhaorui',
    maintainer_email='847235539@qq.com',
    description='HexFlow ROS 2 package',
    license='Apache-2.0',
    tests_require=['pytest'],
    entry_points={
        'console_scripts': [
            # Camera nodes
            'hex-cam-usb = hex_flow_ros.node.node_cam_usb:main',
            'hex-cam-realsense = hex_flow_ros.node.node_cam_realsense:main',
            'hex-cam-berxel = hex_flow_ros.node.node_cam_berxel:main',
            'hex-cam-dummy = hex_flow_ros.node.node_cam_dummy:main',
            # Teleop nodes
            'hex-teleop-keyboard = hex_flow_ros.node.node_teleop_keyboard:main',
            'hex-teleop-joystick = hex_flow_ros.node.node_teleop_joystick:main',
            # Robot nodes
            'hex-robot-archer-y6 = hex_flow_ros.node.node_robot_archer_y6:main',
            'hex-robot-firefly-y6 = hex_flow_ros.node.node_robot_firefly_y6:main',
            'hex-robot-hello-y6 = hex_flow_ros.node.node_robot_hello_y6:main',
            # Mujoco nodes
            'hex-mujoco-archer-y6 = hex_flow_ros.node.node_mujoco_archer_y6:main',
            'hex-mujoco-e3-desktop = hex_flow_ros.node.node_mujoco_e3_desktop:main',
        ],
    },
)
