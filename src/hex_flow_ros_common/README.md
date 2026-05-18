<h1 align="center">HEX FLOW ROS COMMON</h1>

<p align="center">
    <a href="https://github.com/hexfellow/hex_flow_ros_common/stargazers">
        <img src="https://img.shields.io/github/stars/hexfellow/hex_flow_ros_common?style=flat-square&logo=github" />
    </a>
    <a href="https://github.com/hexfellow/hex_flow_ros_common/forks">
        <img src="https://img.shields.io/github/forks/hexfellow/hex_flow_ros_common?style=flat-square&logo=github" />
    </a>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    <a href="https://github.com/hexfellow/hex_flow_ros_common/issues">
        <img src="https://img.shields.io/github/issues/hexfellow/hex_flow_ros_common?style=flat-square&logo=github" />
    </a>
</p>

---

# hex_flow_ros_common

## Overview

`hex_flow_ros_common` is the HexFlow ROS2 common interface package, providing a unified ROS communication abstraction layer (InterfaceBase/DataInterface), control mode enums, and conversion functions between ROS messages and driver command dictionaries.

## Dependencies

### ROS2 Dependencies
```bash
git clone https://github.com/hexfellow/hex_flow_ros_msg.git
git clone https://github.com/hexfellow/hex_flow_ros_common.git
```

### pip Installation
```bash
pip install 'numpy>=2.2.6' 'hex_util_runtime>=0.0.0,<0.1.0'
```

## Topic Interfaces

### Module Overview
| Module | Description |
|--------|-------------|
| `hex_flow_ros_common.interface` | InterfaceBase abstract interface and DataInterface rclpy implementation |
| `hex_flow_ros_common.ctrl_mode` | ArmCtrlMode / GripCtrlMode control mode constants |
| `hex_flow_ros_common.msg_convert` | Conversion functions from ROS messages to driver command dictionaries |