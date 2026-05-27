#!/usr/bin/env python3
import paho.mqtt.client as mqtt
import json
import time
import threading

class InteractiveFMS:
    def __init__(self, robot_id="telezhka_001"):
        self.robot_id = robot_id
        self.client = mqtt.Client()
        self.client.on_connect = self.on_connect
        self.client.connect("localhost", 1883, 60)
        self.client.loop_start()
        print(f"✅ FMS started for {robot_id}")
        print("Управление: w (вперёд), s (стоп), a (влево), d (вправо), q (выход)")

    def on_connect(self, client, userdata, flags, rc):
        print(f"✅ Connected to MQTT broker (code: {rc})")

    def send_command(self, left, right):
        command = {
            "robot_id": self.robot_id,
            "left": left,
            "right": right,
            "timestamp": time.time()
        }
        self.client.publish("fms/robot/control", json.dumps(command))
        print(f"🚀 Command: L={left:.2f}, R={right:.2f}")

    def run(self):
        while True:
            cmd = input().strip().lower()
            if cmd == 'w':
                self.send_command(0.5, 0.5)   # вперёд
            elif cmd == 's':
                self.send_command(0.0, 0.0)   # стоп
            elif cmd == 'a':
                self.send_command(0.2, 0.4)   # поворот налево
            elif cmd == 'd':
                self.send_command(0.4, 0.2)   # поворот направо
            elif cmd == 'q':
                print("Завершение FMS")
                break
            else:
                print("Неизвестная команда. Используйте: w, a, s, d, q")

if __name__ == "__main__":
    fms = InteractiveFMS()
    try:
        fms.run()
    except KeyboardInterrupt:
        print("\nFMS остановлен")
    finally:
        fms.client.loop_stop()