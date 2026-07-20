import joblib
import pandas as pd
from sklearn.preprocessing import LabelEncoder

# Load trained model
model = joblib.load("ai/model.pkl")

# Temporary encoder
encoder = LabelEncoder()


def predict_attack(eventid, src_ip, username, password, command):

    data = pd.DataFrame({
        "eventid": [eventid],
        "src_ip": [src_ip],
        "username": [username],
        "password": [password],
        "command": [command]
    })

    # Encode input
    for col in data.columns:
        data[col] = encoder.fit_transform(data[col].astype(str))

    prediction = model.predict(data)[0]

    probability = max(model.predict_proba(data)[0])
    confidence = round(probability * 100, 2)

    if prediction == 0:
        threat = "🟢 LOW"
        score = 25

    elif prediction == 1:
        threat = "🟠 MEDIUM"
        score = 60

    else:
        threat = "🔴 HIGH"
        score = 95

    return {
        "threat": threat,
        "confidence": f"{confidence}%",
        "score": score
    }


# Test
if __name__ == "__main__":

    result = predict_attack(
        eventid="cowrie.command.input",
        src_ip="172.19.0.1",
        username="root",
        password="adadadmin",
        command="ls"
    )

    print(result)