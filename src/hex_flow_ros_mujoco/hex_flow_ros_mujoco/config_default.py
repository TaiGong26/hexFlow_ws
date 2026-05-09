#!/usr/bin/env python3
# -*- coding:utf-8 -*-
################################################################
# Copyright 2026 Dong Zhaorui. All rights reserved.
# Author: Dong Zhaorui 847235539@qq.com
# Date  : 2026-05-09
################################################################

# hex_flow_ros_mujoco configuration defaults

# Archer Y6 Mujoco
MUJOCO_ARCHER_Y6_DEFAULT = {
    "state_rate": 1000.0,
    "cam_rate": 30.0,
    "headless": False,
    "state_buffer_size": 200,
    "cam_buffer_size": 8,
    "sens_ts": False,
    "camera_type": "usb",
    "rate_hz": 500.0,
}

# E3 Desktop Mujoco
MUJOCO_E3_DESKTOP_DEFAULT = {
    "state_rate": 1000.0,
    "cam_rate": 30.0,
    "headless": False,
    "state_buffer_size": 200,
    "cam_buffer_size": 8,
    "sens_ts": False,
    "head_cam_type": "empty",
    "left_cam_type": "empty",
    "right_cam_type": "empty",
    "rate_hz": 500.0,
}
