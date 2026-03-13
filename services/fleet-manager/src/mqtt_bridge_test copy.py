#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import time

def on_connect(client, userdata, flags, rc):
    print(f"✅ Connected to MQTT with code {rc}")
    client.subscribe("fms/commands")

def on_message(client, userdata, msg):
    print(f"📨 Received command: {msg.topic} -> {msg.payload.decode()}")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message
client.connect("mqtt", 1883, 60)
client.loop_start()
print("MQTT bridge started. Waiting for commands...")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    client.loop_stop()
    print("\nStopped.")
