import sqlite3
import pandas as pd
import joblib

from sklearn.preprocessing import LabelEncoder
from sklearn.ensemble import RandomForestClassifier


# --------------------------
# Load database
# --------------------------

conn = sqlite3.connect("database/honeypot.db")

df = pd.read_sql_query(
    "SELECT command, attack_type FROM attacks",
    conn
)

df["command"] = df["command"].str.strip().str.lower()


conn.close()


print(df.head())


# --------------------------
# Prepare data
# --------------------------

# --------------------------
# Prepare data
# --------------------------

X = df["command"]
y = df["attack_type"]


# Command encoder
command_encoder = LabelEncoder()

X_encoded = command_encoder.fit_transform(X)


# Attack type encoder
attack_encoder = LabelEncoder()

y_encoded = attack_encoder.fit_transform(y)


# Reshape input
X_encoded = X_encoded.reshape(-1,1)

# --------------------------
# Train model
# --------------------------

model = RandomForestClassifier(
    n_estimators=100,
    random_state=42
)

model.fit(
    X_encoded,
    y_encoded
)


# --------------------------
# Save model
# --------------------------

joblib.dump(model, "ai/attack_model.pkl")

joblib.dump(
    command_encoder,
    "ai/command_encoder.pkl"
)

joblib.dump(
    attack_encoder,
    "ai/attack_encoder.pkl"
)


print("Model trained successfully!")