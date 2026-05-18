import threading
from collections import deque

import rclpy
from rclpy.node import Node as RosNode
from rclpy.time import Time
from hex_util_runtime import HexRate, get_env_float, ns_now, deque_helper

from .interface_base import InterfaceBase


class DataInterface(InterfaceBase):

    def __init__(self, name: str, rate_hz: float = 100.0):
        super().__init__(name)
        rclpy.init()
        self.__name = name
        self.__node = RosNode(name)
        self.__logger = self.__node.get_logger()

        self._rate_hz = rate_hz
        self._rate = self.__node.create_rate(self._rate_hz)

        self.__buffers: dict[str, deque] = {}

        self.__spin_thread = threading.Thread(target=self._spin, daemon=True)
        self.__spin_thread.start()

    # ---- Topic management ----

    def create_publisher(self, topic_name, msg_type, queue_size=10):
        return self.__node.create_publisher(msg_type, topic_name, queue_size)

    def create_subscription(self, topic_name, msg_type, callback, queue_size=10):
        return self.__node.create_subscription(
            msg_type, topic_name, callback, queue_size)

    def publish(self, publisher, msg):
        try:
            publisher.publish(msg)
        except Exception:
            pass

    # ---- Timer ----

    def create_timer(self, interval_sec, callback):
        return self.__node.create_timer(interval_sec, callback)

    # ---- Parameter server ----

    def get_parameter(self, name):
        return self.__node.get_parameter(name).value

    def set_parameter(self, name, value):
        self.__node.declare_parameter(name, value)

    # ---- Rate control ----

    def set_rate(self, hz):
        self._rate_hz = hz
        self._rate = self.__node.create_rate(self._rate_hz)

    def get_rate(self):
        return self._rate_hz

    def sleep(self):
        self._rate.sleep()

    # ---- Lifecycle ----

    def ok(self):
        return rclpy.ok()

    def shutdown(self):
        self.__node.destroy_node()
        if self.ok():
            rclpy.shutdown()    

    # ---- Logging ----

    def logd(self, msg, *args, **kwargs):
        self.__logger.debug(msg, *args, **kwargs)

    def logi(self, msg, *args, **kwargs):
        self.__logger.info(msg, *args, **kwargs)

    def logw(self, msg, *args, **kwargs):
        self.__logger.warning(msg, *args, **kwargs)

    def loge(self, msg, *args, **kwargs):
        self.__logger.error(msg, *args, **kwargs)

    def logf(self, msg, *args, **kwargs):
        self.__logger.fatal(msg, *args, **kwargs)

    # ---- Tools ----

    def get_timestamp(self):
        return self.__node.get_clock().now().to_msg()

    def get_timestamp_from_s_ns(self, s, ns):
        return Time(seconds=s, nanoseconds=ns).to_msg()

    def get_timestamp_from_ns(self, ns: int):
        return self.get_timestamp_from_s_ns(
            ns // 1_000_000_000, ns % 1_000_000_000)

    def get_clocksource_timestamp(self, source: str = "driver_timestamp",ts: float = None):
        """
        Get timestamp from specified clock source.

        Args:
            source: "driver_timestamp" for ns_now (Hex driver_timestamp clock), "ros" for rclpy Time

        Returns:
            Time message with nanoseconds from selected clock source
        """
        if source == "driver_timestamp":
            if ts == None:
                ns = ns_now()
            else:
                ns = ts
            return self.get_timestamp_from_ns(int(ns))
        
        else:  # "ros"
            return self.get_timestamp()

    # ---- Internal ----

    def _spin(self):
        try:
            rclpy.spin(self.__node)
        except Exception:
            pass

    def spin_once(self):
        rclpy.spin_once(self.__node)

    # ---- Buffered subscription (polling mode) ----

    def create_subscription_buffered(self, topic_name, msg_type,
                                     maxlen=10, queue_size=10):
        buffer = deque(maxlen=maxlen)
        self.__buffers[topic_name] = buffer

        def _callback(msg):
            buffer.append(msg)

        return self.create_subscription(topic_name, msg_type, _callback, queue_size)

    def get(self, topic_name, latest=False):
        buffer = self.__buffers.get(topic_name)
        if buffer is None:
            return None
        return deque_helper(buffer, latest)
