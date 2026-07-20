# 🛡️ AI-Powered IoT Honeypot Network with Attack Classification

## 📌 Overview

This project is an AI-powered cybersecurity monitoring system that combines an IoT device simulator, MQTT communication, a Cowrie SSH honeypot, machine learning-based threat classification, and a Flask web dashboard for real-time attack monitoring.

---

## ✨ Features

- 🔐 Cowrie SSH Honeypot
- 📡 IoT Device Simulator using MQTT
- 📥 MQTT Collector
- 🤖 AI-based Threat Classification
- 📊 Interactive Flask Dashboard
- 🌍 World Attack Map
- 🔔 Real-Time Attack Notifications
- 📈 Live Charts
- 📤 CSV Export
- 🔍 Search Functionality
- 🕒 Unified Security Timeline
- 💾 SQLite Database

---

## 🛠 Technologies Used

- Python
- Flask
- SQLite
- MQTT (Mosquitto)
- Cowrie Honeypot
- Docker
- Machine Learning (Scikit-learn)
- HTML
- CSS
- JavaScript
- Chart.js
- Leaflet.js

---

## 📂 Project Structure

```
IOT-Honeypot-Network/
│
├── ai/
├── collector/
├── dashboard/
├── simulator/
├── database/
├── docker/
├── requirements.txt
├── README.md
└── .gitignore
```

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/varunisharma07/IOT-Honeypot-Network-with-AI-based-Attack-Classification.git
```

Move into the project:

```bash
cd IOT-Honeypot-Network-with-AI-based-Attack-Classification
```

Install dependencies:

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Project

Start the MQTT broker:

```bash
mosquitto
```

Run the IoT simulator:

```bash
python3 simulator/iot_device.py
```

Run the MQTT collector:

```bash
python3 collector/mqtt_collector.py
```

Run the dashboard:

```bash
python3 dashboard/app.py
```

Open:

```
http://127.0.0.1:5000
```

---

## 📷 Screenshots

Add screenshots here after uploading them.

---

## 👩‍💻 Author

**Varuni Sharma**

B.Tech CSE Student

Cybersecurity Enthusiast
