#!/usr/bin/env python3
"""MQTT 用戶端範例"""

import paho.mqtt.client as mqtt
import time
import json

BROKER = "broker.mqtt-dashboard.com"
PORT = 1883
TOPIC = "aipt/2015/11/sensor"

received_messages = []

def on_connect(client, userdata, flags, rc):
    if rc == 0:
        print(f"Connected to {BROKER}:{PORT}")
        client.subscribe(TOPIC)
        print(f"Subscribed to {TOPIC}")
    else:
        print(f"Connection failed with code {rc}")

def on_message(client, userdata, msg):
    print(f"Received: {msg.topic} - {msg.payload.decode()}")
    received_messages.append(msg.payload.decode())

def on_publish(client, userdata, mid):
    print(f"Published message {mid}")

def demo():
    print("=" * 60)
    print("MQTT Client Demo")
    print("=" * 60)

    client = mqtt.Client()
    client.on_connect = on_connect
    client.on_message = on_message
    client.on_publish = on_publish

    print(f"\nConnecting to {BROKER}...")
    client.connect(BROKER, PORT, 60)

    client.loop_start()

    print("\nPublishing sensor data...")
    for i in range(5):
        data = {
            "sensor_id": "RPi_001",
            "temperature": 20 + i,
            "humidity": 50 + i * 2
        }
        client.publish(TOPIC, json.dumps(data))
        print(f"Published: {data}")
        time.sleep(2)

    print(f"\nReceived {len(received_messages)} messages")

    client.loop_stop()
    client.disconnect()

    print("\nDone!")

if __name__ == "__main__":
    demo()