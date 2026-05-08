import os
import select
import threading
import traceback

from evdev import InputDevice, ecodes, list_devices
from hex_flow_ros.interface import DataInterface
from sensor_msgs.msg import Joy

_LETTER_CODES = [
    getattr(ecodes, f"KEY_{chr(c)}") for c in range(ord('A'), ord('Z') + 1)
]
_LETTER_NAMES = [chr(c) for c in range(ord('a'), ord('z') + 1)]
_LETTER_MAP = dict(zip(_LETTER_CODES, _LETTER_NAMES))


def find_keyboards():
    keyboards = []
    for path in list_devices():
        dev = InputDevice(path)
        caps = dev.capabilities(absinfo=False)
        if ecodes.EV_KEY in caps and ecodes.KEY_A in caps[ecodes.EV_KEY]:
            print(f"[keyboard] found: {dev.path} {dev.name}")
            keyboards.append(dev)
    return keyboards


class KeyboardStateReader:

    def __init__(self, devices):
        self._devices = devices
        self._state = {name: 0 for name in _LETTER_NAMES}
        self._lock = threading.Lock()
        self._running = False

    def start(self):
        self._running = True
        for dev in self._devices:
            t = threading.Thread(target=self._read_loop,
                                 args=(dev,), daemon=True)
            t.start()

    def stop(self):
        self._running = False

    def _read_loop(self, dev):
        while self._running:
            r, _, _ = select.select([dev.fd], [], [], 0.01)
            if not r:
                continue
            try:
                for event in dev.read():
                    if event.type == ecodes.EV_KEY and event.code in _LETTER_MAP:
                        with self._lock:
                            self._state[_LETTER_MAP[
                                event.code]] = 0 if event.value == 0 else 1
            except OSError:
                break

    def get_state(self):
        with self._lock:
            return self._state.copy()


def main():
    interface = DataInterface("teleop_keyboard", rate_hz=100.0)
    interface.set_parameter("device_path", "")

    device_path = interface.get_parameter("device_path")
    if device_path:
        devices = [InputDevice(device_path)]
        print(f"[keyboard] using: {devices[0].path} {devices[0].name}")
    else:
        devices = find_keyboards()

    if not devices:
        print("[keyboard] no keyboard device found")
        print(("[keyboard] This may be caused by permission denied when "
               "accessing /dev/input/*\n"
               "[keyboard] Please add your user to the 'input' group and re-login:\n"
               "[keyboard]   sudo usermod -aG input $USER"))
        interface.shutdown()
        return

    kb_pub = interface.create_publisher("keyboard", Joy, 10)

    reader = KeyboardStateReader(devices)
    reader.start()

    try:
        while interface.ok():
            interface.sleep()
            state = reader.get_state()
            msg = Joy()
            msg.buttons = [state[name] for name in _LETTER_NAMES]
            interface.publish(kb_pub, msg)
    except KeyboardInterrupt:
        pass
    finally:
        reader.stop()
        interface.shutdown()
