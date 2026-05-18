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

## Overview

`hex_flow_ros_robot` is the HexFlow ROS2 robot arm node package, supporting three types of 6-DOF robot arms: Archer Y6, Firefly Y6, and Hello Y6. It connects to real robot hardware via `hex_driver_robot` driver callbacks, publishes joint states (position/velocity/torque), and subscribes to control commands (MIT/COMP/POS/POSE modes, etc.).

## Dependencies

### ROS2 Dependencies
```bash
git clone https://github.com/hexfellow/hex_flow_ros_common.git
git clone https://github.com/hexfellow/hex_flow_ros_msg.git
git clone https://github.com/hexfellow/hex_flow_ros_robot.git
```

### pip Install
```bash
pip install 'hex_driver_robot>=0.1.0,<0.2.0' 'numpy>=2.2.6' 'hex_util_runtime>=0.0.0,<0.1.0'
```

## Quick Start

### launch Command Examples
```bash
ros2 launch hex_flow_ros_robot archer_y6_real.launch.py host:=192.168.1.100 port:=8439
ros2 launch hex_flow_ros_robot firefly_y6_real.launch.py host:=192.168.1.100 port:=8439
ros2 launch hex_flow_ros_robot hello_y6_real.launch.py host:=192.168.1.100 port:=8439
```

### test Examples
```bash
ros2 launch hex_flow_ros_robot archer_y6_test.launch.py host:=192.168.1.100 port:=8439
ros2 launch hex_flow_ros_robot firefly_y6_test.launch.py host:=192.168.1.100 port:=8439
ros2 launch hex_flow_ros_robot hello_y6_test.launch.py host:=192.168.1.100 port:=8439
```

## Topic Interfaces

### Published Topics
| Name | Type | Description | Additional Notes |
|------|------|-------------|------------------|
| `arm_state` | `ArmState` | 6-DOF joint state | Includes position/velocity/torque/end-effector pose/MIT parameters |
| `grip_state` | `GripState` | Gripper state | Used by Archer/Firefly, GripState type |
| `grip_joy` | `sensor_msgs/Joy` | Hello Y6 gripper state | Unique to Hello Y6, Joy message format |

### Subscribed Topics
| Name | Type | Description | Additional Notes |
|------|------|-------------|------------------|
| `arm_ctrl` | `ArmCtrl` | 6-DOF control command | Supports MIT/COMP/POS/POSE/POS_PLAN/POSE_PLAN modes |
| `grip_ctrl` | `GripCtrl` | Gripper control command | Used by Archer/Firefly, GripCtrl type |
| `grip_led_ctrl` | `std_msgs/Int32MultiArray` | LED control command | Hello Y6 only, Int32MultiArray format |

### Supported Control Modes (ArmCtrl.ctrl_mode)
| Value | Mode | Description |
|----|------|-------------|
| 0 | MIT | MIT impedance control |
| 1 | COMP | Torque compensation |
| 2 | POS | Joint position control |
| 3 | POSE | End-effector pose control |
| 4 | POS_PLAN | Joint position planning |
| 5 | POSE_PLAN | End-effector pose planning |

## Notes

### Node Description
| Node | Executable | Description |
|------|-----------|-------------|
| Archer Y6 Main Node | `hex-robot-archer-y6` | Archer Y6 robot arm control node |
| Firefly Y6 Main Node | `hex-robot-firefly-y6` | Firefly Y6 robot arm control node |
| Hello Y6 Main Node | `hex-robot-hello-y6` | Hello Y6 robot arm control node (with LED gripper) |
| Archer Y6 Test | `hex-robot-archer-y6-test` | Archer Y6 test node (publishes control commands) |
| Firefly Y6 Test | `hex-robot-firefly-y6-test` | Firefly Y6 test node |
| Hello Y6 Test | `hex-robot-hello-y6-test` | Hello Y6 test node |

### Test Node Details
| Node | Subscribed Topics | Published Topics | Function | Frequency |
|------|---------|---------|------|------|
| `hex-robot-archer-y6-test` | `arm_state`, `grip_state` | `arm_ctrl` | Publishes position control commands with fixed joint positions [0.0, -1.5, 3.0, 0.07, 0.0, 0.0] | 500Hz |
| `hex-robot-firefly-y6-test` | `arm_state`, `grip_state` | `arm_ctrl` | Publishes position control commands with fixed joint positions, displays joint position/velocity | 100Hz |
| `hex-robot-hello-y6-test` | `arm_state`, `grip_joy` | `grip_led_ctrl` | Publishes LED control commands (red/green/blue cycle), displays arm state and button info | 10Hz |

### Launch Description
| Launch File | Description |
|------------|------|
| `archer_y6_real.launch.py` | Archer Y6 real robot |
| `archer_y6_test.launch.py` | Archer Y6 test |
| `firefly_y6_real.launch.py` | Firefly Y6 real robot |
| `firefly_y6_test.launch.py` | Firefly Y6 test |
| `hello_y6_real.launch.py` | Hello Y6 real robot |
| `hello_y6_test.launch.py` | Hello Y6 test |

> **Note**: The `host` parameter is required to specify the robot controller IP address.

### Node Parameter Description
| Parameter | Default | Description |
|------|--------|-------------|
| host | 0.0.0.0 | Robot controller IP address |
| port | 8439 | Robot controller port |
| ctrl_rate | 500.0 | Control loop frequency (Hz) |
| state_buffer_size | 200 | State buffer size |
| sens_ts | false | Use device clock as timestamp |
| grip_type | gp80 | Gripper type |
| led_buffer_size | 10 | LED command buffer size (Hello Y6 only) |
| clock_source | driver_timestamp | Timestamp clock source: driver_timestamp or ros |

### Topic Remappings

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