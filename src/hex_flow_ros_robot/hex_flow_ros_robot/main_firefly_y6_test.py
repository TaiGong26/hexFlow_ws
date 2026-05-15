import time
import traceback

import numpy as np
from hex_flow_ros_common.interface import DataInterface
from hex_flow_ros_common.ctrl_mode import ArmCtrlMode
from hex_flow_ros_common.msg_convert import ros_ctrl_to_driver_cmd
from hex_flow_ros_msg.msg import ArmState, ArmCtrl, GripState


_ARM_CTRL_MODES = {
    "pos": ArmCtrlMode.POS,
    "mit": ArmCtrlMode.MIT,
    "pose": ArmCtrlMode.POSE,
}


def _show_state(arm_state, grip_state, fps_info=""):
    lines = ["=== Robot Firefly Y6 Test ==="]
    if arm_state is not None:
        lines.append(f"  arm jnt_pos: {np.array2string(arm_state.jnt_pos, precision=3, suppress_small=True)}")
        lines.append(f"  arm jnt_vel: {np.array2string(arm_state.jnt_vel, precision=3, suppress_small=True)}")
    if grip_state is not None:
        lines.append(f"  grip jnt_pos: {np.array2string(grip_state.jnt_pos, precision=3, suppress_small=True)}")
    if fps_info:
        lines.append(fps_info)
    output = "\033[H"
    for line in lines:
        output += line + "\033[K\n"
    output += "\033[J"
    print(output, end="", flush=True)


def main():
    ros_interface = DataInterface("robot_firefly_y6_test", rate_hz=100.0)

    # ============ parameter ============
    ros_interface.set_parameter("rate_hz", 100.0)
    ros_interface.set_parameter("arm_ctrl_mode", "pos")

    ctrl_mode_name = ros_interface.get_parameter("arm_ctrl_mode")
    rate_hz = ros_interface.get_parameter("rate_hz")

    # ============ subscription ============
    arm_state = None
    grip_state = None

    def arm_state_cb(msg):
        nonlocal arm_state
        arm_state = msg

    def grip_state_cb(msg):
        nonlocal grip_state
        grip_state = msg

    ros_interface.create_subscription("arm_state", ArmState, arm_state_cb, 10)
    ros_interface.create_subscription("grip_state", GripState, grip_state_cb, 10)

    # ============ publisher ============
    arm_ctrl_pub = ros_interface.create_publisher("arm_ctrl", ArmCtrl, 10)

    ctrl_mode = _ARM_CTRL_MODES.get(ctrl_mode_name, ArmCtrlMode.POS)

    ros_interface.set_rate(rate_hz)
    fps_cnt, fps_start = 0, time.perf_counter_ns()
    fps_info = ""
    try:
        while ros_interface.ok():
            ros_interface.sleep()

            fps_cnt += 1
            if fps_cnt >= 100:
                now = time.perf_counter_ns()
                fps_info = f"[test] fps={1e12 / (now - fps_start):.1f}"
                fps_cnt = 0
                fps_start = now

            ctrl = ArmCtrl()
            ctrl.stamp = ros_interface.get_timestamp()
            ctrl.ctrl_mode = ctrl_mode
            ctrl.jnt_pos = [0.0, -1.5, 3.0, 0.07, 0.0, 0.0]
            ctrl.mit_kp = [50.0] * 6
            ctrl.mit_kd = [2.0] * 6
            ctrl.lim_err = 0.02
            ros_interface.publish(arm_ctrl_pub, ctrl)

            current_arm = arm_state
            current_grip = grip_state
            _show_state(current_arm, current_grip, fps_info)

    except KeyboardInterrupt:
        pass
    finally:
        ros_interface.shutdown()
