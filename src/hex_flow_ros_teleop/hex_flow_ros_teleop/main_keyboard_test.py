import sys
import time
import traceback

from hex_flow_ros_common.interface import DataInterface
from sensor_msgs.msg import Joy


def main():
    ros_interface = DataInterface("teleop_keyboard_test", rate_hz=10.0)

    # ============ parameter ============
    ros_interface.set_parameter("rate_hz", 10.0)

    _LETTER_NAMES = [chr(c) for c in range(ord('a'), ord('z') + 1)]

    def kb_cb(msg):
        pressed = [name for name, val in zip(_LETTER_NAMES, msg.buttons) if val]
        output = f"\033[H=== Keyboard Test ===\033[K\n"
        output += f"  pressed: {pressed}\033[K\n"
        output += f"  buttons: {msg.buttons}\033[K\n"
        output += "\033[J"
        print(output, end="", flush=True)

    ros_interface.create_subscription("keyboard", Joy, kb_cb, 10)

    try:
        while ros_interface.ok():
            ros_interface.sleep()
    except KeyboardInterrupt:
        pass
    finally:
        ros_interface.shutdown()
