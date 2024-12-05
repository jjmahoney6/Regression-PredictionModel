from flask import Flask, request, jsonify
from flask_cors import CORS
import pickle

app = Flask(__name__)
CORS(app)

# Load pre-trained model
with open("attendance_model.pkl", "rb") as f:
    model = pickle.load(f)

# Maps for categorical inputs
weather_map = {'Sunny': 0, 'Rainy': 1, 'Cloudy': 2}
event_map = {'Sports': 0, 'Concert': 1, 'Conference': 2}
day_map = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}

@app.route('/predict', methods=['POST'])
def predict():
    try:
        data = request.json
        weather = data.get('weather')
        event = data.get('event')
        day_of_week = data.get('day_of_week')

        if not weather or not event or not day_of_week:
            return jsonify({'error': 'Missing input fields'}), 400

        # Convert inputs to numerical values
        features = [
            weather_map[weather],
            event_map[event],
            day_map[day_of_week],
        ]

        # Predict
        prediction = model.predict([features])[0]
        return jsonify({'predicted_attendance': prediction})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == '__main__':
    app.run(debug=True)
