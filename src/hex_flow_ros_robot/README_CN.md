<h1 align="center">HEX FLOW ROS ROBOT</h1>

<p align="center">
    <a href="https://github.com/hexfellow/hex_flow_ros_robot/stargazers">
        <img src="https://img.shields.io/github/stars/hexfellow/hex_flow_ros_robot?style=flat-square&logo=github" />
    </a>
    <a href="https://github.com/hexfellow/hex_flow_ros_robot/forks">
        <img src="https://img.shields.io/github/forks/hexfellow/hex_flow_ros_robot?style=flat-square&logo=github" />
    </a>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    <a href="https://github.com/hexfellow/hex_flow_ros_robot/issues">
        <img src="https://img.shields.io/github/issues/hexfellow/hex_flow_ros_robot?style=flat-square&logo=github" />
    </a>
</p>

---

# hex_flow_ros_robot

## 概述

`hex_flow_ros_robot` 是 HexFlow ROS2 机械臂节点包，支持 Archer Y6、Firefly Y6、Hello Y6 三种 6-DOF 机械臂，通过 `hex_driver_robot` 的驱动回调连接真实机械臂硬件，发布关节状态（位置/速度/力矩），订阅控制指令（MIT/COMP/POS/POSE 等模式）。

## 依赖安装

### ROS2 依赖
```bash
git clone https://github.com/hexfellow/hex_flow_ros_common.git
git clone https://github.com/hexfellow/hex_flow_ros_msg.git
git clone https://github.com/hexfellow/hex_flow_ros_robot.git
```

### pip 安装
```bash
pip install 'hex_driver_robot>=0.1.0,<0.2.0' 'numpy>=2.2.6' 'hex_util_runtime>=0.0.0,<0.1.0'
```

## 快速使用

### launch 命令示例
```bash
ros2 launch hex_flow_ros_robot archer_y6_real.launch.py host:=192.168.1.100 port:=8439
ros2 launch hex_flow_ros_robot firefly_y6_real.launch.py host:=192.168.1.100 port:=8439
ros2 launch hex_flow_ros_robot hello_y6_real.launch.py host:=192.168.1.100 port:=8439
```

### test 示例
```bash
ros2 launch hex_flow_ros_robot archer_y6_test.launch.py host:=192.168.1.100 port:=8439
ros2 launch hex_flow_ros_robot firefly_y6_test.launch.py host:=192.168.1.100 port:=8439
ros2 launch hex_flow_ros_robot hello_y6_test.launch.py host:=192.168.1.100 port:=8439
```

## 话题接口

### 发布话题
| 名称 | 类型 | 描述 | 补充描述 |
|------|------|------|---------|
| `arm_state` | `ArmState` | 6-DOF 关节状态 | 包含位置/速度/力矩/末端位姿/MIT参数 |
| `grip_state` | `GripState` | 夹爪状态 | Archer/Firefly 使用，GripState 类型 |
| `grip_joy` | `sensor_msgs/Joy` | Hello Y6 夹爪状态 | Hello Y6 特有，Joy 消息格式 |

### 订阅话题
| 名称 | 类型 | 描述 | 补充描述 |
|------|------|------|---------|
| `arm_ctrl` | `ArmCtrl` | 6-DOF 控制指令 | 支持 MIT/COMP/POS/POSE/POS_PLAN/POSE_PLAN 模式 |
| `grip_ctrl` | `GripCtrl` | 夹爪控制指令 | Archer/Firefly 使用，GripCtrl 类型 |
| `grip_led_ctrl` | `std_msgs/Int32MultiArray` | LED 控制指令 | 仅 Hello Y6，Int32MultiArray 格式 |

### 支持的控制模式（ArmCtrl.ctrl_mode）
| 值 | 模式 | 描述 |
|----|------|------|
| 0 | MIT | MIT 阻抗控制 |
| 1 | COMP | 力矩补偿 |
| 2 | POS | 关节位置控制 |
| 3 | POSE | 末端姿态控制 |
| 4 | POS_PLAN | 关节位置规划 |
| 5 | POSE_PLAN | 末端姿态规划 |

## 说明

### 节点说明
| 节点 | 可执行文件 | 描述 |
|------|-----------|------|
| Archer Y6 主节点 | `hex-robot-archer-y6` | Archer Y6 机械臂控制节点 |
| Firefly Y6 主节点 | `hex-robot-firefly-y6` | Firefly Y6 机械臂控制节点 |
| Hello Y6 主节点 | `hex-robot-hello-y6` | Hello Y6 机械臂控制节点（带 LED 夹爪） |
| Archer Y6 测试 | `hex-robot-archer-y6-test` | Archer Y6 测试节点（发布控制指令） |
| Firefly Y6 测试 | `hex-robot-firefly-y6-test` | Firefly Y6 测试节点 |
| Hello Y6 测试 | `hex-robot-hello-y6-test` | Hello Y6 测试节点 |

### Test 节点详情
| 节点 | 订阅话题 | 发布话题 | 功能 | 频率 |
|------|---------|---------|------|------|
| `hex-robot-archer-y6-test` | `arm_state`, `grip_state` | `arm_ctrl` | 以固定关节位置 [0.0, -1.5, 3.0, 0.07, 0.0, 0.0] 发布位置控制指令 | 500Hz |
| `hex-robot-firefly-y6-test` | `arm_state`, `grip_state` | `arm_ctrl` | 以固定关节位置发布位置控制指令，显示关节位置/速度 | 100Hz |
| `hex-robot-hello-y6-test` | `arm_state`, `grip_joy` | `grip_led_ctrl` | 发布 LED 控制指令（红/绿/蓝循环），显示臂状态及按键信息 | 10Hz |

### Launch 说明
| Launch 文件 | 描述 |
|------------|------|
| `archer_y6_real.launch.py` | Archer Y6 真机 |
| `archer_y6_test.launch.py` | Archer Y6 测试 |
| `firefly_y6_real.launch.py` | Firefly Y6 真机 |
| `firefly_y6_test.launch.py` | Firefly Y6 测试 |
| `hello_y6_real.launch.py` | Hello Y6 真机 |
| `hello_y6_test.launch.py` | Hello Y6 测试 |

> **注意**：`host` 参数为必填项，用于指定机械臂控制器 IP 地址。

### 节点参数说明
| 参数 | 默认值 | 描述 |
|------|--------|------|
| host | 0.0.0.0 | 机械臂控制器 IP 地址 |
| port | 8439 | 机械臂控制器端口 |
| ctrl_rate | 500.0 | 控制循环频率（Hz） |
| state_buffer_size | 200 | 状态 buffer 大小 |
| sens_ts | false | 使用设备时钟作为时间戳 |
| grip_type | gp80 | 夹爪类型 |
| led_buffer_size | 10 | LED 命令 buffer 大小（仅 Hello Y6） |
| clock_source | driver_timestamp | 时间戳时钟源：driver_timestamp 或 ros |

### 话题重映射

#### archer_y6_real.launch.py
```python
remappings=[
    ('arm_state', '/robot_archer_y6/arm_state'),
    ('arm_ctrl', '/robot_archer_y6/arm_ctrl'),
    ('grip_state', '/robot_archer_y6/grip_state'),
    ('grip_ctrl', '/robot_archer_y6/grip_ctrl'),
],
```

#### archer_y6_test.launch.py
```python
# robot_archer_y6
remappings=[
    ('arm_state', 'robot_archer_y6/arm_state'),
    ('arm_ctrl', 'robot_archer_y6/arm_ctrl'),
    ('grip_state', 'robot_archer_y6/grip_state'),
    ('grip_ctrl', 'robot_archer_y6/grip_ctrl'),
],
# robot_archer_y6_test
remappings=[
    ('arm_state', 'robot_archer_y6/arm_state'),
    ('arm_ctrl', 'robot_archer_y6/arm_ctrl'),
    ('grip_state', 'robot_archer_y6/grip_state'),
],
```

#### firefly_y6_real.launch.py
```python
remappings=[
    ('arm_state', '/robot_firefly_y6/arm_state'),
    ('arm_ctrl', '/robot_firefly_y6/arm_ctrl'),
    ('grip_state', '/robot_firefly_y6/grip_state'),
    ('grip_ctrl', '/robot_firefly_y6/grip_ctrl'),
],
```

#### firefly_y6_test.launch.py
```python
# robot_firefly_y6
remappings=[
    ('arm_state', 'robot_firefly_y6/arm_state'),
    ('arm_ctrl', 'robot_firefly_y6/arm_ctrl'),
    ('grip_state', 'robot_firefly_y6/grip_state'),
    ('grip_ctrl', 'robot_firefly_y6/grip_ctrl'),
],
# robot_firefly_y6_test
remappings=[
    ('arm_state', 'robot_firefly_y6/arm_state'),
    ('arm_ctrl', 'robot_firefly_y6/arm_ctrl'),
    ('grip_state', 'robot_firefly_y6/grip_state'),
],
```

#### hello_y6_real.launch.py
```python
remappings=[
    ('arm_state', '/robot_hello_y6/arm_state'),
    ('grip_joy', '/robot_hello_y6/grip_joy'),
    ('grip_led_ctrl', '/robot_hello_y6/grip_led_ctrl'),
],
```

#### hello_y6_test.launch.py
```python
# robot_hello_y6
remappings=[
    ('arm_state', 'robot_hello_y6/arm_state'),
    ('grip_joy', 'robot_hello_y6/grip_joy'),
    ('grip_led_ctrl', 'robot_hello_y6/grip_led_ctrl'),
],
# robot_hello_y6_test
remappings=[
    ('arm_state', 'robot_hello_y6/arm_state'),
    ('grip_joy', 'robot_hello_y6/grip_joy'),
    ('grip_led_ctrl', 'robot_hello_y6/grip_led_ctrl'),
],
```