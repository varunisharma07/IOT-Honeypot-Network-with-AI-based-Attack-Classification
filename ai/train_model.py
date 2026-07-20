import sqlite3
import pandas as pd
import joblib

from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier

# --------------------------
# Load database
# --------------------------

conn = sqlite3.connect("database/honeypot.db")
df = pd.read_sql_query("SELECT * FROM attacks", conn)
conn.close()

df = df.fillna("Unknown")

# --------------------------
# Create labels
# --------------------------

dangerous = [
    "wget","curl","bash","python","perl",
    "chmod","scp","ssh","busybox","nc"
]

medium = [
    "cat","uname","ps","ifconfig","ip","netstat"
]

def threat_level(command):

    command = str(command).lower()

    for c in dangerous:
        if c in command:
            return 2

    for c in medium:
        if c in command:
            return 1

    return 0

df["threat"] = df["command"].apply(threat_level)

# --------------------------
# Encode features
# --------------------------

encoders = {}

for col in [
    "eventid",
    "src_ip",
    "username",
    "password",
    "command"
]:

    encoder = LabelEncoder()

    df[col] = encoder.fit_transform(df[col].astype(str))

    encoders[col] = encoder

# --------------------------
# Features
# --------------------------

X = df[
    [
        "eventid",
        "src_ip",
        "username",
        "password",
        "command"
    ]
]

y = df["threat"]

# --------------------------
# Train model
# --------------------------

model = RandomForestClassifier(
    n_estimators=200,
    random_state=42
)

model.fit(X, y)

# --------------------------
# Save everything
# --------------------------

joblib.dump(model, "ai/model.pkl")
joblib.dump(encoders, "ai/encoders.pkl")

print("\n==============================")
print("AI Training Completed")
print("==============================")

print("Samples :", len(df))
print("Low     :", (y==0).sum())
print("Medium  :", (y==1).sum())
print("High    :", (y==2).sum())

print("\nSaved:")
print("✔ ai/model.pkl")
print("✔ ai/encoders.pkl")