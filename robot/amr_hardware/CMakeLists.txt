cmake_minimum_required(VERSION 3.8)
project(amr_hardware)

if(NOT CMAKE_CXX_STANDARD)
  set(CMAKE_CXX_STANDARD 17)
endif()

find_package(ament_cmake REQUIRED)
find_package(rclcpp REQUIRED)
find_package(std_msgs REQUIRED)
find_package(builtin_interfaces REQUIRED)
find_package(rosidl_default_generators REQUIRED)
find_package(rosidl_default_runtime REQUIRED)

# Генерация сообщений
set(msg_files
  "msg/RobotStatus.msg"
)

rosidl_generate_interfaces(${PROJECT_NAME}
  ${msg_files}
  DEPENDENCIES std_msgs builtin_interfaces
)

# Явно указываем имя сгенерированной библиотеки
set(generated_interfaces_lib ${PROJECT_NAME}__rosidl_typesupport_cpp)

# Объявляем исполняемые файлы
add_executable(motor_controller src/motor_controller.cpp)
add_executable(motor_controller_v2 src/motor_controller_v2.cpp)
add_executable(motor_listener src/motor_listener.cpp)

# Зависимости с явным указанием сгенерированной библиотеки
ament_target_dependencies(motor_controller
  rclcpp
  std_msgs
)

target_link_libraries(motor_controller
  ${generated_interfaces_lib}
)

ament_target_dependencies(motor_controller_v2
  rclcpp
  std_msgs
)

target_link_libraries(motor_controller_v2
  ${generated_interfaces_lib}
)

ament_target_dependencies(motor_listener
  rclcpp
  std_msgs
)

target_link_libraries(motor_listener
  ${generated_interfaces_lib}
)

install(TARGETS
  motor_controller
  motor_controller_v2
  motor_listener
  DESTINATION lib/${PROJECT_NAME}
)

# Установка конфигурационных файлов
install(DIRECTORY urdf worlds launch config
  DESTINATION share/${PROJECT_NAME}
)
ament_package()