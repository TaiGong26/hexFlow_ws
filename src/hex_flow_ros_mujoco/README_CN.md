# hex_flow_ros_mujoco

## 概述

`hex_flow_ros_mujoco` 是 HexFlow ROS2 MuJoCo 仿真节点包，支持 E3 Desktop 双臂和 Archer Y6 单臂两种机器人配置，通过 `hex_driver_mujoco` 的仿真回调驱动 MuJoCo 物理引擎，发布仿真状态（关节状态/末端位姿/相机图像），订阅控制指令并执行仿真。

## 依赖安装

### ROS2 依赖
```bash
git clone https://github.com/hexfellow/hex_flow_ros_common.git
git clone https://github.com/hexfellow/hex_flow_ros_msg.git
git clone https://github.com/hexfellow/hex_flow_ros_mujoco.git
```

### pip 安装
```bash
pip install 'hex_driver_mujoco>=0.1.0,<0.2.0' 'numpy>=2.2.6' 'hex_util_runtime>=0.0.0,<0.1.0'
```

## 快速使用

### launch 命令示例
```bash
ros2 launch hex_flow_ros_mujoco e3_desktop_sim.launch.py
ros2 launch hex_flow_ros_mujoco archer_y6_sim.launch.py
```

### test 示例
```bash
ros2 launch hex_flow_ros_mujoco e3_desktop_sim_test.launch.py
ros2 launch hex_flow_ros_mujoco archer_y6_sim_test.launch.py
```

## 话题接口

### 发布话题（E3 Desktop）
| 名称 | 类型 | 描述 | 补充描述 |
|------|------|------|---------|
| `left_arm_state` | `ArmState` | 左臂关节状态 | 6-DOF |
| `right_arm_state` | `ArmState` | 右臂关节状态 | 6-DOF |
| `left_grip_state` | `GripState` | 左夹爪状态 | 1-DOF |
| `right_grip_state` | `GripState` | 右夹爪状态 | 1-DOF |
| `obj_pose` | `geometry_msgs/PoseStamped` | 目标物体位姿 | MuJoCo 仿真物体 |
| `head_color` | `sensor_msgs/Image` | 头部相机彩色图 | head_cam_type 指定类型 |
| `head_depth` | `sensor_msgs/Image` | 头部相机深度图 | |
| `left_color` | `sensor_msgs/Image` | 左臂相机彩色图 | |
| `left_depth` | `sensor_msgs/Image` | 左臂相机深度图 | |
| `right_color` | `sensor_msgs/Image` | 右臂相机彩色图 | |
| `right_depth` | `sensor_msgs/Image` | 右臂相机深度图 | |

### 发布话题（Archer Y6）
| 名称 | 类型 | 描述 | 补充描述 |
|------|------|------|---------|
| `arm_state` | `ArmState` | 关节状态 | 6-DOF |
| `grip_state` | `GripState` | 夹爪状态 | 1-DOF |
| `obj_pose` | `geometry_msgs/PoseStamped` | 目标物体位姿 | |
| `color` | `sensor_msgs/Image` | 相机彩色图 | |
| `depth` | `sensor_msgs/Image` | 相机深度图 | |

### 订阅话题（通用）
| 名称 | 类型 | 描述 | 补充描述 |
|------|------|------|---------|
| `left_arm_ctrl` / `arm_ctrl` | `ArmCtrl` | 臂控制指令 | E3 Desktop: left_arm_ctrl；Archer Y6: arm_ctrl |
| `right_arm_ctrl` | `ArmCtrl` | 右臂控制指令 | 仅 E3 Desktop |
| `left_grip_ctrl` / `grip_ctrl` | `GripCtrl` | 夹爪控制指令 | E3 Desktop: left_grip_ctrl；Archer Y6: grip_ctrl |
| `right_grip_ctrl` | `GripCtrl` | 右夹爪控制指令 | 仅 E3 Desktop |
| `reset` | `std_msgs/Bool` | 仿真重置信号 | true 时重置机械臂到初始位姿 |

### 相机类型参数说明
| 类型 | 描述 |
|------|------|
| `empty` | 无 |
| `usb` | USB V4L2 相机 |
| `realsense` | Intel RealSense D400 系列 |
| `berxel` | Berxel ToF 深度相机 |

## 说明

### 节点说明
| 节点 | 可执行文件 | 描述 |
|------|-----------|------|
| E3 Desktop 仿真 | `hex-mujoco-e3-desktop` | E3 Desktop 双臂仿真主节点 |
| Archer Y6 仿真 | `hex-mujoco-archer-y6` | Archer Y6 单臂仿真主节点 |
| E3 Desktop 测试 | `hex-mujoco-e3-desktop-test` | E3 Desktop 测试节点（发布控制指令+显示状态） |
| Archer Y6 测试 | `hex-mujoco-archer-y6-test` | Archer Y6 测试节点 |

#### Test 节点详情
| 节点 | 订阅话题 | 发布话题 | 功能 | 频率 |
|------|---------|---------|------|------|
| `hex-mujoco-e3-desktop-test` | `left_arm_state`, `right_arm_state` | `left_arm_ctrl`, `right_arm_ctrl` | 订阅双臂状态，以固定关节位置 [0.0, -1.5, 3.0, 0.07, 0.0, 0.0] 发布位置控制指令 | 100Hz |
| `hex-mujoco-archer-y6-test` | `arm_state` | `arm_ctrl` | 订阅臂状态，以固定关节位置发布位置控制指令 | 100Hz |

### Launch 说明
| Launch 文件 | 描述 |
|------------|------|
| `e3_desktop_sim.launch.py` | E3 Desktop 仿真 |
| `e3_desktop_sim_test.launch.py` | E3 Desktop 仿真+测试 |
| `archer_y6_sim.launch.py` | Archer Y6 仿真 |
| `archer_y6_sim_test.launch.py` | Archer Y6 仿真+测试 |

### 节点参数说明
| 参数 | 默认值 | 描述 |
|------|--------|------|
| headless | false | 无 GUI 窗口运行 MuJoCo |
| state_rate | 1000.0 | 状态发布频率（Hz） |
| state_buffer_size | 200 | 状态 buffer 大小 |
| cam_buffer_size | 8 | 相机 buffer 大小 |
| cam_rate | 30.0 | 相机发布频率（Hz） |
| camera_type | usb | 相机类型（usb/realsense/berxel） |
| sens_ts | false | 使用设备时钟作为时间戳 |
| head_cam_type | empty | 头部相机类型（empty/usb/realsense/berxel） |
| left_cam_type | empty | 左臂相机类型 |
| right_cam_type | empty | 右臂相机类型 |
| clock_source | driver_timestamp | 时间戳时钟源：driver_timestamp 或 ros |

### 话题重映射

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