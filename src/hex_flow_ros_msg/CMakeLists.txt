cmake_minimum_required(VERSION 3.8)
project(hex_flow_ros_msg)

find_package(ament_cmake REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(builtin_interfaces REQUIRED)

set(msg_files
  msg/ArmState.msg
  msg/ArmCtrl.msg
  msg/GripState.msg
  msg/GripCtrl.msg
)

rosidl_generate_interfaces(${PROJECT_NAME}
  ${msg_files}
  DEPENDENCIES builtin_interfaces
)

ament_export_dependencies(rosidl_default_runtime)
ament_package()
