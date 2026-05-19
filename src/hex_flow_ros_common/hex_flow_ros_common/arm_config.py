#!/usr/bin/env python3
# -*- coding:utf-8 -*-
################################################################
# Copyright 2026 Dong Zhaorui. All rights reserved.
# Author: Dong Zhaorui thetaigon@qq.com
# Date  : 2026-05-19
################################################################

"""Default arm/grip gain configurations for test nodes.

COMP mode is the default fallback when ctrl_mode is not recognized.
It provides zero gains as a safe default (compensation/no-op).
"""

from hex_flow_ros_common.ctrl_mode import ArmCtrlMode, GripCtrlMode

# Arm gain configs: only mit_* and lim_* fields.
# jnt_pos/jnt_vel/pose_pos/pose_quat/ctrl_mode are set by each node directly.
ARM_CTRL_GAINS = {
    ArmCtrlMode.COMP: {
        "mit_kp": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "mit_kd": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
        "mit_tau": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    },
    ArmCtrlMode.MIT: {
        "mit_kp": [400.0, 400.0, 500.0, 200.0, 100.0, 100.0],
        "mit_kd": [5.0, 5.0, 5.0, 5.0, 2.0, 2.0],
        "mit_tau": [0.0, 0.0, 0.0, 0.0, 0.0, 0.0],
    },
    ArmCtrlMode.POS: {
        "mit_kp": [400.0, 400.0, 500.0, 200.0, 100.0, 100.0],
        "mit_kd": [5.0, 5.0, 5.0, 5.0, 2.0, 2.0],
        "lim_err": 0.03,
    },
    ArmCtrlMode.POSE: {
        "mit_kp": [400.0, 400.0, 500.0, 200.0, 100.0, 100.0],
        "mit_kd": [5.0, 5.0, 5.0, 5.0, 2.0, 2.0],
        "lim_err": 0.03,
    },
}

# Grip gain configs: only mit_* and lim_* fields.
GRIP_CTRL_GAINS = {
    GripCtrlMode.COMP: {
        "mit_kp": [0.0],
        "mit_kd": [0.0],
        "mit_tau": [0.0],
    },
    GripCtrlMode.MIT: {
        "mit_kp": [10.0],
        "mit_kd": [0.5],
        "mit_tau": [0.0],
    },
    GripCtrlMode.POS: {
        "mit_kp": [10.0],
        "mit_kd": [0.5],
        "lim_err": 0.01,
    },
}
