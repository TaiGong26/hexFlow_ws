<h1 align="center">HEX FLOW ROS TELEOP</h1>

<p align="center">
    <a href="https://github.com/hexfellow/hex_flow_ros_teleop/stargazers">
        <img src="https://img.shields.io/github/stars/hexfellow/hex_flow_ros_teleop?style=flat-square&logo=github" />
    </a>
    <a href="https://github.com/hexfellow/hex_flow_ros_teleop/forks">
        <img src="https://img.shields.io/github/forks/hexfellow/hex_flow_ros_teleop?style=flat-square&logo=github" />
    </a>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    <a href="https://github.com/hexfellow/hex_flow_ros_teleop/issues">
        <img src="https://img.shields.io/github/issues/hexfellow/hex_flow_ros_teleop?style=flat-square&logo=github" />
    </a>
</p>

---

# hex_flow_ros_teleop

## 概述

`hex_flow_ros_teleop` 是 HexFlow ROS2 遥操作包，支持游戏手柄（Joystick）和键盘（Keyboard）两种输入设备，用于向机械臂发送控制指令。

## 依赖安装

### ROS2 依赖
```bash
git clone https://github.com/hexfellow/hex_flow_ros_common.git
git clone https://github.com/hexfellow/hex_flow_ros_msg.git
git clone https://github.com/hexfellow/hex_flow_ros_teleop.git
```

### 系统依赖
```bash
sudo apt install python3-evdev
```

### pip 安装
```bash
pip install 'evdev>=1.7.0' 'hex_util_runtime>=0.0.0,<0.1.0'
```

## 快速使用

> **注意：** 如果你需要使用遥操作，那么应该先切换至 XBOX/XINPUT 模式。

### launch 命令示例
```bash
ros2 launch hex_flow_ros_teleop joystick_test.launch.py
ros2 launch hex_flow_ros_teleop keyboard_test.launch.py
```
> 不提供参数时默认会自动获取路径

### 带参数的使用示例
```bash
ros2 launch hex_flow_ros_teleop joystick_test.launch.py device_path:=/dev/input/event3
ros2 launch hex_flow_ros_teleop keyboard_test.launch.py device_path:=/dev/input/event4
```

## 话题接口

### 发布话题
| 名称 | 类型 | 描述 | 补充描述 |
|------|------|------|---------|
| `teleop_joy` | `sensor_msgs/Joy` | 游戏手柄状态 | buttons[10] = 1(按下)/0(松开)，axes[8] 归一化到 [-1,1] |
| `keyboard` | `sensor_msgs/Joy` | 键盘状态 | buttons[26] = 1(按下)/0(松开) 对应 A-Z |

### 游戏手柄按钮映射（teleop_joy.buttons）
| Index | evdev Code | 描述 |
|-------|-----------|------|
| 0 | BTN_X | 按钮 X |
| 1 | BTN_Y | 按钮 Y |
| 2 | BTN_A | 按钮 A |
| 3 | BTN_B | 按钮 B |
| 4 | BTN_TL | 左 bumper |
| 5 | BTN_TR | 右 bumper |
| 6 | BTN_TL2 | 左 trigger |
| 7 | BTN_TR2 | 右 trigger |
| 8 | BTN_THUMBL | 左 thumb |
| 9 | BTN_THUMBR | 右 thumb |

### 游戏手柄轴映射（teleop_joy.axes）
| Index | evdev Code | 描述 |
|-------|-----------|------|
| 0 | ABS_X | 左摇杆 X |
| 1 | ABS_Y | 左摇杆 Y |
| 2 | ABS_RX | 右摇杆 X |
| 3 | ABS_RY | 右摇杆 Y |
| 4 | ABS_Z | 左 trigger |
| 5 | ABS_RZ | 右 trigger |
| 6 | ABS_HAT0X | D-Pad X |
| 7 | ABS_HAT0Y | D-Pad Y |

### 键盘按钮映射（keyboard.buttons）
| Index | Key | Index | Key | Index | Key | Index | Key |
|-------|-----|-------|-----|-------|-----|-------|-----|
| 0 | A | 7 | H | 14 | O | 21 | V |
| 1 | B | 8 | I | 15 | P | 22 | W |
| 2 | C | 9 | J | 16 | Q | 23 | X |
| 3 | D | 10 | K | 17 | R | 24 | Y |
| 4 | E | 11 | L | 18 | S | 25 | Z |
| 5 | F | 12 | M | 19 | T | | |
| 6 | G | 13 | N | 20 | U | | |

## 说明

### 节点说明
| 节点 | 可执行文件 | 描述 |
|------|-----------|------|
| 游戏手柄主节点 | `hex-teleop-joystick` | 游戏手柄遥操作主节点 |
| 键盘主节点 | `hex-teleop-keyboard` | 键盘遥操作主节点 |
| 游戏手柄测试节点 | `hex-teleop-joystick-test` | 游戏手柄状态可视化测试节点 |
| 键盘测试节点 | `hex-teleop-keyboard-test` | 键盘状态可视化测试节点 |

#### Test 节点详情
| 节点 | 订阅话题 | 发布话题 | 功能 | 频率 |
|------|---------|---------|------|------|
| `hex-teleop-joystick-test` | `joy` | 无 | 订阅 joystick 消息，终端显示 buttons 和 axes 实时值 | 10Hz |
| `hex-teleop-keyboard-test` | `keyboard` | 无 | 订阅 keyboard 消息，终端显示当前按下的字母键 | 10Hz |

### Launch 说明
| Launch 文件 | 描述 |
|------------|------|
| `joystick_real.launch.py` | 游戏手柄真机 |
| `joystick_test.launch.py` | 游戏手柄测试 |
| `keyboard_real.launch.py` | 键盘真机 |
| `keyboard_test.launch.py` | 键盘测试 |

### 节点参数说明
| 参数 | 默认值 | 描述 |
|------|--------|------|
| device_path | '' | 设备路径（空==自动检测） |
| xbox_view_joy | false | 启用调试输出 |
| clock_source | driver_timestamp | 时间戳时钟源：driver_timestamp 或 ros |

### 话题重映射

#### joystick_real.launch.py
```python
remappings=[
    ('joy', '/teleop_joystick/joy'),
],
```

#### joystick_test.launch.py
```python
remappings=[
    ('joy', 'teleop_joystick/joy'),
],
```

#### keyboard_real.launch.py
```python
remappings=[
    ('keyboard', '/teleop_keyboard/keyboard'),
],
```

#### keyboard_test.launch.py
```python
# teleop_keyboard
remappings=[
    ('keyboard', 'teleop_keyboard/keyboard'),
],
# teleop_keyboard_test
remappings=[
    ('keyboard', 'teleop_keyboard/keyboard'),
],
```