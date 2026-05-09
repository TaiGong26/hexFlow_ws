#!/usr/bin/env python3
# -*- coding:utf-8 -*-
################################################################
# Copyright 2026 Dong Zhaorui. All rights reserved.
# Author: Dong Zhaorui 847235539@qq.com
# Date  : 2026-05-09
################################################################

# hex_flow_ros_camera configuration defaults
# This module provides default configurations for camera nodes

# USB Camera
CAM_USB_DEFAULT = {
    "frame_rate": 30,
    "height": 480,
    "width": 640,
    "cam_buffer_size": 8,
    "sens_ts": False,
    "cam_path": "/dev/video0",
    "exposure": 100,
    "temperature": 4000,
    "color_encoding": "bgr8",
    "rate_hz": 500.0,
}

# Dummy Camera
CAM_DUMMY_DEFAULT = {
    "frame_rate": 30,
    "height": 480,
    "width": 640,
    "cam_buffer_size": 8,
    "sens_ts": False,
    "color_encoding": "bgr8",
    "rate_hz": 500.0,
}

# RealSense Camera
CAM_REALSENSE_DEFAULT = {
    "frame_rate": 30,
    "height": 480,
    "width": 640,
    "cam_buffer_size": 8,
    "sens_ts": False,
    "serial_number": "b0",
    "color_encoding": "bgr8",
    "depth_encoding": "mono16",
    "rate_hz": 500.0,
}

# Berxel Camera
CAM_BERXEL_DEFAULT = {
    "frame_rate": 30,
    "height": 400,
    "width": 640,
    "cam_buffer_size": 8,
    "sens_ts": False,
    "serial_number": "b0",
    "exposure": 10000,
    "gain": 100,
    "color_encoding": "bgr8",
    "depth_encoding": "mono16",
    "rate_hz": 500.0,
}
