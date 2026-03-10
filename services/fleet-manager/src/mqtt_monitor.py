#!/usr/bin/env python3
"""
Мониторинг MQTT сообщений
Показывает все сообщения в системе в реальном времени
"""
import paho.mqtt.client as mqtt
import json
from datetime import datetime

def on_connect(client, userdata, flags, rc):
    print(f"✅ Подключен к MQTT брокеру (код: {rc})")
    # Подписываемся на все топики роботов
    client.subscribe("robot/#")
    client.subscribe("fms/#")
    print("📡 Слушаем топики: robot/#, fms/#")

def on_message(client, userdata, msg):
    timestamp = datetime.now().strftime("%H:%M:%S.%f")[:-3]
    topic = msg.topic
    
    try:
        # Пытаемся разобрать как JSON
        data = json.loads(msg.payload.decode())
        print(f"[{timestamp}] {topic}: {json.dumps(data, indent=2)}")
    except:
        # Если не JSON, выводим как текст
        print(f"[{timestamp}] {topic}: {msg.payload.decode()}")

print("=== MQTT Monitor ===")
print("Отображает все сообщения в системе")
print("Для выхода: Ctrl+C\n")

client = mqtt.Client()
client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)
client.loop_forever()
