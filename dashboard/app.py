from flask import Flask, render_template, jsonify, send_file
import sqlite3
import pandas as pd
import os
import sys
import requests
# Allow importing from project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from ai.predict import predict_attack

app = Flask(__name__)

DATABASE = "database/honeypot.db"


# ============================================
# Database Connection
# ============================================

def get_db():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    return conn


# ============================================
# Dashboard
# ============================================

@app.route("/")
def index():

    conn = get_db()

    cur = conn.cursor()

    cur.execute("SELECT * FROM attacks ORDER BY id DESC")

    rows = cur.fetchall()

    cur.execute("""
    SELECT *
    FROM iot_data
    ORDER BY id DESC
    LIMIT 20
    """)

    iot_logs = cur.fetchall()

    attacks = []

    low = 0
    medium = 0
    high = 0

    for row in rows:

        row = dict(row)

        result = predict_attack(

            row["eventid"],
            row["src_ip"],
            row["username"],
            row["password"],
            row["command"]

        )

        row["threat"] = result["threat"]
        row["confidence"] = result["confidence"]
        row["score"] = result["score"]

        if "LOW" in result["threat"]:
            low += 1

        elif "MEDIUM" in result["threat"]:
            medium += 1

        else:
            high += 1

        attacks.append(row)

    # ------------------------------------

    cur.execute("SELECT COUNT(*) FROM attacks")
    total_attacks = cur.fetchone()[0]

    cur.execute("SELECT COUNT(DISTINCT src_ip) FROM attacks")
    unique_ips = cur.fetchone()[0]

    cur.execute("""

        SELECT COUNT(*)

        FROM attacks

        WHERE username!=''

    """)

    login_attempts = cur.fetchone()[0]

    

    cur.execute("""

        SELECT COUNT(*)

        FROM attacks

        WHERE command!=''

    """)

    commands = cur.fetchone()[0]

    cur.execute("""

        SELECT src_ip,
               COUNT(*) total

        FROM attacks

        GROUP BY src_ip

        ORDER BY total DESC

        LIMIT 1

    """)

    top = cur.fetchone()

    top_ip = top["src_ip"] if top else "N/A"

    conn.close()

    return render_template(

        "index.html",

        attacks=attacks,
        iot_logs=iot_logs,

        total_attacks=total_attacks,

        unique_ips=unique_ips,

        login_attempts=login_attempts,

        commands=commands,

        top_ip=top_ip,

        low=low,

        medium=medium,

        high=high

    )


# ============================================
# API Statistics
# ============================================

@app.route("/api/stats")
def stats():

    conn = get_db()

    cur = conn.cursor()

    cur.execute("SELECT COUNT(*) FROM attacks")
    total = cur.fetchone()[0]

    cur.execute("SELECT COUNT(DISTINCT src_ip) FROM attacks")
    ips = cur.fetchone()[0]

    cur.execute("""

        SELECT COUNT(*)

        FROM attacks

        WHERE username!=''

    """)

    logins = cur.fetchone()[0]

    cur.execute("""

        SELECT COUNT(*)

        FROM attacks

        WHERE command!=''

    """)

    cmds = cur.fetchone()[0]

    conn.close()

    return jsonify({

        "total": total,
        "ips": ips,
        "logins": logins,
        "commands": cmds

    })


# ============================================
# API Attacks
# ============================================

@app.route("/api/attacks")
def api_attacks():

    conn = get_db()

    cur = conn.cursor()

    cur.execute("""

        SELECT *

        FROM attacks

        ORDER BY id DESC

        LIMIT 50

    """)

    rows = []

    for r in cur.fetchall():

        r = dict(r)

        result = predict_attack(

            r["eventid"],
            r["src_ip"],
            r["username"],
            r["password"],
            r["command"]

        )

        r["threat"] = result["threat"]
        r["confidence"] = result["confidence"]

        rows.append(r)

    conn.close()

    return jsonify(rows)


# ============================================
# Export CSV
# ============================================

@app.route("/export")
def export():

    conn = get_db()

    df = pd.read_sql_query(

        "SELECT * FROM attacks",

        conn

    )

    conn.close()

    os.makedirs("exports", exist_ok=True)

    filename = "exports/attacks.csv"

    df.to_csv(filename, index=False)

    return send_file(

        filename,

        as_attachment=True

    )


# ============================================
# Search
# ============================================

@app.route("/search/<keyword>")
def search(keyword):

    conn = get_db()

    cur = conn.cursor()

    cur.execute("""

        SELECT *

        FROM attacks

        WHERE

        src_ip LIKE ?

        OR username LIKE ?

        OR command LIKE ?

        ORDER BY id DESC

    """, (

        f"%{keyword}%",

        f"%{keyword}%",

        f"%{keyword}%"

    ))

    rows = []

    for r in cur.fetchall():

        r = dict(r)

        result = predict_attack(

            r["eventid"],
            r["src_ip"],
            r["username"],
            r["password"],
            r["command"]

        )

        r["threat"] = result["threat"]
        r["confidence"] = result["confidence"]

        rows.append(r)

    conn.close()

    return jsonify(rows)


# ============================================
# Run
# ============================================


@app.route("/api/map")
def map_data():

    conn = sqlite3.connect(DATABASE)
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    cur.execute("""
        SELECT DISTINCT src_ip
        FROM attacks
    """)

    ips = cur.fetchall()
    conn.close()

    locations = []

    for row in ips:

        ip = row["src_ip"]

        # Skip private IPs
        if ip.startswith("127.") or ip.startswith("172.") or ip.startswith("192.168") or ip.startswith("10."):
            continue

        try:
            r = requests.get(f"http://ip-api.com/json/{ip}", timeout=5)
            data = r.json()

            if data["status"] == "success":

                locations.append({
                    "ip": ip,
                    "country": data["country"],
                    "lat": data["lat"],
                    "lon": data["lon"]
                })

        except:
            pass

    return jsonify(locations)


@app.route("/api/latest")
def latest_attack():

    conn = get_db()

    cur = conn.cursor()

    cur.execute("""

        SELECT *

        FROM attacks

        ORDER BY id DESC

        LIMIT 1

    """)

    row = cur.fetchone()

    conn.close()

    if row:

        row = dict(row)

        result = predict_attack(
            row["eventid"],
            row["src_ip"],
            row["username"],
            row["password"],
            row["command"]
        )

        row["threat"] = result["threat"]

        return jsonify(row)

    return jsonify({})

@app.route("/api/iot_status")
def iot_status():

    conn = get_db()
    cur = conn.cursor()

    devices = {}

    for topic in [
        "iot/temperature",
        "iot/light",
        "iot/door",
        "iot/camera"
    ]:

        cur.execute("""
            SELECT payload
            FROM iot_data
            WHERE topic=?
            ORDER BY id DESC
            LIMIT 1
        """, (topic,))

        row = cur.fetchone()

        if row:
            devices[topic] = row["payload"]
        else:
            devices[topic] = "N/A"

    conn.close()

    return jsonify(devices)

@app.route("/api/temperature")
def temperature():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT timestamp, payload
        FROM iot_data
        WHERE topic='iot/temperature'
        ORDER BY id DESC
        LIMIT 20
    """)

    rows = cur.fetchall()
    conn.close()

    data = []

    for row in reversed(rows):
        try:
            data.append({
                "time": row["timestamp"][-8:],
                "value": int(row["payload"])
            })
        except:
            pass

    return jsonify(data)

@app.route("/api/iot_alerts")
def iot_alerts():

    conn = get_db()
    cur = conn.cursor()

    cur.execute("""
        SELECT topic, payload
        FROM iot_data
        ORDER BY id DESC
        LIMIT 20
    """)

    rows = cur.fetchall()
    conn.close()

    alerts = []

    for row in rows:

        topic = row["topic"]
        payload = row["payload"]

        if topic == "iot/temperature":
            try:
                if int(payload) > 40:
                    alerts.append("🔥 High Temperature Detected")
            except:
                pass

        elif topic == "iot/door":
            if payload == "Unlocked":
                alerts.append("🚪 Door Unlocked")

        elif topic == "iot/camera":
            if payload == "Offline":
                alerts.append("📷 Camera Offline")

    return jsonify(alerts)

@app.route("/api/timeline")
def timeline():

    conn = get_db()
    cur = conn.cursor()

    timeline = []

    # Honeypot events
    cur.execute("""
        SELECT timestamp,eventid,src_ip
        FROM attacks
        ORDER BY id DESC
        LIMIT 20
    """)

    for row in cur.fetchall():

        timeline.append({
            "time": row["timestamp"],
            "icon": "🔴",
            "event": f'{row["eventid"]} ({row["src_ip"]})'
        })

    # IoT events
    cur.execute("""
        SELECT timestamp,topic,payload
        FROM iot_data
        ORDER BY id DESC
        LIMIT 20
    """)

    for row in cur.fetchall():

        icon = "📡"

        if row["topic"] == "iot/temperature":
            icon = "🌡"

        elif row["topic"] == "iot/light":
            icon = "💡"

        elif row["topic"] == "iot/door":
            icon = "🚪"

        elif row["topic"] == "iot/camera":
            icon = "📷"

        timeline.append({
            "time": row["timestamp"],
            "icon": icon,
            "event": row["payload"]
        })

    conn.close()

    timeline.sort(
        key=lambda x: x["time"],
        reverse=True
    )

    return jsonify(timeline[:30])
# ============================================
# Run
# ============================================

if __name__ == "__main__":

    app.run(
        debug=True,
        host="0.0.0.0",
        port=5000
    )


