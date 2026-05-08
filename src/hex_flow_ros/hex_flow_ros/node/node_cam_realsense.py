import traceback

from hex_driver_camera import HexCamRealsenseCallback, HexCamRealsenseParams
from hex_flow_ros.interface import DataInterface
from sensor_msgs.msg import Image


def main():
    interface = DataInterface("cam_realsense", rate_hz=500.0)

    interface.set_parameter("frame_rate", 30)
    interface.set_parameter("height", 480)
    interface.set_parameter("width", 640)
    interface.set_parameter("cam_buffer_size", 8)
    interface.set_parameter("sens_ts", False)
    interface.set_parameter("serial_number", "")

    params = HexCamRealsenseParams(
        frame_rate=interface.get_parameter("frame_rate"),
        height=interface.get_parameter("height"),
        width=interface.get_parameter("width"),
        cam_buffer_size=interface.get_parameter("cam_buffer_size"),
        sens_ts=interface.get_parameter("sens_ts"),
        serial_number=interface.get_parameter("serial_number"),
    )

    color_pub = interface.create_publisher("color", Image, 10)
    depth_pub = interface.create_publisher("depth", Image, 10)

    def color_cb(state):
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

    def depth_cb(state):
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

    cam = None
    try:
        cam = HexCamRealsenseCallback(params, callbacks={
            "color": color_cb,
            "depth": depth_cb,
        })
        cam.start()

        while interface.ok():
            interface.sleep()
    except KeyboardInterrupt:
        pass
    finally:
        if cam:
            cam.stop()
        interface.shutdown()
