import traceback

from hex_driver_camera import HexCamUsbCallback, HexCamUsbParams
from hex_flow_ros_common.interface import DataInterface
from sensor_msgs.msg import Image


def main():
    ros_interface = DataInterface("cam_usb", rate_hz=500.0)

    # ============ parameter ============
    # frame_rate: camera frame rate(Hz) → HexCamUsbParams → driver output rate
    ros_interface.set_parameter("frame_rate", 30)
    # height: image height(px) → driver resolution config
    ros_interface.set_parameter("height", 480)
    # width: image width(px) → driver resolution config
    ros_interface.set_parameter("width", 640)
    # cam_buffer_size: camera buffer size → driver frame cache
    ros_interface.set_parameter("cam_buffer_size", 8)
    # sens_ts: clock source(true=device clock/false=system clock) → driver timestamp
    ros_interface.set_parameter("sens_ts", False)
    # cam_path: camera device path → driver device selection
    ros_interface.set_parameter("cam_path", "/dev/video0")
    # exposure: exposure value → driver camera exposure config
    ros_interface.set_parameter("exposure", 100)
    # temperature: color temperature → driver white balance config
    ros_interface.set_parameter("temperature", 4000)
    # color_encoding: color image encoding format → driver encoding config
    ros_interface.set_parameter("color_encoding", "bgr8")
    # clock_source: timestamp clock source for published messages (ptp or ros)
    ros_interface.set_parameter("clock_source", "ptp")

    params = HexCamUsbParams(
        frame_rate=ros_interface.get_parameter("frame_rate"),
        height=ros_interface.get_parameter("height"),
        width=ros_interface.get_parameter("width"),
        cam_buffer_size=ros_interface.get_parameter("cam_buffer_size"),
        sens_ts=ros_interface.get_parameter("sens_ts"),
        cam_path=ros_interface.get_parameter("cam_path"),
        exposure=ros_interface.get_parameter("exposure"),
        temperature=ros_interface.get_parameter("temperature"),
    )
    color_encoding = ros_interface.get_parameter("color_encoding")

    clock_source = ros_interface.get_parameter("clock_source")

    # ============ publisher ============
    color_pub = ros_interface.create_publisher("color", Image, 10)

    def color_cb(state):
        try:
            msg = Image()
            msg.header.stamp = ros_interface.get_clocksource_timestamp(clock_source)
            msg.header.frame_id = "camera_color_optical_frame"
            msg.height, msg.width = state["data"].shape[:2]
            msg.encoding = color_encoding
            msg.is_bigendian = False
            msg.step = msg.width * (3 if color_encoding == "bgr8" else 1)
            msg.data = state["data"].tobytes()
            ros_interface.publish(color_pub, msg)
        except Exception:
            traceback.print_exc()

    # ============ driver ============
    cam = None
    try:
        cam = HexCamUsbCallback(params, callbacks={"color": color_cb})
        cam.start()

        while ros_interface.ok():
            ros_interface.sleep()
    except KeyboardInterrupt:
        pass
    if cam:
        cam.stop()
    ros_interface.shutdown()
