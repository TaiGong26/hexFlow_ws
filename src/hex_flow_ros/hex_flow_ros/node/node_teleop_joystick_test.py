import sys
import time
import traceback

from hex_flow_ros.interface import DataInterface
from sensor_msgs.msg import Joy


def main():
    interface = DataInterface("teleop_joystick_test", rate_hz=10.0)

    # ============ parameter ============
    interface.set_parameter("rate_hz", 10.0)

    def joy_cb(msg):
        output = f"\033[H=== Joystick Test ===\033[K\n"
        output += f"  buttons: {msg.buttons}\033[K\n"
        axes_str = ", ".join(f"{a:7.3f}" for a in msg.axes)
        output += f"  axes:    [{axes_str}]\033[K\n"
        output += "\033[J"
        print(output, end="", flush=True)

    interface.create_subscription("joy", Joy, joy_cb, 10)

    try:
        while interface.ok():
            interface.sleep()
    except KeyboardInterrupt:
        pass
    finally:
        interface.shutdown()
