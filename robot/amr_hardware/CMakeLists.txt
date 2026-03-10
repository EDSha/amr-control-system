cmake_minimum_required(VERSION 3.8)
project(robot_control)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)

add_executable(motor_controller src/motor_controller.cpp)
ament_target_dependencies(motor_controller rclcpp std_msgs)

install(TARGETS motor_controller
  DESTINATION lib/${PROJECT_NAME})

ament_package()

# Добавляем узел motor_listener
add_executable(motor_listener src/motor_listener.cpp)
ament_target_dependencies(motor_listener rclcpp std_msgs)

# Устанавливаем узел
install(TARGETS motor_listener
  DESTINATION lib/${PROJECT_NAME})

# Версия 2 контроллера с поддержкой FMS
add_executable(motor_controller_v2 src/motor_controller_v2.cpp)
ament_target_dependencies(motor_controller_v2 rclcpp std_msgs)

install(TARGETS motor_controller_v2
  DESTINATION lib/${PROJECT_NAME})
