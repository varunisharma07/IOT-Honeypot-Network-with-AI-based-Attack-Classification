import sqlite3


conn = sqlite3.connect("database/honeypot.db")
cursor = conn.cursor()


def classify(command):

    command = command.lower()


    if command in ["whoami", "cat /etc/passwd"]:
        return "User Enumeration"


    elif command in ["uname -a", "pwd", "ls"]:
        return "Reconnaissance"


    elif command == "ps":
        return "Process Discovery"


    elif command in ["on", "off", "locked", "unlocked"]:
        return "IoT Command Manipulation"


    elif command in ["motion detected", "online", "offline"]:
        return "IoT Sensor Activity"


    elif command.isdigit():
        return "Normal IoT Data"


    else:
        return "Suspicious Activity"



cursor.execute("SELECT id, command FROM attacks")


rows = cursor.fetchall()


for row in rows:

    attack_id = row[0]
    command = row[1]

    attack_type = classify(command)


    cursor.execute(
        """
        UPDATE attacks
        SET attack_type=?
        WHERE id=?
        """,
        (attack_type, attack_id)
    )


conn.commit()
conn.close()


print("Attack classification completed")
