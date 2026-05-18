<h1 align="center">HEX FLOW ROS TEMPLATE</h1>

<p align="center">
    <a href="https://github.com/hexfellow/hex_flow_ros_template/stargazers">
        <img src="https://img.shields.io/github/stars/hexfellow/hex_flow_ros_template?style=flat-square&logo=github" />
    </a>
    <a href="https://github.com/hexfellow/hex_flow_ros_template/forks">
        <img src="https://img.shields.io/github/forks/hexfellow/hex_flow_ros_template?style=flat-square&logo=github" />
    </a>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    <a href="https://github.com/hexfellow/hex_flow_ros_template/issues">
        <img src="https://img.shields.io/github/issues/hexfellow/hex_flow_ros_template?style=flat-square&logo=github" />
    </a>
</p>

---

# hex_flow_ros_template

## 概述

`hex_flow_ros_template` 是 HexFlow ROS2 应用模板包，提供 Archer Y6 单臂和 E3 Desktop 双臂两种机械臂应用模板，演示完整的 init/work/exit 控制流程。模板节点实现状态机控制：init 阶段将机械臂移动到稳定位置（位置控制），work 阶段以零力矩补偿模式保持（COMP 模式），exit 阶段回归稳定位姿。按键盘 'q' 退出。

## 依赖安装

### ROS2 依赖
```bash
git clone https://github.com/hexfellow/hex_flow_ros_common.git
git clone https://github.com/hexfellow/hex_flow_ros_msg.git
git clone https://github.com/hexfellow/hex_flow_ros_template.git
```

### pip 安装
```bash
pip install 'numpy>=2.2.6' 'hex_util_runtime>=0.0.0,<0.1.0'
```

## 快速使用

### launch 命令示例
```bash
ros2 launch hex_flow_ros_template archer_y6_sim.launch.py
ros2 launch hex_flow_ros_template e3_desktop_sim.launch.py
```

### 带参数的使用示例
```bash
ros2 launch hex_flow_ros_template archer_y6_real.launch.py host:=192.168.1.100 port:=8439
ros2 launch hex_flow_ros_template e3_desktop_real.launch.py host:=192.168.1.100 port:=8439
```

## 话题接口

### 发布话题（Archer Y6）
| 名称 | 类型 | 描述 | 补充描述 |
|------|------|------|---------|
| `arm_ctrl` | `ArmCtrl` | 臂控制指令 | init/exit 为 POS 模式，work 为 COMP 零力矩 |
| `grip_ctrl` | `GripCtrl` | 夹爪控制指令 | 同上 |

### 订阅话题（Archer Y6）
| 名称 | 类型 | 描述 | 补充描述 |
|------|------|------|---------|
| `arm_state` | `ArmState` | 臂关节状态 | 用于判断是否到达目标位置 |
| `grip_state` | `GripState` | 夹爪状态 | 用于判断是否到达目标位置 |
| `keys` | `sensor_msgs/Joy` | 键盘按键状态 | buttons[16]='q' 时触发退出 |

### 发布话题（E3 Desktop）
| 名称 | 类型 | 描述 | 补充描述 |
|------|------|------|---------|
| `left_arm_ctrl` | `ArmCtrl` | 左臂控制指令 | |
| `right_arm_ctrl` | `ArmCtrl` | 右臂控制指令 | |
| `left_grip_ctrl` | `GripCtrl` | 左夹爪控制指令 | |
| `right_grip_ctrl` | `GripCtrl` | 右夹爪控制指令 | |

### 订阅话题（E3 Desktop）
| 名称 | 类型 | 描述 | 补充描述 |
|------|------|------|---------|
| `left_arm_state` | `ArmState` | 左臂状态 | |
| `right_arm_state` | `ArmState` | 右臂状态 | |
| `left_grip_state` | `GripState` | 左夹爪状态 | |
| `right_grip_state` | `GripState` | 右夹爪状态 | |
| `keys` | `sensor_msgs/Joy` | 键盘按键状态 | buttons[16]='q' 时触发退出 |

### 工作流程状态说明
| 阶段 | 控制模式 | 描述 |
|------|---------|------|
| `init` | POS (ArmCtrlMode=2) | 将臂和夹爪移动到稳定位置 |
| `work` | COMP (ArmCtrlMode=1) | 发送零力矩补偿指令，保持当前位置 |
| `exit` | POS (ArmCtrlMode=2) | 将臂和夹爪归位到稳定位置后退出 |

## 说明

### 节点说明
| 节点 | 可执行文件 | 描述 |
|------|-----------|------|
| Archer Y6 模板 | `hex-template-archer-y6` | Archer Y6 单臂应用模板 |
| E3 Desktop 模板 | `hex-template-e3-desktop` | E3 Desktop 双臂应用模板 |

### Launch 说明
| Launch 文件 | 描述 |
|------------|------|
| `archer_y6_real.launch.py` | Archer Y6 真机模板 |
| `archer_y6_sim.launch.py` | Archer Y6 仿真模板 |
| `e3_desktop_real.launch.py` | E3 Desktop 真机模板 |
| `e3_desktop_sim.launch.py` | E3 Desktop 仿真模板 |

> **注意**：`host` 参数为必填项，用于指定机械臂控制器 IP 地址。

### 节点参数说明
| 参数 | 默认值 | 描述 |
|------|--------|------|
| host | 192.168.1.100 | 机械臂控制器 IP 地址 |
| port | 8439 | 机械臂控制器端口 |
| clock_source | driver_timestamp | 时间戳时钟源：driver_timestamp 或 ros |

### 关键参数说明
| 参数 | 默认值 | 描述 |
|------|--------|------|
| rate_hz | 500.0 | 控制循环频率 |
| arm_stable_pos | [0.0, -1.5, 3.0, 0.07, 0.0, 0.0] | 臂稳定位置（6轴） |
| grip_stable_pos | [0.5] | 夹爪稳定位置 |
| arrive_threshold | 0.06 | 判断到达的误差阈值 |
| clock_source | `"driver_timestamp"` | 时间戳时钟源：`driver_timestamp` 或 `ros` |

### 话题重映射

#### archer_y6_real.launch.py
```python
remappings=[
    ('arm_state', '/robot_archer_y6/arm_state'),
    ('arm_ctrl', '/robot_archer_y6/arm_ctrl'),
    ('grip_state', '/robot_archer_y6/grip_state'),
    ('grip_ctrl', '/robot_archer_y6/grip_ctrl'),
    ('keyboard', '/teleop_keyboard/keyboard'),
],
```

#### archer_y6_sim.launch.py
```python
remappings=[
    ('arm_state', '/mujoco_archer_y6/arm_state'),
    ('arm_ctrl', '/mujoco_archer_y6/arm_ctrl'),
    ('grip_state', '/mujoco_archer_y6/grip_state'),
    ('grip_ctrl', '/mujoco_archer_y6/grip_ctrl'),
    ('keyboard', '/teleop_keyboard/keyboard'),
],
```

#### e3_desktop_real.launch.py
```python
remappings=[
    ('left_arm_state', '/robot_left_arm/arm_state'),
    ('left_arm_ctrl', '/robot_left_arm/arm_ctrl'),
    ('left_grip_state', '/robot_left_arm/grip_state'),
    ('left_grip_ctrl', '/robot_left_arm/grip_ctrl'),
    ('right_arm_state', '/robot_right_arm/arm_state'),
    ('right_arm_ctrl', '/robot_right_arm/arm_ctrl'),
    ('right_grip_state', '/robot_right_arm/grip_state'),
    ('right_grip_ctrl', '/robot_right_arm/grip_ctrl'),
    ('keyboard', '/teleop_keyboard/keyboard'),
],
```

#### e3_desktop_sim.launch.py
```python
remappings=[
    ('left_arm_state', '/mujoco_e3_desktop/left_arm_state'),
    ('left_arm_ctrl', '/mujoco_e3_desktop/left_arm_ctrl'),
    ('left_grip_state', '/mujoco_e3_desktop/left_grip_state'),
    ('left_grip_ctrl', '/mujoco_e3_desktop/left_grip_ctrl'),
    ('right_arm_state', '/mujoco_e3_desktop/right_arm_state'),
    ('right_arm_ctrl', '/mujoco_e3_desktop/right_arm_ctrl'),
    ('right_grip_state', '/mujoco_e3_desktop/right_grip_state'),
    ('right_grip_ctrl', '/mujoco_e3_desktop/right_grip_ctrl'),
    ('keyboard', '/teleop_keyboard/keyboard'),
],
```
