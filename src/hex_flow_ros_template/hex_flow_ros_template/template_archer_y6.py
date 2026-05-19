import threading
import traceback

import numpy as np
from hex_flow_ros_common.interface import DataInterface
from hex_flow_ros_common.ctrl_mode import ArmCtrlMode, GripCtrlMode
from hex_flow_ros_msg.msg import ArmState, ArmCtrl, GripState, GripCtrl
from sensor_msgs.msg import Joy
from hex_util_runtime import HexRate

class HexFlowTemplateArcherY6:

    def __init__(self, name="template_archer_y6"):
        self.__name = name
        self.__ros_interface = DataInterface(name, rate_hz=500.0)
        self.__stop_event = threading.Event()

        self.__init_params()
        self.__init_subs()
        self.__init_pubs()

    def __init_params(self):
        # rate_hz: template control loop rate
        self.__ros_interface.set_parameter("rate_hz", 500.0)
        # arm_stable_pos: 6-DOF stable joint position for init/exit
        self.__ros_interface.set_parameter("arm_stable_pos",
                                        [0.0, -1.5, 3.0, 0.07, 0.0, 0.0])
        # grip_stable_pos: 1-DOF stable grip position
        self.__ros_interface.set_parameter("grip_stable_pos", [0.5])
        # arm_kp/arm_kd: MIT mode stiffness/damping for arm
        self.__ros_interface.set_parameter("arm_kp", [50.0] * 6)
        self.__ros_interface.set_parameter("arm_kd", [2.0] * 6)
        # grip_kp/grip_kd: MIT mode stiffness/damping for grip
        self.__ros_interface.set_parameter("grip_kp", [10.0])
        self.__ros_interface.set_parameter("grip_kd", [1.0])
        # arrive_threshold: max error to consider position as arrived
        self.__ros_interface.set_parameter("arrive_threshold", 0.06)
        # arm_err_threshold: max arm joint error for init/exit
        self.__ros_interface.set_parameter("arm_err_threshold", 0.02)
        # grip_err_threshold: max grip joint error for init/exit
        self.__ros_interface.set_parameter("grip_err_threshold", 0.02)
        # clock_source: timestamp clock source for published messages (driver_timestamp or ros)
        self.__ros_interface.set_parameter("clock_source", "driver_timestamp")

        self.__rate_hz = self.__ros_interface.get_parameter("rate_hz")
        self.__clock_source = self.__ros_interface.get_parameter("clock_source")
        self.__arm_stable_pos = np.array(
            self.__ros_interface.get_parameter("arm_stable_pos"), dtype=np.float64)
        self.__grip_stable_pos = np.array(
            self.__ros_interface.get_parameter("grip_stable_pos"), dtype=np.float64)
        self.__arm_kp = np.array(
            self.__ros_interface.get_parameter("arm_kp"), dtype=np.float64)
        self.__arm_kd = np.array(
            self.__ros_interface.get_parameter("arm_kd"), dtype=np.float64)
        self.__grip_kp = np.array(
            self.__ros_interface.get_parameter("grip_kp"), dtype=np.float64)
        self.__grip_kd = np.array(
            self.__ros_interface.get_parameter("grip_kd"), dtype=np.float64)
        self.__arrive_threshold = self.__ros_interface.get_parameter(
            "arrive_threshold")
        self.__arm_err_threshold = self.__ros_interface.get_parameter(
            "arm_err_threshold")
        self.__grip_err_threshold = self.__ros_interface.get_parameter(
            "grip_err_threshold")

    def __init_subs(self):
        self.__ros_interface.create_subscription_buffered(
            "arm_state", ArmState, maxlen=10)
        self.__ros_interface.create_subscription_buffered(
            "grip_state", GripState, maxlen=10)
        self.__ros_interface.create_subscription_buffered(
            "keys", Joy, maxlen=10)

    def __init_pubs(self):
        self.__arm_ctrl_pub = self.__ros_interface.create_publisher(
            "arm_ctrl", ArmCtrl, 10)
        self.__grip_ctrl_pub = self.__ros_interface.create_publisher(
            "grip_ctrl", GripCtrl, 10)

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

    def __teleop_process(self):
        try:            
            rate = HexRate(100.0)
            prev_q = 0
            while self.__is_running():
                rate.sleep()
                msg = self.__ros_interface.get("keys", latest=True)
                if msg is not None:
                    curr_q = msg.buttons[16]  # buttons[16] = 'q'
                    if curr_q and not prev_q:
                        self.__stop_event.set()
                        self.__ros_interface.logi("Exit signal in, arm homing.")
                        
                    prev_q = curr_q
        except Exception as e:
            self.__ros_interface.loge(f"Exception in template teleop process: {e}")
            traceback.print_exc()

    def __init_process(self):
        try: 
            rate = HexRate(self.__rate_hz)
            while self.__is_running():
                rate.sleep()

                state_msg = self.__ros_interface.get("arm_state", latest=True)
                grip_msg = self.__ros_interface.get("grip_state", latest=True)

                if state_msg is None:
                    continue

                jnt_pos = np.array(state_msg.jnt_pos, dtype=np.float64)
                arm_err = np.fabs(self.__arm_stable_pos - jnt_pos).max()
                grip_err = 0.0
                if grip_msg is not None:
                    grip_pos = np.array(grip_msg.jnt_pos, dtype=np.float64)
                    grip_err = np.fabs(self.__grip_stable_pos - grip_pos).max()

                # If both arm and grip are within the arrive threshold, consider arrived and break the loop
                if arm_err < self.__arrive_threshold and grip_err < self.__arrive_threshold:
                    return

                ctrl = self.__build_pos_ctrl(
                    self.__arm_stable_pos, 
                    self.__arm_kp,
                    self.__arm_kd, 
                    self.__arm_err_threshold
                )
                self.__ros_interface.publish(self.__arm_ctrl_pub, ctrl)

                grip_ctrl = self.__build_grip_pos_ctrl(
                    self.__grip_stable_pos, 
                    self.__grip_kp,
                    self.__grip_kd, 
                    self.__grip_err_threshold
                )
                self.__ros_interface.publish(self.__grip_ctrl_pub, grip_ctrl)
        except Exception as e:
            self.__ros_interface.loge(f"Exception in template init process: {e}")
                
                
    def __work_process(self):
        try:
            rate = HexRate(self.__rate_hz)
                
            while self.__is_running():
                rate.sleep()
                arm_ctrl = self.__build_comp_ctrl()
                self.__ros_interface.publish(self.__arm_ctrl_pub, arm_ctrl)
                
                grip_ctrl = self.__build_grip_comp_ctrl()
                self.__ros_interface.publish(self.__grip_ctrl_pub, grip_ctrl)
        except Exception as e:
            self.__ros_interface.loge(f"Exception in template work process: {e}")
            
    def __exit_process(self):
        try: 
            rate = HexRate(self.__rate_hz)
            while self.__ros_interface.ok():
                rate.sleep()

                state_msg = self.__ros_interface.get("arm_state", latest=True)
                grip_msg = self.__ros_interface.get("grip_state", latest=True)

                if state_msg is None:
                    continue

                jnt_pos = np.array(state_msg.jnt_pos, dtype=np.float64)
                arm_err = np.fabs(self.__arm_stable_pos - jnt_pos).max()
                grip_err = 0.0
                if grip_msg is not None:
                    grip_pos = np.array(grip_msg.jnt_pos, dtype=np.float64)
                    grip_err = np.fabs(self.__grip_stable_pos - grip_pos).max()

                # If both arm and grip are within the arrive threshold, consider arrived and break the loop
                if arm_err < self.__arrive_threshold and grip_err < self.__arrive_threshold:
                    return

                ctrl = self.__build_pos_ctrl(
                    self.__arm_stable_pos, 
                    self.__arm_kp,
                    self.__arm_kd, 
                    self.__arm_err_threshold
                )
                self.__ros_interface.publish(self.__arm_ctrl_pub, ctrl)

                grip_ctrl = self.__build_grip_pos_ctrl(
                    self.__grip_stable_pos, 
                    self.__grip_kp,
                    self.__grip_kd, 
                    self.__grip_err_threshold
                )
                self.__ros_interface.publish(self.__grip_ctrl_pub, grip_ctrl)
        except KeyboardInterrupt:
            pass
        except Exception as e:
            self.__ros_interface.loge(f"Exception in template init process: {e}")

    def __is_running(self):
        return self.__ros_interface.ok() and not self.__stop_event.is_set()
    
    def start(self):
        self.__stop_event.clear()
        self.__teleop_thread = threading.Thread(target=self.__teleop_process)
        self.__teleop_thread.start()
        self.__init_process()

    def run(self):
        try:
            self.__work_process()
        except KeyboardInterrupt:
            pass
        except Exception as e:
            self.__ros_interface.loge(f"Exception in template work process: {e}")
        self.stop()
        
        
    def stop(self):
        self.__stop_event.set()
        self.__teleop_thread.join(timeout=2.0)
        self.__exit_process()
        self.__ros_interface.logi("Arm homed, ready to exit.")
        self.__ros_interface.shutdown()
        