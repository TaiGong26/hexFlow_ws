# hex_flow_ros_mujoco

## Overview

`hex_flow_ros_mujoco` is the HexFlow ROS2 MuJoCo simulation node package, supporting E3 Desktop dual-arm and Archer Y6 single-arm robot configurations. It uses simulation callback drivers from `hex_driver_mujoco` to control the MuJoCo physics engine, publishes simulation state (joint states/end-effector pose/camera images), subscribes to control commands, and executes simulations.

## Dependencies

### ROS2 Dependencies
```bash
git clone https://github.com/hexfellow/hex_flow_ros_common.git
git clone https://github.com/hexfellow/hex_flow_ros_msg.git
git clone https://github.com/hexfellow/hex_flow_ros_mujoco.git
```

### pip Installation
```bash
pip install 'hex_driver_mujoco>=0.1.0,<0.2.0' 'numpy>=2.2.6' 'hex_util_runtime>=0.0.0,<0.1.0'
```

## Quick Start

### launch Commands
```bash
ros2 launch hex_flow_ros_mujoco e3_desktop_sim.launch.py
ros2 launch hex_flow_ros_mujoco archer_y6_sim.launch.py
```

### test Examples
```bash
ros2 launch hex_flow_ros_mujoco e3_desktop_sim_test.launch.py
ros2 launch hex_flow_ros_mujoco archer_y6_sim_test.launch.py
```

## Topic Interfaces

### Published Topics (E3 Desktop)
| Name | Type | Description | Additional Info |
|------|------|-------------|-----------------|
| `left_arm_state` | `ArmState` | Left arm joint state | 6-DOF |
| `right_arm_state` | `ArmState` | Right arm joint state | 6-DOF |
| `left_grip_state` | `GripState` | Left gripper state | 1-DOF |
| `right_grip_state` | `GripState` | Right gripper state | 1-DOF |
| `obj_pose` | `geometry_msgs/PoseStamped` | Target object pose | MuJoCo simulation object |
| `head_color` | `sensor_msgs/Image` | Head camera color image | Depends on head_cam_type |
| `head_depth` | `sensor_msgs/Image` | Head camera depth image | |
| `left_color` | `sensor_msgs/Image` | Left arm camera color image | |
| `left_depth` | `sensor_msgs/Image` | Left arm camera depth image | |
| `right_color` | `sensor_msgs/Image` | Right arm camera color image | |
| `right_depth` | `sensor_msgs/Image` | Right arm camera depth image | |

### Published Topics (Archer Y6)
| Name | Type | Description | Additional Info |
|------|------|-------------|-----------------|
| `arm_state` | `ArmState` | Joint state | 6-DOF |
| `grip_state` | `GripState` | Gripper state | 1-DOF |
| `obj_pose` | `geometry_msgs/PoseStamped` | Target object pose | |
| `color` | `sensor_msgs/Image` | Camera color image | |
| `depth` | `sensor_msgs/Image` | Camera depth image | |

### Subscribed Topics (Common)
| Name | Type | Description | Additional Info |
|------|------|-------------|-----------------|
| `left_arm_ctrl` / `arm_ctrl` | `ArmCtrl` | Arm control command | E3 Desktop: left_arm_ctrl; Archer Y6: arm_ctrl |
| `right_arm_ctrl` | `ArmCtrl` | Right arm control command | E3 Desktop only |
| `left_grip_ctrl` / `grip_ctrl` | `GripCtrl` | Gripper control command | E3 Desktop: left_grip_ctrl; Archer Y6: grip_ctrl |
| `right_grip_ctrl` | `GripCtrl` | Right gripper control command | E3 Desktop only |
| `reset` | `std_msgs/Bool` | Simulation reset signal | When true, resets robot to initial pose |

### Camera Type Parameters
| Type | Description |
|------|-------------|
| `empty` | None |
| `usb` | USB V4L2 camera |
| `realsense` | Intel RealSense D400 series |
| `berxel` | Berxel ToF depth camera |

## Notes

### Node Description
| Node | Executable | Description |
|------|-----------|-------------|
| E3 Desktop Simulation | `hex-mujoco-e3-desktop` | E3 Desktop dual-arm simulation main node |
| Archer Y6 Simulation | `hex-mujoco-archer-y6` | Archer Y6 single-arm simulation main node |
| E3 Desktop Test | `hex-mujoco-e3-desktop-test` | E3 Desktop test node (publishes control commands + displays state) |
| Archer Y6 Test | `hex-mujoco-archer-y6-test` | Archer Y6 test node |

#### Test Node Details
| Node | Subscribed Topics | Published Topics | Function | Frequency |
|------|------------------|------------------|----------|-----------|
| `hex-mujoco-e3-desktop-test` | `left_arm_state`, `right_arm_state` | `left_arm_ctrl`, `right_arm_ctrl` | Subscribes to dual-arm state, publishes position control commands at fixed joint positions [0.0, -1.5, 3.0, 0.07, 0.0, 0.0] | 100Hz |
| `hex-mujoco-archer-y6-test` | `arm_state` | `arm_ctrl` | Subscribes to arm state, publishes position control commands at fixed joint positions | 100Hz |

### Launch Description
| Launch File | Description |
|------------|-------------|
| `e3_desktop_sim.launch.py` | E3 Desktop simulation |
| `e3_desktop_sim_test.launch.py` | E3 Desktop simulation + test |
| `archer_y6_sim.launch.py` | Archer Y6 simulation |
| `archer_y6_sim_test.launch.py` | Archer Y6 simulation + test |

### Node Parameter Description
| Parameter | Default Value | Description |
|------|--------|------|
| headless | false | Run MuJoCo without GUI window |
| state_rate | 1000.0 | State publishing rate (Hz) |
| state_buffer_size | 200 | State buffer size |
| cam_buffer_size | 8 | Camera buffer size |
| cam_rate | 30.0 | Camera publishing rate (Hz) |
| camera_type | usb | Camera type (usb/realsense/berxel) |
| sens_ts | false | Use device clock as timestamp |
| head_cam_type | empty | Head camera type (empty/usb/realsense/berxel) |
| left_cam_type | empty | Left arm camera type |
| right_cam_type | empty | Right arm camera type |
| clock_source | driver_timestamp | Timestamp clock source: driver_timestamp or ros |

### Topic Remapping

#### archer_y6_sim.launch.py
```python
remappings=[
    ('arm_state', '/mujoco_archer_y6/arm_state'),
    ('arm_ctrl', '/mujoco_archer_y6/arm_ctrl'),
    ('grip_state', '/mujoco_archer_y6/grip_state'),
    ('grip_ctrl', '/mujoco_archer_y6/grip_ctrl'),
],
```

#### archer_y6_sim_test.launch.py
```python
# mujoco_archer_y6
remappings=[
    ('arm_state', 'mujoco_archer_y6/arm_state'),
    ('grip_state', 'mujoco_archer_y6/grip_state'),
    ('obj_pose', 'mujoco_archer_y6/obj_pose'),
    ('color', 'mujoco_archer_y6/color'),
    ('depth', 'mujoco_archer_y6/depth'),
    ('arm_ctrl', 'mujoco_archer_y6/arm_ctrl'),
    ('grip_ctrl', 'mujoco_archer_y6/grip_ctrl'),
    ('reset', 'mujoco_archer_y6/reset'),
],
# mujoco_archer_y6_test
remappings=[
    ('arm_state', 'mujoco_archer_y6/arm_state'),
    ('arm_ctrl', 'mujoco_archer_y6/arm_ctrl'),
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
],
```

#### e3_desktop_sim_test.launch.py
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
],
```