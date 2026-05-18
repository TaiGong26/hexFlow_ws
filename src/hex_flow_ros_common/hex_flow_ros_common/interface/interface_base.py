from abc import ABC, abstractmethod
from collections import deque
from typing import Callable, Optional, Any


class InterfaceBase(ABC):

    def __init__(self, name: str):
        self._name = name

    # ---- Topic management ----

    @abstractmethod
    def create_publisher(self, topic_name: str, msg_type: type, queue_size: int = 10):
        pass

    @abstractmethod
    def create_subscription(self, topic_name: str, msg_type: type,
                            callback: Callable, queue_size: int = 10):
        pass

    @abstractmethod
    def publish(self, publisher, msg):
        pass

    # ---- Timer ----

    @abstractmethod
    def create_timer(self, interval_sec: float, callback: Callable):
        pass

    # ---- Parameter server ----

    @abstractmethod
    def get_parameter(self, name: str):
        pass

    @abstractmethod
    def set_parameter(self, name: str, value):
        pass

    # ---- Rate control ----

    @abstractmethod
    def set_rate(self, hz: float):
        pass

    @abstractmethod
    def get_rate(self) -> float:
        pass

    @abstractmethod
    def sleep(self):
        pass

    # ---- Lifecycle ----

    @abstractmethod
    def ok(self) -> bool:
        pass

    @abstractmethod
    def shutdown(self):
        pass

    # ---- Logging ----

    @abstractmethod
    def logd(self, msg: str, *args, **kwargs):
        pass

    @abstractmethod
    def logi(self, msg: str, *args, **kwargs):
        pass

    @abstractmethod
    def logw(self, msg: str, *args, **kwargs):
        pass

    @abstractmethod
    def loge(self, msg: str, *args, **kwargs):
        pass

    @abstractmethod
    def logf(self, msg: str, *args, **kwargs):
        pass

    # ---- Tools ----

    @abstractmethod
    def get_timestamp(self):
        pass

    @abstractmethod
    def get_clocksource_timestamp(self, source: str = "driver_timestamp"):
        pass

    # ---- Buffered subscription (polling mode) ----

    @abstractmethod
    def create_subscription_buffered(
        self, topic_name: str, msg_type: type,
        maxlen: int = 10, queue_size: int = 10,
    ):
        pass

    @abstractmethod
    def get(self, topic_name: str, latest: bool = False):
        pass
