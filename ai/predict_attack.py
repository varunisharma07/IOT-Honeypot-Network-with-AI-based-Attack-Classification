import joblib


# Load trained model
model = joblib.load("ai/attack_model.pkl")

# Load encoders
command_encoder = joblib.load("ai/command_encoder.pkl")
attack_encoder = joblib.load("ai/attack_encoder.pkl")


def predict_attack(command):

    # Convert command into number
    command = command.strip().lower()
    command_encoded = command_encoder.transform([command])

    # Reshape for model
    command_encoded = command_encoded.reshape(-1, 1)

    # Prediction
    prediction = model.predict(command_encoded)

    # Convert number back to attack name
    attack_type = attack_encoder.inverse_transform(prediction)

    return attack_type[0]


# Test commands

while True:

    command = input("\nEnter command (type exit to quit): ")

    if command.lower() == "exit":
        break

    result = predict_attack(command)

    print("Predicted Attack Type:", result)
