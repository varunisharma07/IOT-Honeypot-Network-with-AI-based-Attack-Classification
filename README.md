# AI-Powered IoT Honeypot Network with Attack Classification

##  Overview

This project is an AI-powered cybersecurity monitoring system that combines an IoT device simulator, MQTT communication, a Cowrie SSH honeypot, machine learning-based threat classification, and a Flask web dashboard for real-time attack monitoring.

---

##  Features

-  Cowrie SSH Honeypot
-  IoT Device Simulator using MQTT
-  MQTT Collector
-  AI-based Threat Classification
-  Interactive Flask Dashboard
-  World Attack Map
-  Real-Time Attack Notifications
-  Live Charts
-  CSV Export
-  Search Functionality
-  Unified Security Timeline
-  SQLite Database

---

##  Technologies Used

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

##  Project Structure

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

##  Installation

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

##  Run the Project

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
## System Architecture
                     +----------------------+
                     |     IoT Devices      |
                     |----------------------|
                     | Temperature Sensor   |
                     | Light Sensor         |
                     | Door Sensor          |
                     | Camera Device        |
                     +----------+-----------+
                                |
                                |
                                v
                     +----------------------+
                     |     MQTT Broker      |
                     |----------------------|
                     | Mosquitto MQTT       |
                     | IoT Message Routing  |
                     +----------+-----------+
                                |
                                |
                                v
                +--------------------------------+
                |       Data Collection Layer     |
                |--------------------------------|
                | mqtt_collector.py               |
                | MQTT Subscriber                |
                | Captures IoT Events            |
                +---------------+----------------+
                                |
                                |
                                v
                +--------------------------------+
                |       Honeypot Database        |
                |--------------------------------|
                | SQLite (honeypot.db)            |
                |                                |
                | Tables:                        |
                | - attacks                      |
                | - iot_data                     |
                +---------------+----------------+
                                |
              +-----------------+------------------+
              |                                    |
              v                                    v

    +-----------------------+          +----------------------+
    |  AI Attack Classifier |          |  Flask Dashboard     |
    |-----------------------|          |----------------------|
    | Random Forest Model   |          | SOC Monitoring UI    |
    | Feature Processing    |          | Real-Time Analytics  |
    | Attack Prediction     |          | Attack Visualization|
    +-----------+-----------+          +----------+-----------+
                |                                 |
                |                                 |
                v                                 v

    +-----------------------+          +----------------------+
    | Attack Classification |          | Security Monitoring  |
    |-----------------------|          |----------------------|
    | Reconnaissance       |          | Attack Timeline      |
    | User Enumeration     |          | IoT Status           |
    | Process Discovery    |          | Threat Levels        |
    | Suspicious Activity  |          | Reports Export       |
    | IoT Manipulation     |          | Attack Statistics    |
    +-----------------------+          +----------------------+


                                |
                                v

                     +----------------------+
                     | Security Analyst     |
                     |----------------------|
                     | Monitors attacks    |
                     | Analyzes threats    |
                     | Generates reports   |
                     +----------------------+

---

## 🔹 Architecture Components

### 1. IoT Simulation Layer
- Simulates IoT devices such as:
  - Temperature sensors
  - Light sensors
  - Door sensors
  - Camera devices
- Generates normal and malicious IoT activity.

### 2. MQTT Communication Layer
- Uses MQTT protocol for IoT communication.
- Mosquitto broker handles message exchange between devices and collector.

### 3. Honeypot Collection Layer
- Captures attacker interactions.
- Collects:
  - Commands executed
  - Login attempts
  - Source IP addresses
  - IoT device events

### 4. Database Layer
SQLite database stores:

**attacks table**
- Timestamp
- Source IP
- Username
- Password
- Commands
- Attack Type

**iot_data table**
- Timestamp
- Topic
- Payload


### 5. AI Attack Classification Layer

Machine Learning model analyzes collected activity and classifies attacks into:

- 🔴 Suspicious Activity
- 🔵 Reconnaissance
- 🟡 User Enumeration
- 🟣 Process Discovery
- 🟢 IoT Command Manipulation
- 🟠 IoT Sensor Activity
- ⚪ Normal IoT Data


### 6. Dashboard Layer

Flask-based Security Operations Dashboard provides:

- Total attacks detected
- Unique attackers
- Attack type distribution
- Threat analysis
- IoT device monitoring
- Attack timeline
- Data export reports


### 7. Security Analyst Layer

The analyst can:

- Monitor real-time attacks
- Analyze attacker behavior
- Identify attack patterns
- Generate security reports
---

## Author

**Varuni Sharma**

B.Tech CSE Student

Cybersecurity Enthusiast
