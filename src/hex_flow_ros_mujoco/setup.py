import os
from glob import glob
from setuptools import setup, find_packages

package_name = 'hex_flow_ros_mujoco'

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
    description='HexFlow ROS2 Mujoco simulation nodes',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'hex-mujoco-archer-y6 = hex_flow_ros_mujoco.main_archer_y6:main',
            'hex-mujoco-e3-desktop = hex_flow_ros_mujoco.main_e3_desktop:main',
            'hex-mujoco-archer-y6-test = hex_flow_ros_mujoco.main_archer_y6_test:main',
            'hex-mujoco-e3-desktop-test = hex_flow_ros_mujoco.main_e3_desktop_test:main',
        ],
    },
)
