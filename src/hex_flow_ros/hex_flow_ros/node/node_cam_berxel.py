import traceback

from hex_driver_camera import HexCamBerxelCallback, HexCamBerxelParams
from hex_flow_ros.interface import DataInterface
from sensor_msgs.msg import Image


def main():
    interface = DataInterface("cam_berxel", rate_hz=500.0)

    # ============ parameter ============
    # frame_rate: camera frame rate(Hz) → HexCamBerxelParams → driver output rate
    interface.set_parameter("frame_rate", 30)
    # height: image height(px) → driver resolution config
    interface.set_parameter("height", 400)
    # width: image width(px) → driver resolution config
    interface.set_parameter("width", 640)
    # cam_buffer_size: camera buffer size → driver frame cache
    interface.set_parameter("cam_buffer_size", 8)
    # sens_ts: clock source(true=device clock/false=system clock) → driver timestamp
    interface.set_parameter("sens_ts", False)
    # serial_number: device serial number(empty=auto select) → driver device selection
    interface.set_parameter("serial_number", "")
    # exposure: exposure value → driver camera exposure config
    interface.set_parameter("exposure", 10000)
    # gain: gain value → driver camera gain config
    interface.set_parameter("gain", 100)
    # color_encoding: color image encoding format → driver encoding config
    interface.set_parameter("color_encoding", "bgr8")
    # depth_encoding: depth image encoding format → driver encoding config
    interface.set_parameter("depth_encoding", "mono16")

    params = HexCamBerxelParams(
        frame_rate=interface.get_parameter("frame_rate"),
        height=interface.get_parameter("height"),
        width=interface.get_parameter("width"),
        cam_buffer_size=interface.get_parameter("cam_buffer_size"),
        sens_ts=interface.get_parameter("sens_ts"),
        serial_number=interface.get_parameter("serial_number"),
        exposure=interface.get_parameter("exposure"),
        gain=interface.get_parameter("gain"),
    )
    color_encoding = interface.get_parameter("color_encoding")
    depth_encoding = interface.get_parameter("depth_encoding")

    # ============ publisher ============
    color_pub = interface.create_publisher("color", Image, 10)
    depth_pub = interface.create_publisher("depth", Image, 10)

    def color_cb(state):
        try:
            msg = Image()
            msg.header.stamp = interface.get_timestamp_from_ns(
                int(state["ts_ns"]))
            msg.header.frame_id = "camera_color_optical_frame"
            msg.height, msg.width = state["data"].shape[:2]
            msg.encoding = color_encoding
            msg.is_bigendian = False
            msg.step = msg.width * (3 if color_encoding == "bgr8" else 1)
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
            msg.encoding = depth_encoding
            msg.is_bigendian = False
            msg.step = msg.width * 2
            msg.data = state["data"].tobytes()
            interface.publish(depth_pub, msg)
        except Exception:
            traceback.print_exc()

    # ============ driver ============
    cam = None
    try:
        cam = HexCamBerxelCallback(params, callbacks={
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
