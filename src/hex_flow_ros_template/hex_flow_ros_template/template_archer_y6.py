import threading
import traceback

import numpy as np
from hex_flow_ros_common.interface import DataInterface
from hex_flow_ros_common.ctrl_mode import ArmCtrlMode, GripCtrlMode
from hex_flow_ros_msg.msg import ArmState, ArmCtrl, GripState, GripCtrl
from sensor_msgs.msg import Joy


class HexFlowTemplateArcherY6:

    def __init__(self, name="template_archer_y6"):
        self.__name = name
        self.__interface = DataInterface(name, rate_hz=500.0)
        self.__stop_event = threading.Event()

        self.__init_params()
        self.__init_subs()
        self.__init_pubs()

    def __init_params(self):
        # rate_hz: template control loop rate
        self.__interface.set_parameter("rate_hz", 500.0)
        # arm_stable_pos: 6-DOF stable joint position for init/exit
        self.__interface.set_parameter("arm_stable_pos",
                                        [0.0, -1.5, 3.0, 0.07, 0.0, 0.0])
        # grip_stable_pos: 1-DOF stable grip position
        self.__interface.set_parameter("grip_stable_pos", [0.5])
        # arm_kp/arm_kd: MIT mode stiffness/damping for arm
        self.__interface.set_parameter("arm_kp", [50.0] * 6)
        self.__interface.set_parameter("arm_kd", [2.0] * 6)
        # grip_kp/grip_kd: MIT mode stiffness/damping for grip
        self.__interface.set_parameter("grip_kp", [10.0])
        self.__interface.set_parameter("grip_kd", [1.0])
        # arrive_threshold: max error to consider position as arrived
        self.__interface.set_parameter("arrive_threshold", 0.06)
        # arm_err_threshold: max arm joint error for init/exit
        self.__interface.set_parameter("arm_err_threshold", 0.02)
        # grip_err_threshold: max grip joint error for init/exit
        self.__interface.set_parameter("grip_err_threshold", 0.02)

        self.__rate_hz = self.__interface.get_parameter("rate_hz")
        self.__arm_stable_pos = np.array(
            self.__interface.get_parameter("arm_stable_pos"), dtype=np.float64)
        self.__grip_stable_pos = np.array(
            self.__interface.get_parameter("grip_stable_pos"), dtype=np.float64)
        self.__arm_kp = np.array(
            self.__interface.get_parameter("arm_kp"), dtype=np.float64)
        self.__arm_kd = np.array(
            self.__interface.get_parameter("arm_kd"), dtype=np.float64)
        self.__grip_kp = np.array(
            self.__interface.get_parameter("grip_kp"), dtype=np.float64)
        self.__grip_kd = np.array(
            self.__interface.get_parameter("grip_kd"), dtype=np.float64)
        self.__arrive_threshold = self.__interface.get_parameter(
            "arrive_threshold")
        self.__arm_err_threshold = self.__interface.get_parameter(
            "arm_err_threshold")
        self.__grip_err_threshold = self.__interface.get_parameter(
            "grip_err_threshold")

    def __init_subs(self):
        self.__interface.create_subscription_buffered(
            "arm_state", ArmState, maxlen=10)
        self.__interface.create_subscription_buffered(
            "grip_state", GripState, maxlen=10)
        self.__interface.create_subscription_buffered(
            "keys", Joy, maxlen=10)

    def __init_pubs(self):
        self.__arm_ctrl_pub = self.__interface.create_publisher(
            "arm_ctrl", ArmCtrl, 10)
        self.__grip_ctrl_pub = self.__interface.create_publisher(
            "grip_ctrl", GripCtrl, 10)

    def __build_pos_ctrl(self, stable_pos, kp, kd, lim_err):
        ctrl = ArmCtrl()
        ctrl.stamp = self.__interface.get_timestamp()
        ctrl.ctrl_mode = ArmCtrlMode.POS
        ctrl.jnt_pos = stable_pos.tolist()
        ctrl.mit_kp = kp.tolist()
        ctrl.mit_kd = kd.tolist()
        ctrl.lim_err = lim_err
        return ctrl

    def __build_comp_ctrl(self):
        ctrl = ArmCtrl()
        ctrl.stamp = self.__interface.get_timestamp()
        ctrl.ctrl_mode = ArmCtrlMode.COMP
        ctrl.mit_tau = np.zeros(6).tolist()
        ctrl.mit_kp = np.zeros(6).tolist()
        ctrl.mit_kd = np.zeros(6).tolist()
        return ctrl

    def __build_grip_pos_ctrl(self, stable_pos, kp, kd, lim_err):
        ctrl = GripCtrl()
        ctrl.stamp = self.__interface.get_timestamp()
        ctrl.ctrl_mode = GripCtrlMode.POS
        ctrl.jnt_pos = stable_pos.tolist()
        ctrl.mit_kp = kp.tolist()
        ctrl.mit_kd = kd.tolist()
        ctrl.lim_err = lim_err
        return ctrl

    def __teleop_process(self):
        self.__interface.set_rate(100.0)
        prev_q = 0
        while self.__interface.ok() and not self.__stop_event.is_set():
            self.__interface.sleep()
            msg = self.__interface.get("keys", latest=True)
            if msg is not None:
                curr_q = msg.buttons[16]  # buttons[16] = 'q'
                if curr_q and not prev_q:
                    self.__stop_event.set()
                prev_q = curr_q

    def __init_process(self):
        self.__interface.set_rate(self.__rate_hz)
        while self.__interface.ok() and not self.__stop_event.is_set():
            self.__interface.sleep()

            state_msg = self.__interface.get("arm_state", latest=True)
            grip_msg = self.__interface.get("grip_state", latest=True)

            if state_msg is None:
                continue

            jnt_pos = np.array(state_msg.jnt_pos, dtype=np.float64)
            arm_err = np.fabs(self.__arm_stable_pos - jnt_pos).max()
            grip_err = 0.0
            if grip_msg is not None:
                grip_pos = np.array(grip_msg.jnt_pos, dtype=np.float64)
                grip_err = np.fabs(self.__grip_stable_pos - grip_pos).max()

            if arm_err < self.__arrive_threshold and grip_err < self.__arrive_threshold:
                return

            ctrl = self.__build_pos_ctrl(
                self.__arm_stable_pos, self.__arm_kp,
                self.__arm_kd, self.__arm_err_threshold)
            self.__interface.publish(self.__arm_ctrl_pub, ctrl)

            grip_ctrl = self.__build_grip_pos_ctrl(
                self.__grip_stable_pos, self.__grip_kp,
                self.__grip_kd, self.__grip_err_threshold)
            self.__interface.publish(self.__grip_ctrl_pub, grip_ctrl)

    def __work_process(self):
        self.__interface.set_rate(self.__rate_hz)
        while self.__interface.ok() and not self.__stop_event.is_set():
            self.__interface.sleep()

            ctrl = self.__build_comp_ctrl()
            self.__interface.publish(self.__arm_ctrl_pub, ctrl)

    def __exit_process(self):
        self.__init_process()

    def start(self):
        self.__stop_event.clear()
        self.__teleop_thread = threading.Thread(target=self.__teleop_process)
        self.__teleop_thread.start()
        self.__init_process()

    def run(self):
        self.__work_process()

    def stop(self):
        self.__stop_event.set()
        if hasattr(self, '_HexFlowTemplateArcherY6__teleop_thread'):
            self.__teleop_thread.join(timeout=2.0)
        self.__exit_process()
        self.__interface.shutdown()
