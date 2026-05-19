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

## 概述

`hex_flow_ros_camera` 是 HexFlow ROS2 相机节点包，支持 USB、Dummy、Intel RealSense、Berxel ToF 四种相机类型，提供彩色图和深度图发布。每个相机节点通过对应的 `hex_driver_camera` 驱动回调采集图像数据，通过 `DataInterface` 以 `sensor_msgs/Image` 消息类型发布。

## 依赖安装

### RealSense SDK
```https://github.com/IntelRealSense/librealsense```
> 您需要根据您的设备安装指定的realsense依赖

### Berxel SDK
> 对于 Berxel 相机，您需要安装厂商 SDK `berxel_py_wrapper>=2.0.182`。

### ROS2 依赖
```bash
git clone https://github.com/hexfellow/hex_flow_ros_common.git
git clone https://github.com/hexfellow/hex_flow_ros_msg.git
git clone https://github.com/hexfellow/hex_flow_ros_camera.git
```

### pip 安装
```bash
pip install 'opencv-python>=4.10.0' 'numpy>=2.2.6' 'hex_driver_camera>=0.1.0,<0.2.0' 'hex_util_robot>=0.0.0,<0.1.0' 'cv-bridge' 'pyrealsense2' 'berxel_py_wrapper>=2.0.182'
```

> `cv_bridge` 仅在 test 节点中使用。

## 快速使用

### launch 命令示例
```bash
ros2 launch hex_flow_ros_camera dummy_real.launch.py
ros2 launch hex_flow_ros_camera realsense_real.launch.py serial_number:=SN_123456789
ros2 launch hex_flow_ros_camera berxel_real.launch.py serial_number:=SN_123456789
ros2 launch hex_flow_ros_camera usb_real.launch.py cam_path:=/dev/video0  # 默认: /dev/video0
```

> **注意**：序列号必须带 `SN_` 前缀（如 `SN_123456789`）。若无前缀则节点退出。 \
> 对于 USB 相机，请确保当前用户组有设备访问权限（例如检查 `ls -l /dev/video0` 和 `groups`）。

### test 示例
```bash
ros2 launch hex_flow_ros_camera usb_test.launch.py cam_path:=/dev/video0
ros2 launch hex_flow_ros_camera realsense_test.launch.py serial_number:=SN_123456789
ros2 launch hex_flow_ros_camera berxel_test.launch.py serial_number:=SN_123456789
```

## 话题接口

### 发布话题
| 名称 | 类型 | 描述 | 补充描述 |
|------|------|------|---------|
| `color` | `sensor_msgs/Image` | 彩色图像 | USB/Dummy: V4L2 RAW；RealSense: RGB8；Berxel: RGB8 |
| `depth` | `sensor_msgs/Image` | 深度图像 | 仅 RealSense/Berxel 发布，格式为32FC1 |

## 说明

### 节点说明
| 节点 | 可执行文件 | 描述 |
|------|-----------|------|
| USB 驱动 | `hex-cam-usb` | OpenCV V4L2 USB 相机驱动 |
| Dummy 驱动 | `hex-cam-dummy` | 仿真相机驱动（固定测试图像） |
| RealSense 驱动 | `hex-cam-realsense` | Intel RealSense D400 系列驱动（需安装 RealSense SDK） |
| Berxel 驱动 | `hex-cam-berxel` | Berxel ToF 深度相机驱动 |
| USB 测试 | `hex-cam-usb-test` | 订阅 color 图像并用 OpenCV 显示，验证 USB 相机输入 |
| Dummy 测试 | `hex-cam-dummy-test` | 订阅 color 图像并用 OpenCV 显示，验证仿真相机 |
| RealSense 测试 | `hex-cam-realsense-test` | 订阅 color+depth 图像并用 OpenCV 显示（深度转伪彩色） |
| Berxel 测试 | `hex-cam-berxel-test` | 订阅 color+depth 图像并用 OpenCV 显示（深度转伪彩色） |

### Test 节点详情
| 节点 | 订阅话题 | 发布话题 | 功能 | 频率 |
|------|---------|---------|------|------|
| `hex-cam-usb-test` | `color` | 无 | 订阅 color 图像，用 cv2.imshow 显示 | 30Hz |
| `hex-cam-dummy-test` | `color` | 无 | 订阅 color 图像，用 cv2.imshow 显示 | 30Hz |
| `hex-cam-realsense-test` | `color`, `depth` | 无 | 订阅 color+depth，深度转伪彩色后用 cv2.imshow 显示 | 30Hz |
| `hex-cam-berxel-test` | `color`, `depth` | 无 | 订阅 color+depth，深度转伪彩色后用 cv2.imshow 显示 | 30Hz |

### Launch 说明
| Launch 文件 | 描述 |
|------------|------|
| `usb_real.launch.py` | USB 相机驱动 |
| `usb_test.launch.py` | USB 相机驱动 + 测试 |
| `dummy_real.launch.py` | Dummy 相机驱动 |
| `dummy_test.launch.py` | Dummy 相机驱动 + 测试 |
| `realsense_real.launch.py` | RealSense 驱动 |
| `realsense_test.launch.py` | RealSense 驱动 + 测试 |
| `berxel_real.launch.py` | Berxel 驱动 |
| `berxel_test.launch.py` | Berxel 驱动 + 测试 |

### 参数说明
| 参数 | 默认值 | 描述 |
|------|--------|------|
| frame_rate | 30 | 相机帧率（Hz） |
| height | 480 | 图像高度（px） |
| width | 640 | 图像宽度（px） |
| cam_buffer_size | 8 | 相机 buffer 大小 |
| sens_ts | false | 使用设备时钟作为时间戳 |
| cam_path | /dev/video0 | 相机设备路径 |
| exposure | 100 | 曝光值 |
| temperature | 4000 | 颜色温度（白平衡） |
| color_encoding | bgr8 | 彩色图像编码 |
| clock_source | driver_timestamp | 时间戳时钟源：driver_timestamp 或 ros |
| serial_number | '' | 设备序列号（必须为 `SN_` 前缀，空=自动检测） |
| depth_encoding | mono16 | 深度图像编码 |
| gain | 100 | 增益值（Berxel） |

### 话题重映射

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