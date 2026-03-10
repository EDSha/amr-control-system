#!/usr/bin/env python3
"""
Мост между ROS и MQTT для роботележки
Принимает команды из FMS (MQTT) → отправляет в ROS
Читает состояние из ROS → отправляет в FMS (MQTT)
"""
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import paho.mqtt.client as mqtt
import json

class RosMqttBridge(Node):
    def __init__(self):
        super().__init__('ros_mqtt_bridge')
        
        # Подписка на команды от ROS ноды (твой motor_controller)
        self.create_subscription(Float64, '/left_motor/speed', 
                                self.left_speed_callback, 10)
        self.create_subscription(Float64, '/right_motor/speed',
                                self.right_speed_callback, 10)
        
        # Публикация команд от FMS в ROS
        self.left_cmd_pub = self.create_publisher(Float64, '/left_motor/cmd', 10)
        self.right_cmd_pub = self.create_publisher(Float64, '/right_motor/cmd', 10)
        
        # Настройка MQTT клиента
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_mqtt_connect
        self.mqtt_client.on_message = self.on_mqtt_message
        
        # Подключение к MQTT брокеру (он уже запущен в docker-compose)
        self.mqtt_client.connect("localhost", 1883, 60)
        self.mqtt_client.loop_start()
        
        self.get_logger().info("✅ ROS-MQTT bridge started")
    
    def on_mqtt_connect(self, client, userdata, flags, rc):
        self.get_logger().info(f"✅ Connected to MQTT broker (code: {rc})")
        # Подписываемся на команды от FMS
        client.subscribe("fms/robot/control")
    
    def on_mqtt_message(self, client, userdata, msg):
        """Получение команды от FMS через MQTT"""
        try:
            data = json.loads(msg.payload.decode())
            left = float(data.get('left', 0.0))
            right = float(data.get('right', 0.0))
            
            # Создаём ROS сообщения
            left_msg = Float64()
            left_msg.data = left
            
            right_msg = Float64()
            right_msg.data = right
            
            # Публикуем в ROS
            self.left_cmd_pub.publish(left_msg)
            self.right_cmd_pub.publish(right_msg)
            
            self.get_logger().info(f"📨 MQTT → ROS: L={left:.2f}, R={right:.2f}")
            
        except Exception as e:
            self.get_logger().error(f"❌ MQTT error: {e}")
    
    def left_speed_callback(self, msg):
        """Отправка скорости левого мотора в FMS"""
        self.mqtt_client.publish("robot/motors/left/actual", str(msg.data))
    
    def right_speed_callback(self, msg):
        """Отправка скорости правого мотора в FMS"""
        self.mqtt_client.publish("robot/motors/right/actual", str(msg.data))

def main():
    rclpy.init()
    node = RosMqttBridge()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
