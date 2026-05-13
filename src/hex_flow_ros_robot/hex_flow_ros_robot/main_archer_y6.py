import traceback

import numpy as np
from hex_driver_robot import HexRobotArcherY6Callback, HexRobotArcherY6Params
from hex_flow_ros_common.interface import DataInterface
from hex_flow_ros_common.ctrl_mode import ArmCtrlMode, GripCtrlMode
from hex_flow_ros_common.msg_convert import ros_ctrl_to_driver_cmd, ros_grip_ctrl_to_driver_cmd
from hex_flow_ros_msg.msg import ArmState, ArmCtrl, GripState, GripCtrl


def main():
    interface = DataInterface("robot_archer_y6", rate_hz=1.0)

    # ============ parameter ============
    # host: robot controller IP → HexRobotArcherY6Params → driver connection target
    interface.set_parameter("host", "192.168.1.100")
    # port: robot controller port → driver connection target
    interface.set_parameter("port", 8439)
    # ctrl_rate: control loop rate(Hz) → driver control loop
    interface.set_parameter("ctrl_rate", 500.0)
    # state_buffer_size: state buffer size → driver state cache
    interface.set_parameter("state_buffer_size", 200)
    # sens_ts: clock source(true=device clock/false=system clock) → driver timestamp
    interface.set_parameter("sens_ts", False)
    # grip_type: gripper type → driver gripper config
    interface.set_parameter("grip_type", "gp80")
    # pose_end_in_flange: end-effector pose relative to flange → driver kinematics
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

    # ============ publisher ============
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
        except Exception as e:
            interface.loge(f"publish arm state failed: {e}")

    def grip_state_cb(state):
        try:
            msg = GripState()
            msg.stamp = interface.get_timestamp_from_ns(int(state["ts_ns"]))
            msg.jnt_pos = state["jnt_pos"].tolist()
            msg.jnt_vel = state["jnt_vel"].tolist()
            msg.jnt_eff = state["jnt_eff"].tolist()
            interface.publish(grip_state_pub, msg)
        except Exception as e:
            interface.loge(f"publish grip state failed: {e}")

    # ============ driver ============
    try:
        robot = HexRobotArcherY6Callback(params, callbacks={
            "arm_state": arm_state_cb,
            "grip_state": grip_state_cb,
        })

        def node_arm_ctrl_cb(msg):
            try:
                cmd = ros_ctrl_to_driver_cmd(msg, dof=6)
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
            except Exception as e:
                interface.loge(f"arm ctrl failed: {e}")

        def node_grip_ctrl_cb(msg):
            try:
                cmd = ros_grip_ctrl_to_driver_cmd(msg, dof=1)
                mode = msg.ctrl_mode
                if mode == GripCtrlMode.MIT:
                    robot.set_grip_mit_cmd(cmd)
                elif mode == GripCtrlMode.COMP:
                    robot.set_grip_comp_cmd(cmd)
                elif mode == GripCtrlMode.POS:
                    robot.set_grip_pos_cmd(cmd)
                elif mode == GripCtrlMode.FORCE:
                    robot.set_grip_force_cmd(cmd)
            except Exception as e:
                interface.loge(f"grip ctrl failed: {e}")

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
