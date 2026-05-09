import os
from glob import glob
from setuptools import setup, find_packages

package_name = 'hex_flow_ros_common'

setup(
    name=package_name,
    version='0.0.1',
    packages=[package_name, f'{package_name}.interface'],
    data_files=[
        ('share/ament_index/resource_index/packages',
         ['resource/' + package_name]),
        ('share/' + package_name, ['package.xml']),
    ],
    install_requires=['setuptools'],
    zip_safe=True,
    maintainer='taigon',
    maintainer_email='thetaigon@qq.com',
    description='HexFlow ROS2 common interfaces package',
    license='Apache-2.0',
)
