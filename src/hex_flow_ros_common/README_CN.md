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

## 概述

`hex_flow_ros_common` 是 HexFlow ROS2 公共接口包，提供统一的 ROS 通信抽象层（InterfaceBase/DataInterface）、控制模式枚举、以及 ROS 消息与驱动命令之间的转换函数。

## 依赖安装

### ROS2 依赖
```bash
git clone https://github.com/hexfellow/hex_flow_ros_msg.git
git clone https://github.com/hexfellow/hex_flow_ros_common.git
```

### pip 安装
```bash
pip install 'numpy>=2.2.6' 'hex_util_runtime>=0.0.0,<0.1.0'
```

## 话题接口

### 模块说明
| 模块 | 描述 |
|------|------|
| `hex_flow_ros_common.interface` | InterfaceBase 抽象接口和 DataInterface rclpy 实现 |
| `hex_flow_ros_common.ctrl_mode` | ArmCtrlMode / GripCtrlMode 控制模式常量 |
| `hex_flow_ros_common.msg_convert` | ROS 消息到驱动命令字典的转换函数 |
