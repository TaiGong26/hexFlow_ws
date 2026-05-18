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

## Overview

`hex_flow_ros_template` is the HexFlow ROS2 application template package, providing two robot arm application templates: Archer Y6 single-arm and E3 Desktop dual-arm. These templates demonstrate a complete init/work/exit control flow. The template nodes implement state machine control: the init phase moves the arm to a stable position (position control), the work phase maintains (COMP mode with zero torque compensation), and the exit phase returns to a stable pose. Press 'q' to exit.

## Dependencies

### ROS2 Dependencies
```bash
git clone https://github.com/hexfellow/hex_flow_ros_common.git
git clone https://github.com/hexfellow/hex_flow_ros_msg.git
git clone https://github.com/hexfellow/hex_flow_ros_template.git
```

### pip Installation
```bash
pip install 'numpy>=2.2.6' 'hex_util_runtime>=0.0.0,<0.1.0'
```

## Quick Start

### Launch Command Examples
```bash
ros2 launch hex_flow_ros_template archer_y6_sim.launch.py
ros2 launch hex_flow_ros_template e3_desktop_sim.launch.py
```

### Usage with Parameters
```bash
ros2 launch hex_flow_ros_template archer_y6_real.launch.py host:=192.168.1.100 port:=8439
ros2 launch hex_flow_ros_template e3_desktop_real.launch.py host:=192.168.1.100 port:=8439
```

## Topic Interfaces

### Published Topics (Archer Y6)
| Name | Type | Description | Additional Info |
|------|------|-------------|-----------------|
| `arm_ctrl` | `ArmCtrl` | Arm control command | init/exit use POS mode, work uses COMP zero torque |
| `grip_ctrl` | `GripCtrl` | Gripper control command | Same as above |

### Subscribed Topics (Archer Y6)
| Name | Type | Description | Additional Info |
|------|------|-------------|-----------------|
| `arm_state` | `ArmState` | Arm joint state | Used to determine if target position is reached |
| `grip_state` | `GripState` | Gripper state | Used to determine if target position is reached |
| `keys` | `sensor_msgs/Joy` | Keyboard key state | Exit triggered when buttons[16]='q' |

### Published Topics (E3 Desktop)
| Name | Type | Description | Additional Info |
|------|------|-------------|-----------------|
| `left_arm_ctrl` | `ArmCtrl` | Left arm control command | |
| `right_arm_ctrl` | `ArmCtrl` | Right arm control command | |
| `left_grip_ctrl` | `GripCtrl` | Left gripper control command | |
| `right_grip_ctrl` | `GripCtrl` | Right gripper control command | |

### Subscribed Topics (E3 Desktop)
| Name | Type | Description | Additional Info |
|------|------|-------------|-----------------|
| `left_arm_state` | `ArmState` | Left arm state | |
| `right_arm_state` | `ArmState` | Right arm state | |
| `left_grip_state` | `GripState` | Left gripper state | |
| `right_grip_state` | `GripState` | Right gripper state | |
| `keys` | `sensor_msgs/Joy` | Keyboard key state | Exit triggered when buttons[16]='q' |

### Workflow State Description
| Phase | Control Mode | Description |
|-------|-------------|-------------|
| `init` | POS (ArmCtrlMode=2) | Move arm and gripper to stable position |
| `work` | COMP (ArmCtrlMode=1) | Send zero torque compensation command to maintain current position |
| `exit` | POS (ArmCtrlMode=2) | Return arm and gripper to stable position then exit |

## Notes

### Node Description
| Node | Executable | Description |
|------|------------|-------------|
| Archer Y6 Template | `hex-template-archer-y6` | Archer Y6 single-arm application template |
| E3 Desktop Template | `hex-template-e3-desktop` | E3 Desktop dual-arm application template |

### Launch Description
| Launch File | Description |
|-------------|-------------|
| `archer_y6_real.launch.py` | Archer Y6 real machine template |
| `archer_y6_sim.launch.py` | Archer Y6 simulation template |
| `e3_desktop_real.launch.py` | E3 Desktop real machine template |
| `e3_desktop_sim.launch.py` | E3 Desktop simulation template |

> **Note**: The `host` parameter is required to specify the robot arm controller IP address.

### Node Parameters
| Parameter | Default Value | Description |
|-----------|--------------|-------------|
| host | 192.168.1.100 | Robot arm controller IP address |
| port | 8439 | Robot arm controller port |
| clock_source | driver_timestamp | Timestamp clock source: driver_timestamp or ros |

### Key Parameters
| Parameter | Default Value | Description |
|-----------|--------------|-------------|
| rate_hz | 500.0 | Control loop frequency |
| arm_stable_pos | [0.0, -1.5, 3.0, 0.07, 0.0, 0.0] | Arm stable position (6 axes) |
| grip_stable_pos | [0.5] | Gripper stable position |
| arrive_threshold | 0.06 | Error threshold for arrival judgment |
| clock_source | `"driver_timestamp"` | Timestamp clock source: `driver_timestamp` or `ros` |

### Topic Remapping

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