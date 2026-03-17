#!/usr/bin/env python3
"""
Простая система управления флотом (Fleet Management System)
Отправляет команды роботам через MQTT
"""
import paho.mqtt.client as mqtt
import json
import time

class SimpleFMS:
    def __init__(self, robot_id="robot_1"):
        self.robot_id = robot_id
        self.client = mqtt.Client()
        self.client.connect("localhost", 1883, 60)
        self.client.loop_start()
        print(f"✅ FMS started for {robot_id}")
    
    def send_command(self, left_speed, right_speed):
        """Отправка команды моторам конкретного робота"""
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
    
    def turn_left(self, speed=0.3):
        """Поворот налево"""
        self.send_command(speed * 0.5, speed)
    
    def turn_right(self, speed=0.3):
        """Поворот направо"""
        self.send_command(speed, speed * 0.5)
    
    def stop(self):
        """Остановка"""
        self.send_command(0.0, 0.0)

# Тестовый сценарий
if __name__ == "__main__":
    print("=== Тест системы управления флотом ===")
    fms = SimpleFMS("telezhka_001")
    
    print("1. Вперед на 50%...")
    fms.move_forward(0.5)
    time.sleep(2)
    
    print("2. Поворот налево...")
    fms.turn_left(0.4)
    time.sleep(2)
    
    print("3. Поворот направо...")
    fms.turn_right(0.4)
    time.sleep(2)
    
    print("4. Остановка...")
    fms.stop()
    
    print("✅ Тест завершен!")
