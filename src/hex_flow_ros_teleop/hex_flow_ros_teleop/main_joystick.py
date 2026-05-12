import os
import select
import threading
import traceback

from evdev import InputDevice, ecodes, list_devices
from hex_flow_ros_common.interface import DataInterface
from sensor_msgs.msg import Joy

_BTN_MAP = {
    ecodes.BTN_X: 0,
    ecodes.BTN_Y: 1,
    ecodes.BTN_A: 2,
    ecodes.BTN_B: 3,
    ecodes.BTN_TL: 4,
    ecodes.BTN_TR: 5,
    ecodes.BTN_TL2: 6,
    ecodes.BTN_TR2: 7,
    ecodes.BTN_THUMBL: 8,
    ecodes.BTN_THUMBR: 9,
}

_AXIS_MAP = {
    ecodes.ABS_X: 0,
    ecodes.ABS_Y: 1,
    ecodes.ABS_RX: 2,
    ecodes.ABS_RY: 3,
    ecodes.ABS_Z: 4,
    ecodes.ABS_RZ: 5,
    ecodes.ABS_HAT0X: 6,
    ecodes.ABS_HAT0Y: 7,
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


class JoystickStateReader:

    def __init__(self, device):
        self._device = device
        self._btns = [0] * len(_BTN_MAP)
        self._axes = [0.0] * len(_AXIS_MAP)
        self._lock = threading.Lock()
        self._running = False
        self._set_view_test = False

    def start(self):
        self._running = True
        t = threading.Thread(target=self._read_loop, daemon=True)
        t.start()

    def stop(self):
        self._running = False

    def _read_loop(self):
        while self._running:
            r, _, _ = select.select([self._device.fd], [], [], 0.01)
            if not r:
                continue
            try:
                for event in self._device.read():
                    if event.type == ecodes.EV_KEY and event.code in _BTN_MAP:
                        with self._lock:
                            self._btns[_BTN_MAP[event.code]] = event.value

                    elif event.type == ecodes.EV_ABS and event.code in _AXIS_MAP:
                        with self._lock:
                            val = event.value
                            absinfo = self._device.absinfo(event.code)
                            if absinfo and absinfo.max != absinfo.min:
                                self._axes[_AXIS_MAP[event.code]] = (
                                    2.0 * (val - absinfo.min)
                                    / (absinfo.max - absinfo.min) - 1.0
                                )
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
