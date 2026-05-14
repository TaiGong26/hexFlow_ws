import time
import traceback

import numpy as np
import cv2
from cv_bridge import CvBridge
from hex_flow_ros_common.interface import DataInterface
from sensor_msgs.msg import Image
from hex_util_robot import depth_to_cmap


def main():
    interface = DataInterface("cam_berxel_test", rate_hz=30.0)

    # ============ parameter ============
    interface.set_parameter("rate_hz", 30.0)

    bridge = CvBridge()

    def color_cb(msg):
        try:
            cv_image = bridge.imgmsg_to_cv2(msg, desired_encoding=msg.encoding)
            cv2.imshow("Berxel Camera - Color", cv_image)
            cv2.waitKey(1)
        except Exception:
            traceback.print_exc()

    def depth_cb(msg):
        try:
            frame = bridge.imgmsg_to_cv2(msg, desired_encoding=msg.encoding)
            depth_cmap = depth_to_cmap(np.asarray(frame.data))
            cv2.imshow("Berxel Camera - Depth", depth_cmap)
            cv2.waitKey(1)
        except Exception:
            traceback.print_exc()

    interface.create_subscription("color", Image, color_cb, 10)
    interface.create_subscription("depth", Image, depth_cb, 10)

    try:
        while interface.ok():
            interface.sleep()
    except KeyboardInterrupt:
        pass
    finally:
        cv2.destroyAllWindows()
        interface.shutdown()
