import os
from glob import glob
from setuptools import setup, find_packages

package_name = 'hex_flow_ros_camera'

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
    description='HexFlow ROS2 camera nodes',
    license='Apache-2.0',
    entry_points={
        'console_scripts': [
            'hex-cam-usb = hex_flow_ros_camera.main_usb:main',
            'hex-cam-dummy = hex_flow_ros_camera.main_dummy:main',
            'hex-cam-realsense = hex_flow_ros_camera.main_realsense:main',
            'hex-cam-berxel = hex_flow_ros_camera.main_berxel:main',
            'hex-cam-usb-test = hex_flow_ros_camera.main_usb_test:main',
            'hex-cam-dummy-test = hex_flow_ros_camera.main_dummy_test:main',
            'hex-cam-realsense-test = hex_flow_ros_camera.main_realsense_test:main',
            'hex-cam-berxel-test = hex_flow_ros_camera.main_berxel_test:main',
        ],
    },
)
