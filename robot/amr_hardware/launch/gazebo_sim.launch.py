import os
from ament_index_python.packages import get_package_share_directory
from launch import LaunchDescription
from launch.actions import IncludeLaunchDescription
from launch.launch_description_sources import PythonLaunchDescriptionSource
from launch_ros.actions import Node

def generate_launch_description():
    # Путь к пакету
    pkg_amr_hardware = get_package_share_directory('amr_hardware')
    
    # Пути к файлам
    urdf_path = os.path.join(pkg_amr_hardware, 'urdf', 'simple_robot.urdf')
    
    # Запуск Gazebo с пустым миром
    gazebo = IncludeLaunchDescription(
        PythonLaunchDescriptionSource(
            os.path.join(get_package_share_directory('gazebo_ros'), 'launch', 'gazebo.launch.py')
        )
    )
    
    # Загрузка робота в симуляцию
    spawn_robot = Node(
        package='gazebo_ros',
        executable='spawn_entity.py',
        arguments=['-entity', 'simple_robot', '-file', urdf_path],
        output='screen'
    )
    
    # Публикация состояния робота (для RViz)
    robot_state_publisher = Node(
        package='robot_state_publisher',
        executable='robot_state_publisher',
        arguments=[urdf_path]
    )
    
    return LaunchDescription([
        gazebo,
        robot_state_publisher,
        spawn_robot
    ])