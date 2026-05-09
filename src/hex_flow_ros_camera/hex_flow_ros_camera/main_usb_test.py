import time
import traceback

import cv2
from cv_bridge import CvBridge
from hex_flow_ros_common.interface import DataInterface
from sensor_msgs.msg import Image


def main():
    interface = DataInterface("cam_usb_test", rate_hz=30.0)

    # ============ parameter ============
    interface.set_parameter("rate_hz", 30.0)

    bridge = CvBridge()

    def color_cb(msg):
        try:
            cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding="bgr8")
            cv2.imshow("USB Camera - Color", cv_image)
            cv2.waitKey(1)
        except Exception:
            traceback.print_exc()

    interface.create_subscription("color", Image, color_cb, 10)

    try:
        while interface.ok():
            interface.sleep()
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        interface.shutdown()
