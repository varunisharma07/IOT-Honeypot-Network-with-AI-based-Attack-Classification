import sqlite3
import joblib
import time


model = joblib.load("ai/attack_model.pkl")
command_encoder = joblib.load("ai/command_encoder.pkl")
attack_encoder = joblib.load("ai/attack_encoder.pkl")


def predict_attack(command):

    command = command.strip().lower()

    try:
        encoded = command_encoder.transform([command])
        encoded = encoded.reshape(-1,1)

        prediction = model.predict(encoded)

        return attack_encoder.inverse_transform(prediction)[0]

    except:
        return "Suspicious Activity"



def classify_new_attacks():

    conn = sqlite3.connect("database/honeypot.db")
    cursor = conn.cursor()


    cursor.execute("""
        SELECT id, command
        FROM attacks
        WHERE attack_type IS NULL
    """)


    rows = cursor.fetchall()


    for attack in rows:

        attack_id = attack[0]
        command = attack[1]


        attack_type = predict_attack(command)


        cursor.execute("""
            UPDATE attacks
            SET attack_type=?
            WHERE id=?
        """,
        (attack_type, attack_id))


        print(
            f"{command} --> {attack_type}"
        )


    conn.commit()
    conn.close()



print("AI Attack Classifier Started...")


while True:

    classify_new_attacks()

    time.sleep(5)