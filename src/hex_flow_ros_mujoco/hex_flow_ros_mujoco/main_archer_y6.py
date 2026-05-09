import traceback

import numpy as np
from hex_driver_mujoco import HexMujocoArcherY6Callback, HexMujocoArcherY6Params
from hex_flow_ros_common.interface import DataInterface
from hex_flow_ros_common.ctrl_mode import ArmCtrlMode, GripCtrlMode
from hex_flow_ros_common.msg_convert import ros_ctrl_to_driver_cmd, ros_grip_ctrl_to_driver_cmd
from hex_flow_ros_msg.msg import ArmState, ArmCtrl, GripState, GripCtrl
from geometry_msgs.msg import PoseStamped
from sensor_msgs.msg import Image
from std_msgs.msg import Bool


def main():
    interface = DataInterface("mujoco_archer_y6", rate_hz=1.0)

    # ============ parameter ============
    # state_rate: state publish rate(Hz) → HexMujocoArcherY6Params → driver state loop
    interface.set_parameter("state_rate", 500.0)
    # cam_rate: camera capture rate(Hz) → driver camera loop
    interface.set_parameter("cam_rate", 30.0)
    # headless: run Mujoco without GUI → driver render config
    interface.set_parameter("headless", False)
    # state_buffer_size: state buffer size → driver state cache
    interface.set_parameter("state_buffer_size", 200)
    # cam_buffer_size: camera buffer size → driver frame cache
    interface.set_parameter("cam_buffer_size", 8)
    # sens_ts: clock source(true=device clock/false=system clock) → driver timestamp
    interface.set_parameter("sens_ts", False)
    # camera_type: simulation camera type → driver camera config
    interface.set_parameter("camera_type", "usb")

    params = HexMujocoArcherY6Params(
        state_rate=interface.get_parameter("state_rate"),
        cam_rate=interface.get_parameter("cam_rate"),
        headless=interface.get_parameter("headless"),
        state_buffer_size=interface.get_parameter("state_buffer_size"),
        cam_buffer_size=interface.get_parameter("cam_buffer_size"),
        sens_ts=interface.get_parameter("sens_ts"),
        camera_type=interface.get_parameter("camera_type"),
    )

    # ============ publisher ============
    arm_state_pub = interface.create_publisher("arm_state", ArmState, 10)
    grip_state_pub = interface.create_publisher("grip_state", GripState, 10)
    pose_pub = interface.create_publisher("obj_pose", PoseStamped, 10)
    color_pub = interface.create_publisher("color", Image, 10)
    depth_pub = interface.create_publisher("depth", Image, 10)


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

    def color_img_cb(state):
        try:
            msg = Image()
            msg.header.stamp = interface.get_timestamp_from_ns(
                int(state["ts_ns"]))
            msg.header.frame_id = "camera_color_optical_frame"
            msg.height, msg.width = state["data"].shape[:2]
            msg.encoding = "bgr8"
            msg.is_bigendian = False
            msg.step = msg.width * 3
            msg.data = state["data"].tobytes()
            interface.publish(color_pub, msg)
        except Exception:
            traceback.print_exc()

    def depth_img_cb(state):
        try:
            msg = Image()
            msg.header.stamp = interface.get_timestamp_from_ns(
                int(state["ts_ns"]))
            msg.header.frame_id = "camera_depth_optical_frame"
            msg.height, msg.width = state["data"].shape[:2]
            msg.encoding = "16UC1"
            msg.is_bigendian = False
            msg.step = msg.width * 2
            msg.data = state["data"].tobytes()
            interface.publish(depth_pub, msg)
        except Exception:
            traceback.print_exc()

    # ============ driver ============
    sim = None
    
    try:
        sim = HexMujocoArcherY6Callback(params, callbacks={
            "arm_state": arm_state_cb,
            "grip_state": grip_state_cb,
            "obj_pose": obj_pose_cb,
            "color_img": color_img_cb,
            "depth_img": depth_img_cb,
        })

        def node_arm_ctrl_cb(msg):
            try:
                cmd = ros_ctrl_to_driver_cmd(msg, dof=6)
                mode = msg.ctrl_mode
                if mode == ArmCtrlMode.MIT:
                    sim.set_arm_mit_cmd(cmd)
                elif mode == ArmCtrlMode.COMP:
                    sim.set_arm_mit_comp_cmd(cmd)
                elif mode == ArmCtrlMode.POS:
                    sim.set_arm_pos_cmd(cmd)
                elif mode == ArmCtrlMode.POSE:
                    sim.set_arm_pose_cmd(cmd)
                elif mode == ArmCtrlMode.POS_PLAN:
                    sim.set_arm_pos_plan_cmd(cmd)
                elif mode == ArmCtrlMode.POSE_PLAN:
                    sim.set_arm_pose_plan_cmd(cmd)
            except Exception:
                traceback.print_exc()

        def node_grip_ctrl_cb(msg):
            try:
                cmd = ros_grip_ctrl_to_driver_cmd(msg, dof=1)
                mode = msg.ctrl_mode
                if mode == GripCtrlMode.MIT:
                    sim.set_grip_mit_cmd(cmd)
                elif mode == GripCtrlMode.COMP:
                    sim.set_grip_comp_cmd(cmd)
                elif mode == GripCtrlMode.POS:
                    sim.set_grip_pos_cmd(cmd)
                elif mode == GripCtrlMode.FORCE:
                    sim.set_grip_force_cmd(cmd)
            except Exception:
                traceback.print_exc()

        def node_reset_cb(msg):
            if msg.data:
                sim.reset()

        interface.create_subscription("arm_ctrl", ArmCtrl, node_arm_ctrl_cb, 10)
        interface.create_subscription("grip_ctrl", GripCtrl, node_grip_ctrl_cb, 10)
        interface.create_subscription("reset", Bool, node_reset_cb, 10)
        sim.start()

        while interface.ok():
            interface.sleep()
    except KeyboardInterrupt:
        pass
    finally:
        if sim:
            sim.stop()
        interface.shutdown()
