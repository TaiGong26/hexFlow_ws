import numpy as np


def ros_ctrl_to_driver_cmd(msg, dof=6):
    """Convert ROS 2 ArmCtrl message to driver cmd dict (numpy arrays)."""
    return {
        "ts_ns": int(msg.stamp.sec * 1_000_000_000 + msg.stamp.nanosec),
        "ctrl_mode": msg.ctrl_mode,
        "jnt_pos": _arr(msg.jnt_pos, dof),
        "jnt_vel": _arr(msg.jnt_vel, dof),
        "jnt_eff": _arr(msg.jnt_eff, dof),
        "pose_pos": np.array(msg.pose_pos, dtype=np.float64),
        "pose_quat": np.array(msg.pose_quat, dtype=np.float64),
        "mit_tau": _arr(msg.mit_tau, dof),
        "mit_kp": _arr(msg.mit_kp, dof),
        "mit_kd": _arr(msg.mit_kd, dof),
        "lim_err": msg.lim_err,
        "lim_vel": _arr(msg.lim_vel, dof),
        "lim_acc": _arr(msg.lim_acc, dof),
    }


def ros_grip_ctrl_to_driver_cmd(msg, dof=1):
    """Convert ROS 2 GripCtrl message to driver cmd dict (numpy arrays)."""
    return {
        "ts_ns": int(msg.stamp.sec * 1_000_000_000 + msg.stamp.nanosec),
        "ctrl_mode": msg.ctrl_mode,
        "jnt_pos": _arr(msg.jnt_pos, dof),
        "jnt_vel": _arr(msg.jnt_vel, dof),
        "jnt_eff": _arr(msg.jnt_eff, dof),
        "grip_force": msg.grip_force,
        "mit_tau": _arr(msg.mit_tau, dof),
        "mit_kp": _arr(msg.mit_kp, dof),
        "mit_kd": _arr(msg.mit_kd, dof),
        "lim_err": msg.lim_err,
    }


def _arr(values, dof):
    return np.array(values, dtype=np.float64) if len(values) == dof else np.zeros(dof)
