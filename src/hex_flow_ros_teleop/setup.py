import os
from glob import glob
from setuptools import setup, find_packages

package_name = 'hex_flow_ros_teleop'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name],
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
        (os.path.join('share', package_name, 'launch'),
         glob('launch/*.launch.py')),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='taigon',
    maintainer_email='thetaigon@qq.com',
    description='HexFlow ROS2 teleoperation nodes',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'hex-teleop-keyboard = hex_flow_ros_teleop.main_keyboard:main',
            'hex-teleop-joystick = hex_flow_ros_teleop.main_joystick:main',
            'hex-teleop-keyboard-test = hex_flow_ros_teleop.main_keyboard_test:main',
            'hex-teleop-joystick-test = hex_flow_ros_teleop.main_joystick_test:main',
        ],
    },
)
