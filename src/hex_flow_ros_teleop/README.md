# hex_flow_ros_teleop

HexFlow ROS2 teleoperation package supporting joystick and keyboard input devices.

## Dependencies

### System Dependencies
- Python 3.10+
- ROS2
- `evdev`

### ROS2 Dependencies
- `rclpy`
- `sensor_msgs`
- `hex_flow_ros_common`
- `hex_flow_ros_msg`

### Python Packages
```bash
pip install evdev
```

## Installation

```bash
cd <your_ros2_ws>
colcon build --packages-select hex_flow_ros_teleop
source install/setup.bash
```

## Usage

### Joystick Node

#### Start Joystick Teleoperation Node
```bash
# Auto-detect joystick (default)
ros2 run hex_flow_ros_teleop hex-teleop-joystick

# Specify device path
ros2 run hex_flow_ros_teleop hex-teleop-joystick --ros-args -p device_path:=/dev/input/event3

# Launch file
ros2 launch hex_flow_ros_teleop joystick_test.launch.py
```

#### Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `device_path` | string | `""` | Joystick device path. Empty for auto-detect |

#### Test
```bash
ros2 launch hex_flow_ros_teleop joystick_test.launch.py
```

### Keyboard Node

#### Start Keyboard Teleoperation Node
```bash
ros2 run hex_flow_ros_teleop hex-teleop-keyboard

# Specify device path
ros2 run hex_flow_ros_teleop hex-teleop-keyboard --ros-args -p device_path:=/dev/input/event4
```

#### Parameters
| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `device_path` | string | `""` | Keyboard device path. Empty for auto-detect |

#### Test 
```bash
ros2 launch hex_flow_ros_teleop keyboard_test.launch.py
```

## Published Topics

### Joystick Topic: `teleop_joy` (default topic name, can be remapped via launch file)

**Message Type**: `sensor_msgs/Joy`

**buttons array** (10 elements, index starting from 0):

| Index | evdev Code | Description |
|-------|-----------|-------------|
| 0 | BTN_X | Button X |
| 1 | BTN_Y | Button Y |
| 2 | BTN_A | Button A |
| 3 | BTN_B | Button B |
| 4 | BTN_TL | Left Bumper |
| 5 | BTN_TR | Right Bumper |
| 6 | BTN_TL2 | Left Trigger |
| 7 | BTN_TR2 | Right Trigger |
| 8 | BTN_THUMBL | Left Thumb Button |
| 9 | BTN_THUMBR | Right Thumb Button |

**axes array** (8 elements, value range [-1.0, 1.0], normalized):

| Index | evdev Code | Description |
|-------|-----------|-------------|
| 0 | ABS_X | Left Stick X Axis |
| 1 | ABS_Y | Left Stick Y Axis |
| 2 | ABS_RX | Right Stick X Axis |
| 3 | ABS_RY | Right Stick Y Axis |
| 4 | ABS_Z | Left Trigger (fully pressed = -1.0, released = 1.0) |
| 5 | ABS_RZ | Right Trigger (fully pressed = -1.0, released = 1.0) |
| 6 | ABS_HAT0X | D-Pad X Direction |
| 7 | ABS_HAT0Y | D-Pad Y Direction |

### Keyboard Topic: `keyboard`

**Message Type**: `sensor_msgs/Joy`

**buttons array** (26 elements, corresponding to A-Z):

| Index | Key | Index | Key | Index | Key | Index | Key |
|-------|-----|-------|-----|-------|-----|-------|-----|
| 0 | A | 7 | H | 14 | O | 21 | V |
| 1 | B | 8 | I | 15 | P | 22 | W |
| 2 | C | 9 | J | 16 | Q | 23 | X |
| 3 | D | 10 | K | 17 | R | 24 | Y |
| 4 | E | 11 | L | 18 | S | 25 | Z |
| 5 | F | 12 | M | 19 | T | | |
| 6 | G | 13 | N | 20 | U | | |

**axes array**: empty

## Executables

| Name | Description |
|------|-------------|
| `hex-teleop-joystick` | Joystick teleoperation main node |
| `hex-teleop-keyboard` | Keyboard teleoperation main node |
| `hex-teleop-joystick-test` | Joystick state visualization test node |
| `hex-teleop-keyboard-test` | Keyboard state visualization test node |