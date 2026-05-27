#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
from amr_hardware.msg import RobotStatus
import paho.mqtt.client as mqtt
import json

class MQTTtoROS(Node):
    def __init__(self):
        super().__init__('mqtt_bridge')
        
        # === ROS Publishers (команды роботу) ===
        self.left_pub = self.create_publisher(Float64, '/left_motor/cmd', 10)
        self.right_pub = self.create_publisher(Float64, '/right_motor/cmd', 10)
        
        # === ROS Subscribers (статус от робота) ===
        self.status_sub = self.create_subscription(
            RobotStatus,
            '/robot_status',
            self.status_callback,
            10)
        
        # === MQTT setup ===
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_mqtt_connect
        self.mqtt_client.on_message = self.on_mqtt_message
        self.mqtt_client.connect("mqtt", 1883, 60)
        self.mqtt_client.loop_start()
        
        self.get_logger().info("🚀 MQTT bridge started (bidirectional)")

    def on_mqtt_connect(self, client, userdata, flags, rc):
        self.get_logger().info(f"✅ Connected to MQTT with code {rc}")
        client.subscribe("fms/robot/control")

    def on_mqtt_message(self, client, userdata, msg):
        """Получение команд от FMS"""
        try:
            data = json.loads(msg.payload.decode())
            left = float(data.get('left', 0.0))
            right = float(data.get('right', 0.0))
            
            left_msg = Float64()
            left_msg.data = left
            self.left_pub.publish(left_msg)
            
            right_msg = Float64()
            right_msg.data = right
            self.right_pub.publish(right_msg)
            
            self.get_logger().info(f"📨 MQTT → ROS: L={left:.2f}, R={right:.2f}")
        except Exception as e:
            self.get_logger().error(f"❌ Error processing command: {e}")

    def status_callback(self, msg):
        """Получение статуса от робота и отправка в MQTT"""
        try:
            # Формируем JSON для отправки
            status_data = {
                'robot_id': msg.robot_id,
                'battery': msg.battery,
                'x': msg.x,
                'y': msg.y,
                'current_task': msg.current_task,
                'timestamp': {
                    'sec': msg.stamp.sec,
                    'nanosec': msg.stamp.nanosec
                }
            }
            
            # Отправляем в MQTT
            self.mqtt_client.publish("robot/status", json.dumps(status_data))
            self.get_logger().debug(f"📤 ROS → MQTT: Status sent")
            
        except Exception as e:
            self.get_logger().error(f"❌ Error sending status: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = MQTTtoROS()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
