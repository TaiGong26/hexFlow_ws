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

## Overview

`hex_flow_ros_teleop` is the HexFlow ROS2 teleoperation package, supporting both joystick and keyboard input devices for sending control commands to robotic arms.

## Dependencies

### ROS2 Dependencies
```bash
git clone https://github.com/hexfellow/hex_flow_ros_common.git
git clone https://github.com/hexfellow/hex_flow_ros_msg.git
git clone https://github.com/hexfellow/hex_flow_ros_teleop.git
```

### System Dependencies
```bash
sudo apt install python3-evdev
```

### pip Installation
```bash
pip install 'evdev>=1.7.0' 'hex_util_runtime>=0.0.0,<0.1.0'
```

## Quick Start

### Launch Command Examples
```bash
ros2 launch hex_flow_ros_teleop joystick_test.launch.py
ros2 launch hex_flow_ros_teleop keyboard_test.launch.py
```
> When no parameters are provided, the device path is automatically detected by default.

### Usage Examples with Parameters
```bash
ros2 launch hex_flow_ros_teleop joystick_test.launch.py device_path:=/dev/input/event3
ros2 launch hex_flow_ros_teleop keyboard_test.launch.py device_path:=/dev/input/event4
```

## Topic Interfaces

### Published Topics
| Name | Type | Description | Additional Info |
|------|------|-------------|-----------------|
| `teleop_joy` | `sensor_msgs/Joy` | Joystick state | buttons[10] + axes[8] |
| `keyboard` | `sensor_msgs/Joy` | Keyboard state | buttons[26] corresponding to A-Z |

### Joystick Button Mapping (teleop_joy.buttons)
| Index | evdev Code | Description |
|-------|-----------|-------------|
| 0 | BTN_X | Button X |
| 1 | BTN_Y | Button Y |
| 2 | BTN_A | Button A |
| 3 | BTN_B | Button B |
| 4 | BTN_TL | Left bumper |
| 5 | BTN_TR | Right bumper |
| 6 | BTN_TL2 | Left trigger |
| 7 | BTN_TR2 | Right trigger |
| 8 | BTN_THUMBL | Left thumb |
| 9 | BTN_THUMBR | Right thumb |

### Joystick Axis Mapping (teleop_joy.axes)
| Index | evdev Code | Description |
|-------|-----------|-------------|
| 0 | ABS_X | Left stick X |
| 1 | ABS_Y | Left stick Y |
| 2 | ABS_RX | Right stick X |
| 3 | ABS_RY | Right stick Y |
| 4 | ABS_Z | Left trigger |
| 5 | ABS_RZ | Right trigger |
| 6 | ABS_HAT0X | D-Pad X |
| 7 | ABS_HAT0Y | D-Pad Y |

### Keyboard Button Mapping (keyboard.buttons)
| Index | Key | Index | Key | Index | Key | Index | Key |
|-------|-----|-------|-----|-------|-----|-------|-----|
| 0 | A | 7 | H | 14 | O | 21 | V |
| 1 | B | 8 | I | 15 | P | 22 | W |
| 2 | C | 9 | J | 16 | Q | 23 | X |
| 3 | D | 10 | K | 17 | R | 24 | Y |
| 4 | E | 11 | L | 18 | S | 25 | Z |
| 5 | F | 12 | M | 19 | T | | |
| 6 | G | 13 | N | 20 | U | | |

## Notes

### Node Description
| Node | Executable | Description |
|------|------------|-------------|
| Joystick Main Node | `hex-teleop-joystick` | Joystick teleoperation main node |
| Keyboard Main Node | `hex-teleop-keyboard` | Keyboard teleoperation main node |
| Joystick Test Node | `hex-teleop-joystick-test` | Joystick state visualization test node |
| Keyboard Test Node | `hex-teleop-keyboard-test` | Keyboard state visualization test node |

#### Test Node Details
| Node | Subscribed Topic | Published Topic | Function | Frequency |
|------|------------------|-----------------|----------|-----------|
| `hex-teleop-joystick-test` | `joy` | None | Subscribe to joystick messages, display buttons and axes values in terminal | 10Hz |
| `hex-teleop-keyboard-test` | `keyboard` | None | Subscribe to keyboard messages, display currently pressed letter keys in terminal | 10Hz |

### Launch Description
| Launch File | Description |
|-------------|-------------|
| `joystick_real.launch.py` | Joystick for real robot |
| `joystick_test.launch.py` | Joystick for testing |
| `keyboard_real.launch.py` | Keyboard for real robot |
| `keyboard_test.launch.py` | Keyboard for testing |

### Node Parameter Description
| Parameter | Default Value | Description |
|-----------|---------------|-------------|
| device_path | '' | Device path (empty == auto detect) |
| xbox_view_joy | false | Enable debug output |
| clock_source | driver_timestamp | Timestamp clock source: driver_timestamp or ros |

### Topic Remapping

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