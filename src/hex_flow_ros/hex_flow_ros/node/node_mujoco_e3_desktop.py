import traceback

import numpy as np
from hex_driver_mujoco import HexMujocoE3DesktopCallback, HexMujocoE3DesktopParams
from hex_flow_ros.interface import DataInterface
from hex_flow_ros.ctrl_mode import ArmCtrlMode, GripCtrlMode
from hex_flow_ros_msg.msg import ArmState, ArmCtrl, GripState, GripCtrl
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import Image
from std_msgs.msg import Bool


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
    interface = DataInterface("mujoco_e3_desktop", rate_hz=500.0)

    interface.set_parameter("state_rate", 1000.0)
    interface.set_parameter("cam_rate", 30.0)
    interface.set_parameter("headless", False)
    interface.set_parameter("state_buffer_size", 200)
    interface.set_parameter("cam_buffer_size", 8)
    interface.set_parameter("sens_ts", False)
    interface.set_parameter("head_cam_type", "empty")
    interface.set_parameter("left_cam_type", "empty")
    interface.set_parameter("right_cam_type", "empty")

    params = HexMujocoE3DesktopParams(
        state_rate=interface.get_parameter("state_rate"),
        cam_rate=interface.get_parameter("cam_rate"),
        headless=interface.get_parameter("headless"),
        state_buffer_size=interface.get_parameter("state_buffer_size"),
        cam_buffer_size=interface.get_parameter("cam_buffer_size"),
        sens_ts=interface.get_parameter("sens_ts"),
        cam_type={
            "head": interface.get_parameter("head_cam_type"),
            "left": interface.get_parameter("left_cam_type"),
            "right": interface.get_parameter("right_cam_type"),
        },
    )

    # ---- Publishers (11, relative topics, namespace /sim) ----
    arm_state_pubs = {}
    grip_state_pubs = {}
    for side in ("left", "right"):
        arm_state_pubs[side] = interface.create_publisher(
            f"{side}_arm_state", ArmState, 10)
        grip_state_pubs[side] = interface.create_publisher(
            f"{side}_grip_state", GripState, 10)

    pose_pub = interface.create_publisher("obj_pose", PoseStamped, 10)

    color_pubs = {}
    depth_pubs = {}
    for cam in ("head", "left", "right"):
        color_pubs[cam] = interface.create_publisher(
            f"{cam}_color", Image, 10)
        depth_pubs[cam] = interface.create_publisher(
            f"{cam}_depth", Image, 10)

    # ---- Buffered Subscriptions (5, polling mode) ----
    for side in ("left", "right"):
        interface.create_subscription_buffered(
            f"{side}_arm_ctrl", ArmCtrl, maxlen=1, queue_size=1)
        interface.create_subscription_buffered(
            f"{side}_grip_ctrl", GripCtrl, maxlen=1, queue_size=1)
    interface.create_subscription_buffered(
        "reset", Bool, maxlen=1, queue_size=1)

    sim = None

    # ---- Driver callbacks ----
    def _make_arm_state_cb(side):
        def cb(state):
            try:
                msg = ArmState()
                msg.stamp = interface.get_timestamp_from_ns(
                    int(state["ts_ns"]))
                msg.jnt_pos = state["jnt_pos"].tolist()
                msg.jnt_vel = state["jnt_vel"].tolist()
                msg.jnt_eff = state["jnt_eff"].tolist()
                msg.pose_pos = state["pose_pos"].tolist()
                msg.pose_quat = state["pose_quat"].tolist()
                interface.publish(arm_state_pubs[side], msg)
            except Exception:
                traceback.print_exc()
        return cb

    def _make_grip_state_cb(side):
        def cb(state):
            try:
                msg = GripState()
                msg.stamp = interface.get_timestamp_from_ns(
                    int(state["ts_ns"]))
                msg.jnt_pos = state["jnt_pos"].tolist()
                msg.jnt_vel = state["jnt_vel"].tolist()
                msg.jnt_eff = state["jnt_eff"].tolist()
                interface.publish(grip_state_pubs[side], msg)
            except Exception:
                traceback.print_exc()
        return cb

    def obj_pose_cb(state):
        try:
            msg = PoseStamped()
            msg.header.stamp = interface.get_timestamp_from_ns(
                int(state["ts_ns"]))
            msg.pose.position.x = float(state["pose_pos"][0])
            msg.pose.position.y = float(state["pose_pos"][1])
            msg.pose.position.z = float(state["pose_pos"][2])
            msg.pose.orientation.x = float(state["pose_quat"][0])
            msg.pose.orientation.y = float(state["pose_quat"][1])
            msg.pose.orientation.z = float(state["pose_quat"][2])
            msg.pose.orientation.w = float(state["pose_quat"][3])
            interface.publish(pose_pub, msg)
        except Exception:
            traceback.print_exc()

    def _make_color_img_cb(cam):
        def cb(state):
            try:
                msg = Image()
                msg.header.stamp = interface.get_timestamp_from_ns(
                    int(state["ts_ns"]))
                msg.header.frame_id = f"camera_{cam}_optical_frame"
                msg.height, msg.width = state["data"].shape[:2]
                msg.encoding = "bgr8"
                msg.is_bigendian = False
                msg.step = msg.width * 3
                msg.data = state["data"].tobytes()
                interface.publish(color_pubs[cam], msg)
            except Exception:
                traceback.print_exc()
        return cb

    def _make_depth_img_cb(cam):
        def cb(state):
            try:
                msg = Image()
                msg.header.stamp = interface.get_timestamp_from_ns(
                    int(state["ts_ns"]))
                msg.header.frame_id = f"camera_{cam}_optical_frame"
                msg.height, msg.width = state["data"].shape[:2]
                msg.encoding = "16UC1"
                msg.is_bigendian = False
                msg.step = msg.width * 2
                msg.data = state["data"].tobytes()
                interface.publish(depth_pubs[cam], msg)
            except Exception:
                traceback.print_exc()
        return cb

    callbacks = {}
    for side in ("left", "right"):
        callbacks[f"{side}_arm_state"] = _make_arm_state_cb(side)
        callbacks[f"{side}_grip_state"] = _make_grip_state_cb(side)
    callbacks["obj_pose"] = obj_pose_cb
    for cam in ("head", "left", "right"):
        callbacks[f"{cam}_color_img"] = _make_color_img_cb(cam)
        callbacks[f"{cam}_depth_img"] = _make_depth_img_cb(cam)

    try:
        sim = HexMujocoE3DesktopCallback(params, callbacks=callbacks)
        sim.start()

        while interface.ok():
            interface.sleep()  # 500 Hz

            for side in ("left", "right"):
                # Poll arm_ctrl
                msg = interface.get(f"{side}_arm_ctrl", latest=True)
                if msg is not None:
                    cmd = _ros_ctrl_to_driver_cmd(msg, dof=6)
                    mode = msg.ctrl_mode
                    fn_map = {
                        ArmCtrlMode.MIT: getattr(sim, f"set_{side}_arm_mit_cmd"),
                        ArmCtrlMode.COMP: getattr(sim, f"set_{side}_arm_mit_comp_cmd"),
                        ArmCtrlMode.POS: getattr(sim, f"set_{side}_arm_pos_cmd"),
                        ArmCtrlMode.POSE: getattr(sim, f"set_{side}_arm_pose_cmd"),
                        ArmCtrlMode.POS_PLAN: getattr(sim, f"set_{side}_arm_pos_plan_cmd"),
                        ArmCtrlMode.POSE_PLAN: getattr(sim, f"set_{side}_arm_pose_plan_cmd"),
                    }
                    fn = fn_map.get(mode)
                    if fn is not None:
                        fn(cmd)

                # Poll grip_ctrl
                msg = interface.get(f"{side}_grip_ctrl", latest=True)
                if msg is not None:
                    cmd = _ros_grip_ctrl_to_driver_cmd(msg, dof=1)
                    mode = msg.ctrl_mode
                    fn_map = {
                        GripCtrlMode.MIT: getattr(sim, f"set_{side}_grip_mit_cmd"),
                        GripCtrlMode.COMP: getattr(sim, f"set_{side}_grip_comp_cmd"),
                        GripCtrlMode.POS: getattr(sim, f"set_{side}_grip_pos_cmd"),
                        GripCtrlMode.FORCE: getattr(sim, f"set_{side}_grip_force_cmd"),
                    }
                    fn = fn_map.get(mode)
                    if fn is not None:
                        fn(cmd)

            # Poll reset
            msg = interface.get("reset", latest=True)
            if msg is not None and msg.data:
                sim.reset()

    except KeyboardInterrupt:
        pass
    finally:
        if sim:
            sim.stop()
        interface.shutdown()
