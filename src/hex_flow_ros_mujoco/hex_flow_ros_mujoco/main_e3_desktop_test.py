import time
import traceback

import numpy as np
from hex_flow_ros_common.interface import DataInterface
from hex_flow_ros_common.ctrl_mode import ArmCtrlMode
from hex_flow_ros_common.msg_convert import ros_ctrl_to_driver_cmd
from hex_flow_ros_msg.msg import ArmState, ArmCtrl


def _show_state(states, fps_info=""):
    lines = ["=== Mujoco E3 Desktop Test ==="]
    for side in ("left", "right"):
        s = states.get(side)
        if s is not None:
            lines.append(f"  {side} jnt_pos: {np.array2string(s.jnt_pos, precision=3, suppress_small=True)}")
    if fps_info:
        lines.append(fps_info)
    output = "\033[H"
    for line in lines:
        output += line + "\033[K\n"
    output += "\033[J"
    print(output, end="", flush=True)


def main():
    ros_interface = DataInterface("mujoco_e3_desktop_test", rate_hz=100.0)

    # ============ parameter ============
    ros_interface.set_parameter("rate_hz", 100.0)
    ros_interface.set_parameter("arm_ctrl_mode", "pos")
    ros_interface.set_parameter("clock_source", "driver_timestamp")

    ctrl_mode_name = ros_interface.get_parameter("arm_ctrl_mode")
    rate_hz = ros_interface.get_parameter("rate_hz")
    clock_source = ros_interface.get_parameter("clock_source")

    states = {}

    for side in ("left", "right"):
        def make_cb(s):
            def cb(msg):
                states[s] = msg
            return cb
        ros_interface.create_subscription(f"{side}_arm_state", ArmState, make_cb(side), 10)

    arm_ctrl_pubs = {}
    for side in ("left", "right"):
        arm_ctrl_pubs[side] = ros_interface.create_publisher(f"{side}_arm_ctrl", ArmCtrl, 10)

    ctrl_mode = ArmCtrlMode.POS

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

            for side in ("left", "right"):
                ctrl = ArmCtrl()
                ctrl.stamp = ros_interface.get_clocksource_timestamp(clock_source)
                ctrl.ctrl_mode = ctrl_mode
                ctrl.jnt_pos = [0.0, -1.5, 3.0, 0.07, 0.0, 0.0]
                ctrl.mit_kp = [50.0] * 6
                ctrl.mit_kd = [2.0] * 6
                ctrl.lim_err = 0.02
                ros_interface.publish(arm_ctrl_pubs[side], ctrl)

            _show_state(states, fps_info)

    except KeyboardInterrupt:
        pass
    finally:
        ros_interface.shutdown()
