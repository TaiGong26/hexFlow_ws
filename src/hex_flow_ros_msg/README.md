<h1 align="center">HEX FLOW ROS MSG</h1>

<p align="center">
    <a href="https://github.com/hexfellow/hex_flow_ros_msg/stargazers">
        <img src="https://img.shields.io/github/stars/hexfellow/hex_flow_ros_msg?style=flat-square&logo=github" />
    </a>
    <a href="https://github.com/hexfellow/hex_flow_ros_msg/forks">
        <img src="https://img.shields.io/github/forks/hexfellow/hex_flow_ros_msg?style=flat-square&logo=github" />
    </a>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    <a href="https://github.com/hexfellow/hex_flow_ros_msg/issues">
        <img src="https://img.shields.io/github/issues/hexfellow/hex_flow_ros_msg?style=flat-square&logo=github" />
    </a>
</p>

---

# hex_flow_ros_msg

## Overview

`hex_flow_ros_msg` is the custom ROS2 message definition package for HexFlow, providing state and control message types for robotic arms and grippers. This package is a pure message definition package with no executable nodes; it only provides rosidl interfaces for other packages to use.

## Message Types

#### ArmState.msg
| Field | Type | Description |
|------|------|------|
| stamp | builtin_interfaces/Time | Timestamp |
| jnt_pos | float64[6] | Joint positions (6-axis) |
| jnt_vel | float64[6] | Joint velocities (6-axis) |
| jnt_eff | float64[6] | Joint torques (6-axis) |
| pose_pos | float64[3] | End-effector position (x,y,z) |
| pose_quat | float64[4] | End-effector quaternion (qx,qy,qz,qw) |

#### ArmCtrl.msg
| Field | Type | Description |
|------|------|------|
| stamp | builtin_interfaces/Time | Timestamp |
| ctrl_mode | uint8 | Control mode |
| jnt_pos | float64[6] | Joint positions (6-axis) |
| jnt_vel | float64[6] | Joint velocities (6-axis) |
| jnt_eff | float64[6] | Joint torques (6-axis) |
| pose_pos | float64[3] | End-effector position (x,y,z) |
| pose_quat | float64[4] | End-effector quaternion (qx,qy,qz,qw) |
| mit_tau | float64[6] | MIT mode torque feedforward (6-axis) |
| mit_kp | float64[6] | MIT mode proportional gain (6-axis) |
| mit_kd | float64[6] | MIT mode derivative gain (6-axis) |
| lim_err | float64 | Position limit error |
| lim_vel | float64[6] | Joint velocity limits (6-axis) |
| lim_acc | float64[6] | Joint acceleration limits (6-axis) |

#### GripState.msg
| Field | Type | Description |
|------|------|------|
| stamp | builtin_interfaces/Time | Timestamp |
| jnt_pos | float64[1] | Joint position |
| jnt_vel | float64[1] | Joint velocity |
| jnt_eff | float64[1] | Joint torque |

#### GripCtrl.msg
| Field | Type | Description |
|------|------|------|
| stamp | builtin_interfaces/Time | Timestamp |
| ctrl_mode | uint8 | Control mode |
| jnt_pos | float64[1] | Joint position |
| jnt_vel | float64[1] | Joint velocity |
| jnt_eff | float64[1] | Joint torque |
| grip_force | float64 | Gripper force |
| mit_tau | float64[1] | MIT torque feedforward |
| mit_kp | float64[1] | MIT proportional gain |
| mit_kd | float64[1] | MIT derivative gain |
| lim_err | float64 | Position limit error |

### Control Mode Enumeration (ArmCtrlMode)
| Value | Mode | Description |
|----|------|------|
| 0 | MIT | MIT impedance control mode |
| 1 | COMP | Torque compensation mode |
| 2 | POS | Position control mode |
| 3 | POSE | End-effector pose control mode |
| 4 | POS_PLAN | Position planning mode |
| 5 | POSE_PLAN | Pose planning mode |

### Control Mode Enumeration (GripCtrlMode)
| Value | Mode | Description |
|----|------|------|
| 0 | MIT | MIT impedance control mode |
| 1 | COMP | Torque compensation mode |
| 2 | POS | Position control mode |
| 3 | FORCE | Force control mode |