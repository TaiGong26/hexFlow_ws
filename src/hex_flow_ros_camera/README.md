<h1 align="center">HEX FLOW ROS CAMERA</h1>

<p align="center">
    <a href="https://github.com/hexfellow/hex_flow_ros_camera/stargazers">
        <img src="https://img.shields.io/github/stars/hexfellow/hex_flow_ros_camera?style=flat-square&logo=github" />
    </a>
    <a href="https://github.com/hexfellow/hex_flow_ros_camera/forks">
        <img src="https://img.shields.io/github/forks/hexfellow/hex_flow_ros_camera?style=flat-square&logo=github" />
    </a>
    &nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;
    <a href="https://github.com/hexfellow/hex_flow_ros_camera/issues">
        <img src="https://img.shields.io/github/issues/hexfellow/hex_flow_ros_camera?style=flat-square&logo=github" />
    </a>
</p>

---

# hex_flow_ros_camera

## Overview

`hex_flow_ros_camera` is the HexFlow ROS2 camera node package, supporting four camera types: USB, Dummy, Intel RealSense, and Berxel ToF. It provides color and depth image publishing. Each camera node captures image data through the corresponding `hex_driver_camera` driver callback and publishes it as `sensor_msgs/Image` messages via `DataInterface`.

## Dependencies

### RealSense SDK
```https://github.com/IntelRealSense/librealsense```
> You need to install the appropriate realsense dependencies according to your device.

### Berxel SDK
> For Berxel cameras, you need to install the vendor SDK `berxel_py_wrapper>=2.0.182`.

### ROS2 Dependencies
```bash
git clone https://github.com/hexfellow/hex_flow_ros_common.git
git clone https://github.com/hexfellow/hex_flow_ros_msg.git
git clone https://github.com/hexfellow/hex_flow_ros_camera.git
```

### pip Installation
```bash
pip install 'opencv-python>=4.10.0' 'numpy>=2.2.6' 'hex_driver_camera>=0.1.0,<0.2.0' 'hex_util_robot>=0.0.0,<0.1.0' 'cv-bridge' 'pyrealsense2' 'berxel_py_wrapper>=2.0.182'
```

> `cv_bridge` is only used in test nodes.

## Quick Start

### launch Command Examples
```bash
ros2 launch hex_flow_ros_camera dummy_real.launch.py
ros2 launch hex_flow_ros_camera realsense_real.launch.py serial_number:=SN_123456789
ros2 launch hex_flow_ros_camera berxel_real.launch.py serial_number:=SN_123456789
ros2 launch hex_flow_ros_camera usb_real.launch.py cam_path:=/dev/video0  # default: /dev/video0
```

> **Note**: The serial number must be provided with the `SN_` prefix (e.g., `SN_123456789`). If the prefix is missing, the node will exit.      \
> For USB cameras, ensure your user group has access to the device (e.g., check `ls -l /dev/video0` and `groups`).

### test Examples
```bash
ros2 launch hex_flow_ros_camera usb_test.launch.py cam_path:=/dev/video0
ros2 launch hex_flow_ros_camera realsense_test.launch.py serial_number:=SN_123456789
ros2 launch hex_flow_ros_camera berxel_test.launch.py serial_number:=SN_123456789
```

## Topic Interfaces

### Published Topics
| Name | Type | Description | Additional Notes |
|------|------|-------------|------------------|
| `color` | `sensor_msgs/Image` | Color image | USB/Dummy: V4L2 RAW; RealSense: RGB8; Berxel: RGB8 |
| `depth` | `sensor_msgs/Image` | Depth image | Only published by RealSense/Berxel, format: 32FC1 |

## Notes

### Node Description
| Node | Executable | Description |
|------|------------|-------------|
| USB Driver | `hex-cam-usb` | OpenCV V4L2 USB camera driver |
| Dummy Driver | `hex-cam-dummy` | Simulation camera driver (fixed test image) |
| RealSense Driver | `hex-cam-realsense` | Intel RealSense D400 series driver (requires RealSense SDK installation) |
| Berxel Driver | `hex-cam-berxel` | Berxel ToF depth camera driver |
| USB Test | `hex-cam-usb-test` | Subscribes to color image and displays with OpenCV, validates USB camera input |
| Dummy Test | `hex-cam-dummy-test` | Subscribes to color image and displays with OpenCV, validates simulation camera |
| RealSense Test | `hex-cam-realsense-test` | Subscribes to color+depth images and displays with OpenCV (depth converted to pseudocolor) |
| Berxel Test | `hex-cam-berxel-test` | Subscribes to color+depth images and displays with OpenCV (depth converted to pseudocolor) |

### Test Node Details
| Node | Subscribed Topics | Published Topics | Function | Frequency |
|------|------------------|------------------|----------|-----------|
| `hex-cam-usb-test` | `color` | None | Subscribes to color image and displays with cv2.imshow | 30Hz |
| `hex-cam-dummy-test` | `color` | None | Subscribes to color image and displays with cv2.imshow | 30Hz |
| `hex-cam-realsense-test` | `color`, `depth` | None | Subscribes to color+depth, depth converted to pseudocolor and displayed with cv2.imshow | 30Hz |
| `hex-cam-berxel-test` | `color`, `depth` | None | Subscribes to color+depth, depth converted to pseudocolor and displayed with cv2.imshow | 30Hz |

### Launch Description
| Launch File | Description |
|-------------|-------------|
| `usb_real.launch.py` | USB camera driver |
| `usb_test.launch.py` | USB camera driver + test |
| `dummy_real.launch.py` | Dummy camera driver |
| `dummy_test.launch.py` | Dummy camera driver + test |
| `realsense_real.launch.py` | RealSense driver |
| `realsense_test.launch.py` | RealSense driver + test |
| `berxel_real.launch.py` | Berxel driver |
| `berxel_test.launch.py` | Berxel driver + test |

### Parameter Description
| Parameter | Default Value | Description |
|-----------|--------------|-------------|
| frame_rate | 30 | Camera frame rate (Hz) |
| height | 480 | Image height (px) |
| width | 640 | Image width (px) |
| cam_buffer_size | 8 | Camera buffer size |
| sens_ts | false | Use device clock as timestamp |
| cam_path | /dev/video0 | Camera device path |
| exposure | 100 | Exposure value |
| temperature | 4000 | Color temperature (white balance) |
| color_encoding | bgr8 | Color image encoding |
| clock_source | driver_timestamp | Timestamp clock source: driver_timestamp or ros |
| serial_number | '' | Device serial number (must be `SN_` prefixed, empty=auto detect) |
| depth_encoding | mono16 | Depth image encoding |
| gain | 100 | Gain value (Berxel) |

### Topic Remapping

#### usb_real.launch.py
```python
remappings=[
    ('color', '/cam_usb/color'),
],
```

#### usb_test.launch.py
```python
remappings=[
    ('color', '/cam_usb/color'),
],
```

#### dummy_real.launch.py
```python
remappings=[
    ('color', '/cam_dummy/color'),
],
```

#### dummy_test.launch.py
```python
remappings=[
    ('color', '/cam_dummy/color'),
],
```

#### realsense_real.launch.py
```python
remappings=[
    ('color', '/cam_realsense/color'),
    ('depth', '/cam_realsense/depth'),
],
```

#### realsense_test.launch.py
```python
remappings=[
    ('color', '/cam_realsense/color'),
    ('depth', '/cam_realsense/depth'),
],
```

#### berxel_real.launch.py
```python
remappings=[
    ('color', '/cam_berxel/color'),
    ('depth', '/cam_berxel/depth'),
],
```

#### berxel_test.launch.py
```python
# cam_berxel
remappings=[
    ('color', '/cam_berxel/color'),
    ('depth', '/cam_berxel/depth'),
],
# cam_berxel_test
remappings=[
    ('color', '/cam_berxel/color'),
    ('depth', '/cam_berxel/depth'),
],
```