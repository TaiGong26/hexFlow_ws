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

## 概述

`hex_flow_ros_msg` 是 HexFlow 自定义的 ROS2 消息定义包，提供机械臂和夹爪的状态与控制消息类型。本包为纯消息定义包，不含可执行节点，仅提供 rosidl 接口供其他包使用。

## 消息类型详情

#### ArmState.msg
| 字段 | 类型 | 描述 |
|------|------|------|
| stamp | builtin_interfaces/Time | 时间戳 |
| jnt_pos | float64[6] | 关节位置（6轴） |
| jnt_vel | float64[6] | 关节速度（6轴） |
| jnt_eff | float64[6] | 关节力矩（6轴） |
| pose_pos | float64[3] | 末端位置（x,y,z） |
| pose_quat | float64[4] | 末端四元数（qx,qy,qz,qw） |

#### ArmCtrl.msg
| 字段 | 类型 | 描述 |
|------|------|------|
| stamp | builtin_interfaces/Time | 时间戳 |
| ctrl_mode | uint8 | 控制模式 |
| jnt_pos | float64[6] | 关节位置（6轴） |
| jnt_vel | float64[6] | 关节速度（6轴） |
| jnt_eff | float64[6] | 关节力矩（6轴） |
| pose_pos | float64[3] | 末端位置（x,y,z） |
| pose_quat | float64[4] | 末端四元数（qx,qy,qz,qw） |
| mit_tau | float64[6] | MIT 模式力矩前馈（6轴） |
| mit_kp | float64[6] | MIT 模式比例增益（6轴） |
| mit_kd | float64[6] | MIT 模式微分增益（6轴） |
| lim_err | float64 | 位置限制误差 |
| lim_vel | float64[6] | 关节速度限制（6轴） |
| lim_acc | float64[6] | 关节加速度限制（6轴） |

#### GripState.msg
| 字段 | 类型 | 描述 |
|------|------|------|
| stamp | builtin_interfaces/Time | 时间戳 |
| jnt_pos | float64[1] | 关节位置 |
| jnt_vel | float64[1] | 关节速度 |
| jnt_eff | float64[1] | 关节力矩 |

#### GripCtrl.msg
| 字段 | 类型 | 描述 |
|------|------|------|
| stamp | builtin_interfaces/Time | 时间戳 |
| ctrl_mode | uint8 | 控制模式 |
| jnt_pos | float64[1] | 关节位置 |
| jnt_vel | float64[1] | 关节速度 |
| jnt_eff | float64[1] | 关节力矩 |
| grip_force | float64 | 夹爪力 |
| mit_tau | float64[1] | MIT 力矩前馈 |
| mit_kp | float64[1] | MIT 比例增益 |
| mit_kd | float64[1] | MIT 微分增益 |
| lim_err | float64 | 位置限制误差 |

### 控制模式枚举值（ArmCtrlMode）
| 值 | 模式 | 描述 |
|----|------|------|
| 0 | MIT | MIT 阻抗控制模式 |
| 1 | COMP | 力矩补偿模式 |
| 2 | POS | 位置控制模式 |
| 3 | POSE | 末端姿态控制模式 |
| 4 | POS_PLAN | 位置规划模式 |
| 5 | POSE_PLAN | 姿态规划模式 |

### 控制模式枚举值（GripCtrlMode）
| 值 | 模式 | 描述 |
|----|------|------|
| 0 | MIT | MIT 阻抗控制模式 |
| 1 | COMP | 力矩补偿模式 |
| 2 | POS | 位置控制模式 |
| 3 | FORCE | 力控制模式 |
