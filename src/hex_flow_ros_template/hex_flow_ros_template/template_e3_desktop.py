import threading
import traceback

import numpy as np
from hex_flow_ros_common.interface import DataInterface
from hex_flow_ros_common.ctrl_mode import ArmCtrlMode, GripCtrlMode
from hex_flow_ros_msg.msg import ArmState, ArmCtrl, GripState, GripCtrl
from sensor_msgs.msg import Joy

_ARM_HOME_CFG = {
    "stable_pos": [0.0, -1.5, 3.0, 0.07, 0.0, 0.0],
    "kp": [200.0, 200.0, 250.0, 150.0, 100.0, 100.0],
    "kd": [5.0, 5.0, 5.0, 5.0, 2.0, 2.0],
    "lim_err": 0.02,
    "arrive_threshold": 0.06,
}

_GRIP_HOME_CFG = {
    "stable_pos": [0.5],
    "kp": [10.0],
    "kd": [0.5],
    "lim_err": 0.02,
    "arrive_threshold": 0.06,
}

class HexFlowTemplateE3Desktop:

    def __init__(self, name="template_e3_desktop"):
        self.__name = name
        self.__ros_interface = DataInterface(name, rate_hz=1.0)
        self.__stop_event = threading.Event()
        self.__sides = ("left", "right")

        self.__load_config()
        self.__init_subs()
        self.__init_pubs()

    def __load_config(self):
        self.__ros_interface.set_parameter("rate_hz", 500.0)
        self.__ros_interface.set_parameter("clock_source", "driver_timestamp")

        self.__rate_hz = self.__ros_interface.get_parameter("rate_hz")
        self.__clock_source = self.__ros_interface.get_parameter("clock_source")
        self.__arm_stable_pos = np.array(_ARM_HOME_CFG["stable_pos"], dtype=np.float64)
        self.__grip_stable_pos = np.array(_GRIP_HOME_CFG["stable_pos"], dtype=np.float64)
        self.__arm_kp = np.array(_ARM_HOME_CFG["kp"], dtype=np.float64)
        self.__arm_kd = np.array(_ARM_HOME_CFG["kd"], dtype=np.float64)
        self.__grip_kp = np.array(_GRIP_HOME_CFG["kp"], dtype=np.float64)
        self.__grip_kd = np.array(_GRIP_HOME_CFG["kd"], dtype=np.float64)
        self.__arrive_threshold = _ARM_HOME_CFG["arrive_threshold"]
        self.__arm_err_threshold = _ARM_HOME_CFG["lim_err"]
        self.__grip_err_threshold = _GRIP_HOME_CFG["lim_err"]

    def __init_subs(self):
        for side in self.__sides:
            self.__ros_interface.create_subscription_buffered(
                f"{side}_arm_state", ArmState, maxlen=10)
            self.__ros_interface.create_subscription_buffered(
                f"{side}_grip_state", GripState, maxlen=10)
        self.__ros_interface.create_subscription_buffered(
            "keys", Joy, maxlen=10)

    def __init_pubs(self):
        self.__arm_ctrl_pubs = {}
        self.__grip_ctrl_pubs = {}
        for side in self.__sides:
            self.__arm_ctrl_pubs[side] = self.__ros_interface.create_publisher(
                f"{side}_arm_ctrl", ArmCtrl, 10)
            self.__grip_ctrl_pubs[side] = self.__ros_interface.create_publisher(
                f"{side}_grip_ctrl", GripCtrl, 10)

    def __build_pos_ctrl(self, stable_pos, kp, kd, lim_err):
        ctrl = ArmCtrl()
        ctrl.stamp = self.__ros_interface.get_clocksource_timestamp(self.__clock_source)
        ctrl.ctrl_mode = ArmCtrlMode.POS
        ctrl.jnt_pos = stable_pos.tolist()
        ctrl.mit_kp = kp.tolist()
        ctrl.mit_kd = kd.tolist()
        ctrl.lim_err = lim_err
        return ctrl

    def __build_comp_ctrl(self):
        ctrl = ArmCtrl()
        ctrl.stamp = self.__ros_interface.get_clocksource_timestamp(self.__clock_source)
        ctrl.ctrl_mode = ArmCtrlMode.COMP
        ctrl.mit_tau = np.zeros(6).tolist()
        ctrl.mit_kp = np.zeros(6).tolist()
        ctrl.mit_kd = np.zeros(6).tolist()
        return ctrl

    def __build_grip_pos_ctrl(self, stable_pos, kp, kd, lim_err):
        ctrl = GripCtrl()
        ctrl.stamp = self.__ros_interface.get_clocksource_timestamp(self.__clock_source)
        ctrl.ctrl_mode = GripCtrlMode.POS
        ctrl.jnt_pos = stable_pos.tolist()
        ctrl.mit_kp = kp.tolist()
        ctrl.mit_kd = kd.tolist()
        ctrl.lim_err = lim_err
        return ctrl
    
    def __build_grip_comp_ctrl(self):
        ctrl = GripCtrl()
        ctrl.stamp = self.__ros_interface.get_clocksource_timestamp(self.__clock_source)
        ctrl.ctrl_mode = GripCtrlMode.COMP
        ctrl.mit_tau = np.zeros(1).tolist()
        ctrl.mit_kp = np.zeros(1).tolist()
        ctrl.mit_kd = np.zeros(1).tolist()
        return ctrl

    def __is_running(self):
        return self.__ros_interface.ok() and not self.__stop_event.is_set()

    def __teleop_process(self):
        self.__ros_interface.set_rate(100.0)
        prev_q = 0
        while self.__is_running():
            self.__ros_interface.sleep()
            msg = self.__ros_interface.get("keys", latest=True)
            if msg is not None:
                curr_q = msg.buttons[16]
                if curr_q and not prev_q:
                    self.__stop_event.set()
                    self.__ros_interface.logi("Exit signal in, arm homing.")
                prev_q = curr_q

    def __init_process(self):
        self.__ros_interface.set_rate(self.__rate_hz)
        arrived = {side: False for side in self.__sides}
        while self.__is_running():
            self.__ros_interface.sleep()

            for side in self.__sides:
                if arrived[side]:
                    continue
                arm_msg = self.__ros_interface.get(
                    f"{side}_arm_state", latest=True)
                grip_msg = self.__ros_interface.get(
                    f"{side}_grip_state", latest=True)
                if arm_msg is None:
                    continue

                jnt_pos = np.array(arm_msg.jnt_pos, dtype=np.float64)
                arm_err = np.fabs(self.__arm_stable_pos - jnt_pos).max()

                grip_err = 0.0
                if grip_msg is not None:
                    grip_pos = np.array(grip_msg.jnt_pos, dtype=np.float64)
                    grip_err = np.fabs(
                        self.__grip_stable_pos - grip_pos).max()

                if arm_err < self.__arrive_threshold and grip_err < self.__arrive_threshold:
                    arrived[side] = True
                else:
                    ctrl = self.__build_pos_ctrl(
                        self.__arm_stable_pos, self.__arm_kp,
                        self.__arm_kd, self.__arm_err_threshold)
                    self.__ros_interface.publish(
                        self.__arm_ctrl_pubs[side], ctrl)

                    grip_ctrl = self.__build_grip_pos_ctrl(
                        self.__grip_stable_pos, self.__grip_kp,
                        self.__grip_kd, self.__grip_err_threshold)
                    self.__ros_interface.publish(
                        self.__grip_ctrl_pubs[side], grip_ctrl)

            if all(arrived.values()):
                return

    def __work_process(self):
        self.__ros_interface.set_rate(self.__rate_hz)
        while self.__is_running():
            self.__ros_interface.sleep()
            for side in self.__sides:
                ctrl = self.__build_comp_ctrl()
                self.__ros_interface.publish(
                    self.__arm_ctrl_pubs[side], ctrl)

                grip_ctrl = self.__build_grip_comp_ctrl()
                self.__ros_interface.publish(
                    self.__grip_ctrl_pubs[side], grip_ctrl)

    def __exit_process(self):
        self.__ros_interface.set_rate(self.__rate_hz)
        arrived = {side: False for side in self.__sides}
        while self.__ros_interface.ok():
            self.__ros_interface.sleep()

            for side in self.__sides:
                if arrived[side]:
                    continue
                arm_msg = self.__ros_interface.get(
                    f"{side}_arm_state", latest=True)
                grip_msg = self.__ros_interface.get(
                    f"{side}_grip_state", latest=True)
                if arm_msg is None:
                    continue

                jnt_pos = np.array(arm_msg.jnt_pos, dtype=np.float64)
                arm_err = np.fabs(self.__arm_stable_pos - jnt_pos).max()

                grip_err = 0.0
                if grip_msg is not None:
                    grip_pos = np.array(grip_msg.jnt_pos, dtype=np.float64)
                    grip_err = np.fabs(
                        self.__grip_stable_pos - grip_pos).max()

                if arm_err < self.__arrive_threshold:
                    arrived[side] = True
                else:
                    ctrl = self.__build_pos_ctrl(
                        self.__arm_stable_pos, self.__arm_kp,
                        self.__arm_kd, self.__arm_err_threshold)
                    self.__ros_interface.publish(
                        self.__arm_ctrl_pubs[side], ctrl)

                    grip_ctrl = self.__build_grip_pos_ctrl(
                        self.__grip_stable_pos, self.__grip_kp,
                        self.__grip_kd, self.__grip_err_threshold)
                    self.__ros_interface.publish(
                        self.__grip_ctrl_pubs[side], grip_ctrl)

            if all(arrived.values()):
                return

    def start(self):
        self.__stop_event.clear()
        self.__teleop_thread = threading.Thread(target=self.__teleop_process)
        self.__teleop_thread.start()
        self.__init_process()

    def run(self):
        self.__work_process()

    def stop(self):
        self.__stop_event.set()
        if hasattr(self, '_HexFlowTemplateE3Desktop__teleop_thread'):
            self.__teleop_thread.join(timeout=2.0)
        self.__exit_process()
        self.__ros_interface.logi("Arm homed, ready to exit.")
        self.__ros_interface.shutdown()
