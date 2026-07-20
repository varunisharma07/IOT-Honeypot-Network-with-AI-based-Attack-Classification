import time
import random
import paho.mqtt.publish as publish

devices = [
    ("ESP32-01", "iot/temperature"),
    ("Camera-01", "iot/camera"),
    ("DoorLock-01", "iot/door"),
    ("Light-01", "iot/light")
]

while True:

    device, topic = random.choice(devices)

    if topic == "iot/temperature":
        payload = f"{random.randint(20,35)}"

    elif topic == "iot/camera":
        payload = random.choice([
            "Motion Detected",
            "Online",
            "Offline"
        ])

    elif topic == "iot/door":
        payload = random.choice([
            "Locked",
            "Unlocked"
        ])

    else:
        payload = random.choice([
            "ON",
            "OFF"
        ])

    publish.single(
        topic,
        payload,
        hostname="localhost"
    )

    print(f"{device} -> {topic} : {payload}")

    time.sleep(3)
