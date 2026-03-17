#!/usr/bin/env python3
"""
FMS (Fleet Management System) с поддержкой приема статуса от робота
"""
import paho.mqtt.client as mqtt
import json
import time

class SimpleFMS:
    def __init__(self, robot_id="robot_1"):
        self.robot_id = robot_id
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.on_message = self.on_message
        self.client.connect("localhost", 1883, 60)
        self.client.loop_start()
        print(f"✅ FMS started for {robot_id}")
        print("📡 Listening for robot status on topic 'robot/status'")
    
    def on_connect(self, client, userdata, flags, rc):
        print(f"✅ Connected to MQTT broker (code: {rc})")
        # Подписываемся на статус робота
        client.subscribe("robot/status")
    
    def on_message(self, client, userdata, msg):
        """Обработка входящих MQTT сообщений"""
        if msg.topic == "robot/status":
            try:
                status = json.loads(msg.payload.decode())
                print(f"\n📊 Robot status received:")
                print(f"   Robot:     {status.get('robot_id')}")
                print(f"   Battery:   {status.get('battery')}%")
                print(f"   Position:  ({status.get('x')}, {status.get('y')})")
                print(f"   Task:      {status.get('current_task')}")
                print(f"   Timestamp: {status.get('timestamp')}")
            except Exception as e:
                print(f"❌ Error parsing status: {e}")
    
    def send_command(self, left_speed, right_speed):
        """Отправка команды моторам"""
        command = {
            "robot_id": self.robot_id,
            "left": left_speed,
            "right": right_speed,
            "timestamp": time.time()
        }
        self.client.publish("fms/robot/control", json.dumps(command))
        print(f"🚀 FMS → {self.robot_id}: L={left_speed:.2f}, R={right_speed:.2f}")
    
    def move_forward(self, speed=0.5):
        """Движение вперед"""
        self.send_command(speed, speed)
    
    def turn_left(self, speed=0.4):
        """Поворот налево"""
        self.send_command(speed * 0.5, speed)
    
    def turn_right(self, speed=0.4):
        """Поворот направо"""
        self.send_command(speed, speed * 0.5)
    
    def stop(self):
        """Остановка"""
        self.send_command(0.0, 0.0)

# Тестовый сценарий
if __name__ == "__main__":
    print("=== FMS с приемом статуса ===")
    fms = SimpleFMS("telezhka_001")
    
    print("\n--- Отправка тестовых команд ---")
    input("Нажмите Enter для отправки команды 'Вперед'...")
    fms.move_forward(0.5)
    
    input("Нажмите Enter для отправки команды 'Поворот налево'...")
    fms.turn_left(0.4)
    
    input("Нажмите Enter для отправки команды 'Стоп'...")
    fms.stop()
    
    print("\n✅ Тест завершен. FMS продолжает слушать статус робота...")
    
    # Бесконечный цикл, чтобы FMS продолжал работать
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        print("\n🛑 FMS остановлен")
