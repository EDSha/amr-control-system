#!/usr/bin/env python3
import rclpy
from rclpy.node import Node
from std_msgs.msg import Float64
import paho.mqtt.client as mqtt
import json

class MQTTtoROS(Node):
    def __init__(self):
        super().__init__('mqtt_bridge')
        # ROS publishers
        self.left_pub = self.create_publisher(Float64, '/left_motor/cmd', 10)
        self.right_pub = self.create_publisher(Float64, '/right_motor/cmd', 10)
        
        # MQTT setup
        self.mqtt_client = mqtt.Client()
        self.mqtt_client.on_connect = self.on_mqtt_connect
        self.mqtt_client.on_message = self.on_mqtt_message
        self.mqtt_client.connect("mqtt", 1883, 60)
        self.mqtt_client.loop_start()
        
        self.get_logger().info("🚀 MQTT bridge started. Waiting for commands...")

    def on_mqtt_connect(self, client, userdata, flags, rc):
        self.get_logger().info(f"✅ Connected to MQTT with code {rc}")
        client.subscribe("fms/robot/control")

    def on_mqtt_message(self, client, userdata, msg):
        try:
            data = json.loads(msg.payload.decode())
            left = float(data.get('left', 0.0))
            right = float(data.get('right', 0.0))
            
            # Publish to ROS
            left_msg = Float64()
            left_msg.data = left
            self.left_pub.publish(left_msg)
            
            right_msg = Float64()
            right_msg.data = right
            self.right_pub.publish(right_msg)
            
            self.get_logger().info(f"📨 MQTT → ROS: L={left:.2f}, R={right:.2f}")
        except Exception as e:
            self.get_logger().error(f"❌ Error: {e}")

def main(args=None):
    rclpy.init(args=args)
    node = MQTTtoROS()
    rclpy.spin(node)
    rclpy.shutdown()

if __name__ == '__main__':
    main()
