import os
import select
import threading
import traceback

from evdev import InputDevice, ecodes, list_devices
from hex_flow_ros_common.interface import DataInterface
from sensor_msgs.msg import Joy

# 标准名称 -> Joy 消息数组索引的映射
_BTN_NAME_TO_INDEX = {
    'BTN_X': 0,
    'BTN_Y': 1,
    'BTN_A': 2,
    'BTN_B': 3,
    'BTN_TL': 4,
    'BTN_TR': 5,
    'BTN_TL2': 6,
    'BTN_TR2': 7,
    'BTN_THUMBL': 8,
    'BTN_THUMBR': 9,
}

_AXIS_NAME_TO_INDEX = {
    'ABS_X': 0,
    'ABS_Y': 1,
    'ABS_RX': 2,
    'ABS_RY': 3,
    'ABS_Z': 4,
    'ABS_RZ': 5,
    'ABS_HAT0X': 6,
    'ABS_HAT0Y': 7,
}

def _has_joystick_buttons(caps):
    """Check if the device has joystick/gamepad buttons (0x120-0x13f)."""
    key_codes = caps.get(ecodes.EV_KEY, [])
    return any(0x120 <= code <= 0x13f for code in key_codes)


def find_joysticks():
    """Find joystick / gamepad devices.

    Prefer devices that have both ABS axes and joystick/gamepad buttons.
    Fall back to any ABS_X/ABS_Y device only if no real gamepad is found.
    """
    gamepads = []
    fallback = []
    for path in list_devices():
        dev = InputDevice(path)
        caps = dev.capabilities(absinfo=False)
        if ecodes.EV_ABS not in caps:
            continue
        abs_codes = caps[ecodes.EV_ABS]
        if ecodes.ABS_X not in abs_codes and ecodes.ABS_Y not in abs_codes:
            continue
        if _has_joystick_buttons(caps):
            print(f"[joystick] found gamepad: {dev.path} {dev.name}")
            gamepads.append(dev)
        else:
            print(f"[joystick] found candidate: {dev.path} {dev.name}")
            fallback.append(dev)

    return gamepads if gamepads else fallback


def _resolve_name(raw_name):
    """解析 name，可能为 str/list/tuple，找到在 map 中存在的那个"""
    if raw_name is None:
        return None
    if isinstance(raw_name, (list, tuple)):
        for n in raw_name:
            if n in _AXIS_NAME_TO_INDEX or n in _BTN_NAME_TO_INDEX:
                return n
        return None
    return raw_name if isinstance(raw_name, str) else None


class JoystickStateReader:

    def __init__(self, device):
        self._device = device
        self._btns = [0] * len(_BTN_NAME_TO_INDEX)
        self._axes = [0.0] * len(_AXIS_NAME_TO_INDEX)
        self._lock = threading.Lock()
        self._running = False
        self._set_view_test = False

        # 动态检测：建立 code -> 索引的映射
        self._code_to_btn_idx = {}
        self._code_to_axis_idx = {}
        self._axis_info = {}

        key_types = ecodes.bytype.get(ecodes.EV_KEY, {})
        abs_types = ecodes.bytype.get(ecodes.EV_ABS, {})

        # 按钮：获取 device 报告的 code，映射到标准名称，再查 map 得索引
        caps_simple = device.capabilities(absinfo=False)
        for code in caps_simple.get(ecodes.EV_KEY, []):
            raw_name = key_types.get(code)
            name = _resolve_name(raw_name)
            if name and name in _BTN_NAME_TO_INDEX:
                self._code_to_btn_idx[code] = _BTN_NAME_TO_INDEX[name]

        # 轴：同上，并缓存 absinfo
        caps_abs = device.capabilities(absinfo=True)
        for code, absinfo in caps_abs.get(ecodes.EV_ABS, []):
            raw_name = abs_types.get(code)
            name = _resolve_name(raw_name)
            if name and name in _AXIS_NAME_TO_INDEX:
                self._code_to_axis_idx[code] = _AXIS_NAME_TO_INDEX[name]
                self._axis_info[code] = absinfo

    def start(self):
        self._running = True
        t = threading.Thread(target=self._read_loop, daemon=True)
        t.start()

    def stop(self):
        self._running = False

    @staticmethod
    def _normalize(value, absinfo):
        lo, hi = absinfo.min, absinfo.max
        if hi == lo:
            return 0.0
        return 2.0 * (value - lo) / (hi - lo) - 1.0

    def _read_loop(self):
        while self._running:
            r, _, _ = select.select([self._device.fd], [], [], 0.01)
            if not r:
                continue
            try:
                for event in self._device.read():
                    if event.type == ecodes.EV_KEY and event.code in self._code_to_btn_idx:
                        with self._lock:
                            self._btns[self._code_to_btn_idx[event.code]] = event.value

                    elif event.type == ecodes.EV_ABS and event.code in self._code_to_axis_idx:
                        with self._lock:
                            absinfo = self._axis_info.get(event.code)
                            if absinfo and absinfo.max != absinfo.min:
                                self._axes[self._code_to_axis_idx[event.code]] = self._normalize(event.value, absinfo)
                    if self._set_view_test:
                        if event.type == ecodes.EV_KEY and event.value == 1:
                            name = ecodes.bytype[ecodes.EV_KEY].get(event.code, "UNKNOWN")
                            print(f"[KEY PRESS] code={event.code}, name={name}, value={event.value}")

                        if event.type == ecodes.EV_ABS:
                            name = ecodes.bytype[ecodes.EV_ABS].get(event.code, "UNKNOWN")
                            print(f"[AXIS MOVE] code={event.code}, name={name}, value={event.value}")
            except OSError:
                break

    def get_buttons(self):
        with self._lock:
            return list(self._btns)

    def get_axes(self):
        with self._lock:
            return list(self._axes)

    def set_view(self, enable=True):
            self._set_view_test = enable


def main():
    interface = DataInterface("teleop_joystick", rate_hz=100.0)
    interface.set_parameter("device_path", "")
    interface.set_parameter("xbox_view_test", False)

    device_path = interface.get_parameter("device_path")
    if device_path:
        devices = [InputDevice(device_path)]
        print(f"[joystick] using: {devices[0].path} {devices[0].name}")
    else:
        devices = find_joysticks()

    if not devices:
        print("[joystick] no joystick device found")
        interface.shutdown()
        return

    joy_pub = interface.create_publisher("joy", Joy, 10)

    device = devices[0]
    reader = JoystickStateReader(device)
    reader.start()
    reader.set_view(interface.get_parameter("xbox_view_test"))
    try:
        while interface.ok():
            interface.sleep()
            msg = Joy()
            msg.buttons = reader.get_buttons()
            msg.axes = reader.get_axes()
            interface.publish(joy_pub, msg)
    except KeyboardInterrupt:
        pass
    finally:
        reader.stop()
        interface.shutdown()

