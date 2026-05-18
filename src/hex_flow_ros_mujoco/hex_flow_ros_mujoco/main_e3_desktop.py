import traceback

import numpy as np
from hex_driver_mujoco import HexMujocoE3DesktopCallback, HexMujocoE3DesktopParams
from hex_flow_ros_common.interface import DataInterface
from hex_flow_ros_common.ctrl_mode import ArmCtrlMode, GripCtrlMode
from hex_flow_ros_common.msg_convert import ros_ctrl_to_driver_cmd, ros_grip_ctrl_to_driver_cmd
from hex_flow_ros_msg.msg import ArmState, ArmCtrl, GripState, GripCtrl
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import Image
from std_msgs.msg import Bool


def main():
    ros_interface = DataInterface("mujoco_e3_desktop", rate_hz=500.0)

    # ============ parameter ============
    # state_rate: state publish rate(Hz) → HexMujocoE3DesktopParams → driver state loop
    ros_interface.set_parameter("state_rate", 500.0)
    # cam_rate: camera capture rate(Hz) → driver camera loop
    ros_interface.set_parameter("cam_rate", 30.0)
    # headless: run Mujoco without GUI → driver render config
    ros_interface.set_parameter("headless", False)
    # state_buffer_size: state buffer size → driver state cache
    ros_interface.set_parameter("state_buffer_size", 200)
    # cam_buffer_size: camera buffer size → driver frame cache
    ros_interface.set_parameter("cam_buffer_size", 8)
    # sens_ts: clock source(true=device clock/false=system clock) → driver timestamp
    ros_interface.set_parameter("sens_ts", False)
    # head_cam_type: head camera type → driver camera config
    ros_interface.set_parameter("head_cam_type", "empty")
    # left_cam_type: left arm camera type → driver camera config
    ros_interface.set_parameter("left_cam_type", "empty")
    # right_cam_type: right arm camera type → driver camera config
    ros_interface.set_parameter("right_cam_type", "empty")
    # clock_source: timestamp clock source for published messages (driver_timestamp or ros)
    ros_interface.set_parameter("clock_source", "driver_timestamp")

    params = HexMujocoE3DesktopParams(
        state_rate=ros_interface.get_parameter("state_rate"),
        cam_rate=ros_interface.get_parameter("cam_rate"),
        headless=ros_interface.get_parameter("headless"),
        state_buffer_size=ros_interface.get_parameter("state_buffer_size"),
        cam_buffer_size=ros_interface.get_parameter("cam_buffer_size"),
        sens_ts=ros_interface.get_parameter("sens_ts"),
        cam_type={
            "head": ros_interface.get_parameter("head_cam_type"),
            "left": ros_interface.get_parameter("left_cam_type"),
            "right": ros_interface.get_parameter("right_cam_type"),
        },
    )

    clock_source = ros_interface.get_parameter("clock_source")

    # ============ publisher ============
    arm_state_pubs = {}
    grip_state_pubs = {}
    for side in ("left", "right"):
        arm_state_pubs[side] = ros_interface.create_publisher(
            f"{side}_arm_state", ArmState, 10)
        grip_state_pubs[side] = ros_interface.create_publisher(
            f"{side}_grip_state", GripState, 10)

    pose_pub = ros_interface.create_publisher("obj_pose", PoseStamped, 10)

    color_pubs = {}
    depth_pubs = {}
    for cam in ("head", "left", "right"):
        color_pubs[cam] = ros_interface.create_publisher(
            f"{cam}_color", Image, 10)
        depth_pubs[cam] = ros_interface.create_publisher(
            f"{cam}_depth", Image, 10)
        
    def _make_arm_state_cb(side):
        def cb(state):
            try:
                msg = ArmState()
                msg.stamp = ros_interface.get_clocksource_timestamp(clock_source,state["ts_ns"])
                msg.jnt_pos = state["jnt_pos"].tolist()
                msg.jnt_vel = state["jnt_vel"].tolist()
                msg.jnt_eff = state["jnt_eff"].tolist()
                msg.pose_pos = state["pose_pos"].tolist()
                msg.pose_quat = state["pose_quat"].tolist()
                ros_interface.publish(arm_state_pubs[side], msg)
            except Exception as e:
                ros_interface.loge(f"publish arm state failed: {e}")
        return cb

    def _make_grip_state_cb(side):
        def cb(state):
            try:
                msg = GripState()
                msg.stamp = ros_interface.get_clocksource_timestamp(clock_source,state["ts_ns"])
                msg.jnt_pos = state["jnt_pos"].tolist()
                msg.jnt_vel = state["jnt_vel"].tolist()
                msg.jnt_eff = state["jnt_eff"].tolist()
                ros_interface.publish(grip_state_pubs[side], msg)
            except Exception as e:
                ros_interface.loge(f"publish grip state failed: {e}")
        return cb

    def obj_pose_cb(state):
        try:
            msg = PoseStamped()
            msg.header.stamp = ros_interface.get_clocksource_timestamp(clock_source,state["ts_ns"])
            msg.pose.position.x = float(state["pose_pos"][0])
            msg.pose.position.y = float(state["pose_pos"][1])
            msg.pose.position.z = float(state["pose_pos"][2])
            msg.pose.orientation.x = float(state["pose_quat"][0])
            msg.pose.orientation.y = float(state["pose_quat"][1])
            msg.pose.orientation.z = float(state["pose_quat"][2])
            msg.pose.orientation.w = float(state["pose_quat"][3])
            ros_interface.publish(pose_pub, msg)
        except Exception as e:
            ros_interface.loge(f"publish obj pose failed: {e}")

    def _make_color_img_cb(cam):
        def cb(state):
            try:
                msg = Image()
                msg.header.stamp = ros_interface.get_clocksource_timestamp(clock_source,state["ts_ns"])
                msg.header.frame_id = f"camera_{cam}_optical_frame"
                msg.height, msg.width = state["data"].shape[:2]
                msg.encoding = "bgr8"
                msg.is_bigendian = False
                msg.step = msg.width * 3
                msg.data = state["data"].tobytes()
                ros_interface.publish(color_pubs[cam], msg)
            except Exception as e:
                ros_interface.loge(f"publish color image failed: {e}")
        return cb

    def _make_depth_img_cb(cam):
        def cb(state):
            try:
                msg = Image()
                msg.header.stamp = ros_interface.get_clocksource_timestamp(clock_source,state["ts_ns"])
                msg.header.frame_id = f"camera_{cam}_optical_frame"
                msg.height, msg.width = state["data"].shape[:2]
                msg.encoding = "mono16"
                msg.is_bigendian = False
                msg.step = msg.width * 2
                msg.data = state["data"].tobytes()
                ros_interface.publish(depth_pubs[cam], msg)
            except Exception as e:
                ros_interface.loge(f"publish depth image failed: {e}")
        return cb
    
    callbacks = {}
    for side in ("left", "right"):
        callbacks[f"{side}_arm_state"] = _make_arm_state_cb(side)
        callbacks[f"{side}_grip_state"] = _make_grip_state_cb(side)
    callbacks["obj_pose"] = obj_pose_cb
    for cam in ("head", "left", "right"):
        callbacks[f"{cam}_color_img"] = _make_color_img_cb(cam)
        callbacks[f"{cam}_depth_img"] = _make_depth_img_cb(cam)


    # ============ buffered subscription ============
    for side in ("left", "right"):
        ros_interface.create_subscription_buffered(
            f"{side}_arm_ctrl", ArmCtrl, maxlen=1, queue_size=1)
        ros_interface.create_subscription_buffered(
            f"{side}_grip_ctrl", GripCtrl, maxlen=1, queue_size=1)
    ros_interface.create_subscription_buffered(
        "reset", Bool, maxlen=1, queue_size=1)

    # ============ driver ============
    sim = None
    try:
        sim = HexMujocoE3DesktopCallback(params, callbacks=callbacks)
        sim.start()

        while ros_interface.ok():
            ros_interface.sleep()

            for side in ("left", "right"):
                msg = ros_interface.get(f"{side}_arm_ctrl", latest=True)
                if msg is not None:
                    cmd = ros_ctrl_to_driver_cmd(msg, dof=6)
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

                msg = ros_interface.get(f"{side}_grip_ctrl", latest=True)
                if msg is not None:
                    cmd = ros_grip_ctrl_to_driver_cmd(msg, dof=1)
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

            msg = ros_interface.get("reset", latest=True)
            if msg is not None and msg.data:
                sim.reset()

    except KeyboardInterrupt:
        pass
    finally:
        if sim:
            sim.stop()
        ros_interface.shutdown()
