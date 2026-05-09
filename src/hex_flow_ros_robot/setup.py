import os
from glob import glob
from setuptools import setup, find_packages

package_name = 'hex_flow_ros_robot'

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
    description='HexFlow ROS2 robot nodes',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'hex-robot-archer-y6 = hex_flow_ros_robot.main_archer_y6:main',
            'hex-robot-firefly-y6 = hex_flow_ros_robot.main_firefly_y6:main',
            'hex-robot-hello-y6 = hex_flow_ros_robot.main_hello_y6:main',
            'hex-robot-archer-y6-test = hex_flow_ros_robot.main_archer_y6_test:main',
            'hex-robot-firefly-y6-test = hex_flow_ros_robot.main_firefly_y6_test:main',
            'hex-robot-hello-y6-test = hex_flow_ros_robot.main_hello_y6_test:main',
        ],
    },
)
