import sqlite3
import paho.mqtt.client as mqtt
from datetime import datetime

DATABASE = "database/honeypot.db"

# Connect to database
conn = sqlite3.connect(DATABASE, check_same_thread=False)
cursor = conn.cursor()


def on_connect(client, userdata, flags, reason_code, properties=None):
    print("Connected to MQTT Broker")
    client.subscribe("iot/#")


def on_message(client, userdata, msg):
    topic = msg.topic
    payload = msg.payload.decode()

    print(f"{topic} -> {payload}")

    cursor.execute("""
    INSERT INTO iot_data
    (timestamp, topic, payload)
    VALUES (?, ?, ?)
    """, (
    datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
    topic,
    payload
    ))

    conn.commit()


client = mqtt.Client(mqtt.CallbackAPIVersion.VERSION2)

client.on_connect = on_connect
client.on_message = on_message

client.connect("localhost", 1883, 60)

client.loop_forever()
