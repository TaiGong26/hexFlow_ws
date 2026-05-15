import traceback

import numpy as np
from hex_driver_robot import HexRobotHelloY6Callback, HexRobotHelloY6Params
from hex_flow_ros_common.interface import DataInterface
from hex_flow_ros_msg.msg import ArmState
from sensor_msgs.msg import Joy
from std_msgs.msg import Int32MultiArray


def main():
    ros_interface = DataInterface("robot_hello_y6", rate_hz=1.0)

    # ============ parameter ============
    # host: robot controller IP → HexRobotHelloY6Params → driver connection target
    ros_interface.set_parameter("host", "192.168.1.100")
    # port: robot controller port → driver connection target
    ros_interface.set_parameter("port", 8439)
    # ctrl_rate: control loop rate(Hz) → driver control loop
    ros_interface.set_parameter("ctrl_rate", 500.0)
    # state_buffer_size: state buffer size → driver state cache
    ros_interface.set_parameter("state_buffer_size", 200)
    # sens_ts: clock source(true=device clock/false=system clock) → driver timestamp
    ros_interface.set_parameter("sens_ts", False)
    # led_buffer_size: LED command buffer size → driver RGB LED control
    ros_interface.set_parameter("led_buffer_size", 10)
    # clock_source: timestamp clock source for published messages (ptp or ros)
    ros_interface.set_parameter("clock_source", "ptp")

    params = HexRobotHelloY6Params(
        host=ros_interface.get_parameter("host"),
        port=ros_interface.get_parameter("port"),
        ctrl_rate=ros_interface.get_parameter("ctrl_rate"),
        state_buffer_size=ros_interface.get_parameter("state_buffer_size"),
        sens_ts=ros_interface.get_parameter("sens_ts"),
        led_buffer_size=ros_interface.get_parameter("led_buffer_size"),
    )

    clock_source = ros_interface.get_parameter("clock_source")

    # ============ publisher ============
    arm_state_pub = ros_interface.create_publisher("arm_state", ArmState, 10)
    grip_joy_pub = ros_interface.create_publisher("grip_joy", Joy, 10)

    # ============ subscription callback ============
    def arm_state_cb(state):
        try:
            msg = ArmState()
            msg.stamp = ros_interface.get_clocksource_timestamp(clock_source)
            msg.jnt_pos = state["jnt_pos"].tolist()
            msg.jnt_vel = state["jnt_vel"].tolist()
            # jnt_eff intentionally omitted — Zenoh reference does not publish it
            ros_interface.publish(arm_state_pub, msg)
        except Exception as e:
            ros_interface.loge(f"publish arm state failed: {e}")

    def grip_joy_cb(state):
        try:
            msg = Joy()
            msg.header.stamp = ros_interface.get_clocksource_timestamp(clock_source)
            msg.axes = [
                float(state["trigger"]),
                float(state["axis_x"]),
                float(state["axis_y"]),
            ]
            msg.buttons = [
                int(state["btn_w"]),
                int(state["btn_x"]),
                int(state["btn_y"]),
                int(state["btn_z"]),
            ]
            ros_interface.publish(grip_joy_pub, msg)
        except Exception as e:
            ros_interface.loge(f"publish grip joy failed: {e}")

    robot = None
    # ============ driver ============
    try:
        robot = HexRobotHelloY6Callback(params, callbacks={
            "arm_state": arm_state_cb,
            "grip_joy": grip_joy_cb,
        })

        def node_grip_led_ctrl_cb(msg):
            try:
                data = msg.data
                ts = ros_interface.get_clocksource_timestamp(clock_source)
                cmd = {
                    "ts_ns": int(ts.sec * 1e9 + ts.nanosec),
                    "r": np.array(data[0:6], dtype=np.uint8),
                    "g": np.array(data[6:12], dtype=np.uint8),
                    "b": np.array(data[12:18], dtype=np.uint8),
                }
                robot.set_rgb_cmd(cmd)
            except Exception as e:
                ros_interface.loge(f"grip led ctrl failed: {e}")

        ros_interface.create_subscription("grip_led_ctrl", Int32MultiArray,
                                       node_grip_led_ctrl_cb, 10)
        robot.start()

        while ros_interface.ok():
            ros_interface.sleep()
    except KeyboardInterrupt:
        pass
    finally:
        if robot:
            robot.stop()
        ros_interface.shutdown()
