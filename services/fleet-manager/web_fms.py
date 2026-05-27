#!/usr/bin/env python3
import json
import time
from fastapi import FastAPI, Request
from fastapi.responses import HTMLResponse
import paho.mqtt.client as mqtt
import uvicorn

app = FastAPI()

# MQTT настройки
MQTT_BROKER = "localhost"
MQTT_PORT = 1883
MQTT_TOPIC = "fms/robot/control"

client = mqtt.Client()
client.connect(MQTT_BROKER, MQTT_PORT, 60)
client.loop_start()

def send_command(left, right):
    msg = {
        "robot_id": "telezhka_001",
        "left": left,
        "right": right,
        "timestamp": time.time()
    }
    client.publish(MQTT_TOPIC, json.dumps(msg))
    print(f"Command sent: L={left}, R={right}")

# HTML страница прямо в коде (чтобы не зависеть от шаблонов)
html_content = """
<!DOCTYPE html>
<html>
<head>
    <title>FMS Robot Control</title>
    <style>
        body { font-family: Arial; text-align: center; margin-top: 50px; background: #f0f0f0; }
        .container { background: white; width: 400px; margin: 0 auto; padding: 30px; border-radius: 15px; box-shadow: 0 4px 8px rgba(0,0,0,0.2); }
        button { font-size: 24px; padding: 15px 25px; margin: 10px; border: none; border-radius: 10px; cursor: pointer; transition: 0.2s; }
        button.forward { background: #4CAF50; color: white; }
        button.backward { background: #f44336; color: white; }
        button.left, button.right { background: #FF9800; color: white; }
        button.stop { background: #9E9E9E; color: white; }
        button:hover { opacity: 0.8; transform: scale(1.05); }
        .row { margin: 20px 0; }
        h1 { color: #333; }
        p { color: #666; }
    </style>
</head>
<body>
<div class="container">
    <h1>Управление роботом</h1>
    <p>Нажимайте кнопки для отправки команд</p>
    <div class="row"><button class="forward" onclick="sendCommand('forward')">⬆ Вперёд</button></div>
    <div class="row">
        <button class="left" onclick="sendCommand('left')">↩ Левый</button>
        <button class="stop" onclick="sendCommand('stop')">⏹ Стоп</button>
        <button class="right" onclick="sendCommand('right')">↪ Правый</button>
    </div>
    <div class="row"><button class="backward" onclick="sendCommand('backward')">⬇ Назад</button></div>
    <div id="status" style="margin-top: 20px; font-size: 14px; color: #333;">Готов</div>
</div>
<script>
    async function sendCommand(cmd) {
        const statusDiv = document.getElementById('status');
        statusDiv.innerText = `Отправка: ${cmd} ...`;
        try {
            const response = await fetch(`/cmd/${cmd}`, { method: 'POST' });
            const data = await response.json();
            if (data.status === 'ok') statusDiv.innerText = `✅ Команда ${cmd} выполнена`;
            else statusDiv.innerText = `❌ Ошибка: ${data.error}`;
        } catch (err) {
            statusDiv.innerText = `❌ Ошибка соединения: ${err}`;
        }
        setTimeout(() => statusDiv.innerText = 'Готов', 1500);
    }
</script>
</body>
</html>
"""

@app.get("/", response_class=HTMLResponse)
async def index():
    return html_content

@app.post("/cmd/{direction}")
async def control(direction: str):
    if direction == "forward":
        send_command(0.5, 0.5)
    elif direction == "backward":
        send_command(-0.5, -0.5)
    elif direction == "left":
        send_command(0.2, 0.4)
    elif direction == "right":
        send_command(0.4, 0.2)
    elif direction == "stop":
        send_command(0.0, 0.0)
    else:
        return {"error": "unknown command"}
    return {"status": "ok"}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)
