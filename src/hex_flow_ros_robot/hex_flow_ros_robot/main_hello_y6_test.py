import sys
import time
import traceback

import numpy as np
from hex_flow_ros_common.interface import DataInterface
from hex_flow_ros_msg.msg import ArmState
from sensor_msgs.msg import Joy
from std_msgs.msg import Int32MultiArray


_LED_CTRL_CMD = {
    "r": [255, 0, 0, 0, 0, 255],
    "g": [0, 255, 0, 0, 255, 0],
    "b": [0, 0, 255, 255, 0, 0],
}


def _show_state(arm_state, grip_joy, fps_info=""):
    lines = ["=== Hello Y6 Test ==="]
    if arm_state is not None:
        lines.append(f"  arm pos: {np.array2string(arm_state.jnt_pos, precision=3, suppress_small=True)}")
        lines.append(f"  arm vel: {np.array2string(arm_state.jnt_vel, precision=3, suppress_small=True)}")
    if grip_joy is not None:
        axes = grip_joy.axes
        if len(axes) >= 3:
            lines.append(f"  trigger: {axes[0]:.4f}")
            lines.append(f"  axis:    ({axes[1]:.4f}, {axes[2]:.4f})")
        btns = []
        btn_labels = ["w", "x", "y", "z"]
        for i, label in enumerate(btn_labels):
            if i < len(grip_joy.buttons) and grip_joy.buttons[i]:
                btns.append(f"btn_{label}")
        lines.append(f"  buttons: [{', '.join(btns)}]")
    if fps_info:
        lines.append(fps_info)
    output = "\033[H"
    for line in lines:
        output += line + "\033[K\n"
    output += "\033[J"
    print(output, end="", flush=True)


def main():
    interface = DataInterface("robot_hello_y6_test", rate_hz=10.0)

    # ============ parameter ============
    interface.set_parameter("rate_hz", 10.0)
    rate_hz = interface.get_parameter("rate_hz")

    # ============ subscription ============
    arm_state = None
    grip_joy = None

    def arm_state_cb(msg):
        nonlocal arm_state
        arm_state = msg

    def grip_joy_cb(msg):
        nonlocal grip_joy
        grip_joy = msg

    interface.create_subscription("arm_state", ArmState, arm_state_cb, 10)
    interface.create_subscription("grip_joy", Joy, grip_joy_cb, 10)

    # ============ publisher ============
    led_pub = interface.create_publisher("grip_led_ctrl", Int32MultiArray, 10)

    rate = interface.create_rate(rate_hz)
    fps_cnt, fps_start = 0, time.perf_counter_ns()
    fps_info = ""
    try:
        while interface.ok():
            rate.sleep()

            fps_cnt += 1
            if fps_cnt >= 1000:
                now = time.perf_counter_ns()
                fps_info = f"[hello_y6_test] arm_state fps={1e12 / (now - fps_start):.1f}"
                fps_cnt = 0
                fps_start = now

            led_msg = Int32MultiArray()
            led_msg.data = _LED_CTRL_CMD["r"] + _LED_CTRL_CMD["g"] + _LED_CTRL_CMD["b"]
            interface.publish(led_pub, led_msg)

            current_arm = arm_state
            current_grip = grip_joy
            _show_state(current_arm, current_grip, fps_info)

    except KeyboardInterrupt:
        pass
    finally:
        interface.shutdown()
