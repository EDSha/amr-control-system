#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import time
import json

def on_connect(client, userdata, flags, rc):
    print(f"✅ Connected to MQTT: {rc}")
    client.subscribe("fms/commands")

def on_message(client, userdata, msg):
    print(f"📨 Received command: {msg.topic} = {msg.payload.decode()}")

print("=== ROS-MQTT Test Bridge ===")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("mqtt", 1883, 60)
client.loop_start()

print("Bridge ready. Send commands from Ubuntu with:")
print("  mosquitto_pub -h localhost -t 'fms/commands' -m '{\"left\":0.5,\"right\":0.5}'")

counter = 0
try:
    while True:
        # Отправляем статус
        status = {
            "robot_id": "telezhka_001",
            "battery": 85,
            "position": {"x": counter * 0.1, "y": 0},
            "timestamp": time.time()
        }
        client.publish("robot/status", json.dumps(status))
        print(f"📤 Sent status #{counter}")
        counter += 1
        time.sleep(3)
except KeyboardInterrupt:
    print("\n⏹️ Stopping...")
    client.loop_stop()
