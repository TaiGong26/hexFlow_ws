#!/usr/bin/env python3
# -*- coding:utf-8 -*-
################################################################
# Copyright 2026 Dong Zhaorui. All rights reserved.
# Author: Dong Zhaorui 847235539@qq.com
# Date  : 2026-05-09
################################################################

# hex_flow_ros_robot configuration defaults

# Archer Y6 Robot
ROBOT_ARCHER_Y6_DEFAULT = {
    "host": "192.168.1.100",
    "port": 8439,
    "ctrl_rate": 500.0,
    "state_buffer_size": 200,
    "sens_ts": True,
    "grip_type": "gp80",
    "pose_end_in_flange": "0.187,0.0,0.0,1.0,0.0,0.0,0.0",
}

# Firefly Y6 Robot
ROBOT_FIREFLY_Y6_DEFAULT = {
    "host": "192.168.1.100",
    "port": 8439,
    "ctrl_rate": 500.0,
    "state_buffer_size": 200,
    "sens_ts": True,
}

# Hello Y6 Robot
ROBOT_HELLO_Y6_DEFAULT = {
    "host": "192.168.1.100",
    "port": 8439,
    "ctrl_rate": 500.0,
    "state_buffer_size": 200,
    "sens_ts": True,
}
