from flask import Flask, request, jsonify, render_template
import numpy as np
import tensorflow as tf
import pickle
import json

app = Flask(__name__)

# ===== Load Model and Label Encoder =====
MODEL_PATH = r'C:\Users\Chandramouli bandaru\OneDrive\Desktop\Weather prediction\weatherPrediction.keras'
LABEL_ENCODER_PATH = r'C:\Users\Chandramouli bandaru\OneDrive\Desktop\Weather prediction\label_encoder.pkl'

# Load trained LSTM model
model = tf.keras.models.load_model(MODEL_PATH)

# Load saved label encoder
with open(LABEL_ENCODER_PATH, 'rb') as f:
    lb = pickle.load(f)

# ===== Routes =====

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict_weather():
    try:
        data = request.get_json()

        # Expecting 24×7 data from frontend
        features = np.array(data['features'])  # shape (24, 7)
        if features.shape != (24, 7):
            return jsonify({'error': 'Input shape must be (24, 7)'}), 400

        # Expand dims for batch (1, 24, 7)
        input_seq = np.expand_dims(features, axis=0)

        # Predict
        prediction = model.predict(input_seq)
        predicted_index = np.argmax(prediction)
        predicted_class = lb.inverse_transform([predicted_index])[0]

        return jsonify({'predicted_weather': predicted_class})

    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
