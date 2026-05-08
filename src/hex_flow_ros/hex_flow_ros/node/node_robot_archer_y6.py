import traceback

import numpy as np
from hex_driver_robot import HexRobotArcherY6Callback, HexRobotArcherY6Params
from hex_flow_ros.interface import DataInterface
from hex_flow_ros.ctrl_mode import ArmCtrlMode, GripCtrlMode
from hex_flow_ros_msg.msg import ArmState, ArmCtrl, GripState, GripCtrl


def _ros_ctrl_to_driver_cmd(msg, dof=6):
    return {
        "ts_ns": int(msg.stamp.sec * 1e9 + msg.stamp.nanosec),
        "ctrl_mode": msg.ctrl_mode,
        "jnt_pos": np.array(msg.jnt_pos, dtype=np.float64) if len(msg.jnt_pos) == dof else np.zeros(dof),
        "jnt_vel": np.array(msg.jnt_vel, dtype=np.float64) if len(msg.jnt_vel) == dof else np.zeros(dof),
        "jnt_eff": np.array(msg.jnt_eff, dtype=np.float64) if len(msg.jnt_eff) == dof else np.zeros(dof),
        "pose_pos": np.array(msg.pose_pos, dtype=np.float64),
        "pose_quat": np.array(msg.pose_quat, dtype=np.float64),
        "mit_tau": np.array(msg.mit_tau, dtype=np.float64) if len(msg.mit_tau) == dof else np.zeros(dof),
        "mit_kp": np.array(msg.mit_kp, dtype=np.float64) if len(msg.mit_kp) == dof else np.zeros(dof),
        "mit_kd": np.array(msg.mit_kd, dtype=np.float64) if len(msg.mit_kd) == dof else np.zeros(dof),
        "lim_err": msg.lim_err,
        "lim_vel": np.array(msg.lim_vel, dtype=np.float64) if len(msg.lim_vel) == dof else np.zeros(dof),
        "lim_acc": np.array(msg.lim_acc, dtype=np.float64) if len(msg.lim_acc) == dof else np.zeros(dof),
    }


def _ros_grip_ctrl_to_driver_cmd(msg, dof=1):
    return {
        "ts_ns": int(msg.stamp.sec * 1e9 + msg.stamp.nanosec),
        "ctrl_mode": msg.ctrl_mode,
        "jnt_pos": np.array(msg.jnt_pos, dtype=np.float64) if len(msg.jnt_pos) == dof else np.zeros(dof),
        "jnt_vel": np.array(msg.jnt_vel, dtype=np.float64) if len(msg.jnt_vel) == dof else np.zeros(dof),
        "jnt_eff": np.array(msg.jnt_eff, dtype=np.float64) if len(msg.jnt_eff) == dof else np.zeros(dof),
        "grip_force": msg.grip_force,
        "mit_tau": np.array(msg.mit_tau, dtype=np.float64) if len(msg.mit_tau) == dof else np.zeros(dof),
        "mit_kp": np.array(msg.mit_kp, dtype=np.float64) if len(msg.mit_kp) == dof else np.zeros(dof),
        "mit_kd": np.array(msg.mit_kd, dtype=np.float64) if len(msg.mit_kd) == dof else np.zeros(dof),
        "lim_err": msg.lim_err,
    }


def main():
    interface = DataInterface("robot_archer_y6", rate_hz=1.0)

    interface.set_parameter("host", "192.168.1.100")
    interface.set_parameter("port", 8439)
    interface.set_parameter("ctrl_rate", 500.0)
    interface.set_parameter("state_buffer_size", 200)
    interface.set_parameter("sens_ts", False)
    interface.set_parameter("grip_type", "gp80")
    interface.set_parameter("pose_end_in_flange",
                            [0.187, 0.0, 0.0, 1.0, 0.0, 0.0, 0.0])

    params = HexRobotArcherY6Params(
        host=interface.get_parameter("host"),
        port=interface.get_parameter("port"),
        ctrl_rate=interface.get_parameter("ctrl_rate"),
        state_buffer_size=interface.get_parameter("state_buffer_size"),
        sens_ts=interface.get_parameter("sens_ts"),
        grip_type=interface.get_parameter("grip_type"),
        pose_end_in_flange=np.array(
            interface.get_parameter("pose_end_in_flange"), dtype=np.float64),
    )

    arm_state_pub = interface.create_publisher("arm_state", ArmState, 10)
    grip_state_pub = interface.create_publisher("grip_state", GripState, 10)

    robot = None

    def arm_state_cb(state):
        try:
            msg = ArmState()
            msg.stamp = interface.get_timestamp_from_ns(int(state["ts_ns"]))
            msg.jnt_pos = state["jnt_pos"].tolist()
            msg.jnt_vel = state["jnt_vel"].tolist()
            msg.jnt_eff = state["jnt_eff"].tolist()
            msg.pose_pos = state["pose_pos"].tolist()
            msg.pose_quat = state["pose_quat"].tolist()
            interface.publish(arm_state_pub, msg)
        except Exception:
            traceback.print_exc()

    def grip_state_cb(state):
        try:
            msg = GripState()
            msg.stamp = interface.get_timestamp_from_ns(int(state["ts_ns"]))
            msg.jnt_pos = state["jnt_pos"].tolist()
            msg.jnt_vel = state["jnt_vel"].tolist()
            msg.jnt_eff = state["jnt_eff"].tolist()
            interface.publish(grip_state_pub, msg)
        except Exception:
            traceback.print_exc()

    try:
        robot = HexRobotArcherY6Callback(params, callbacks={
            "arm_state": arm_state_cb,
            "grip_state": grip_state_cb,
        })

        def node_arm_ctrl_cb(msg):
            try:
                cmd = _ros_ctrl_to_driver_cmd(msg, dof=6)
                mode = msg.ctrl_mode
                if mode == ArmCtrlMode.MIT:
                    robot.set_arm_mit_cmd(cmd)
                elif mode == ArmCtrlMode.COMP:
                    robot.set_arm_mit_comp_cmd(cmd)
                elif mode == ArmCtrlMode.POS:
                    robot.set_arm_pos_cmd(cmd)
                elif mode == ArmCtrlMode.POSE:
                    robot.set_arm_pose_cmd(cmd)
                elif mode == ArmCtrlMode.POS_PLAN:
                    robot.set_arm_pos_plan_cmd(cmd)
                elif mode == ArmCtrlMode.POSE_PLAN:
                    robot.set_arm_pose_plan_cmd(cmd)
            except Exception:
                traceback.print_exc()

        def node_grip_ctrl_cb(msg):
            try:
                cmd = _ros_grip_ctrl_to_driver_cmd(msg, dof=1)
                mode = msg.ctrl_mode
                if mode == GripCtrlMode.MIT:
                    robot.set_grip_mit_cmd(cmd)
                elif mode == GripCtrlMode.COMP:
                    robot.set_grip_comp_cmd(cmd)
                elif mode == GripCtrlMode.POS:
                    robot.set_grip_pos_cmd(cmd)
                elif mode == GripCtrlMode.FORCE:
                    robot.set_grip_force_cmd(cmd)
            except Exception:
                traceback.print_exc()

        interface.create_subscription("arm_ctrl", ArmCtrl, node_arm_ctrl_cb, 10)
        interface.create_subscription("grip_ctrl", GripCtrl, node_grip_ctrl_cb, 10)
        robot.start()

        while interface.ok():
            interface.sleep()
    except KeyboardInterrupt:
        pass
    finally:
        if robot:
            robot.stop()
        interface.shutdown()
