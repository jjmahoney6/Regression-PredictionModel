from flask import Flask, request, jsonify
from flask_cors import CORS 
import pandas as pd
import pickle

# Load the saved model
with open("attendance_model.pkl", "rb") as f:
    model = pickle.load(f)

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}}, supports_credentials=True)

# Mapping weather and event to numeric weights

day_map = {
    'friday': [1, 0, 0, 0, 0, 0],
    'saturday': [0, 1, 0, 0, 0, 0],
    'sunday': [0, 0, 1, 0, 0, 0],
    'thursday': [0, 0, 0, 1, 0, 0],
    'tuesday': [0, 0, 0, 0, 1, 0],
    'wednesday': [0, 0, 0, 0, 0, 1],
}

weather_map = {
    'sunny': 1,
    'clear': 2,
    'partly cloudy': 3,
    'cloudy': 4,
    'overcast': 5,
    'drizzle': 6,
    'rain': 7
}

event_map = {
    'opening day': 1,
    'fireworks': 2,
    'promotions': 3,
    'regular': 4,
    'none': 5
}

@app.route("/")
def home():
    return "Welcome to the Attendance Prediction API!"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get JSON request data
        data = request.get_json()

        if 'weather' not in data or 'event' not in data or 'day_of_week' not in data:
            return jsonify({'error': 'Missing required fields: weather, event, or day_of_week'}), 400
        
        weather = data.get('weather', '').lower()
        event = data.get('event', '').lower()
        day_of_week = data.get('day_of_week', '').lower()
        
        if weather not in weather_map or event not in event_map or day_of_week not in day_map:
            return jsonify({'error': 'Invalid values for weather, event, or day_of_week'}), 400

        # Extract features
        features = {
            'weather_weight': weather_map[weather],
            'event_weight': event_map[event],
            'temp_weight': data.get('temp_weight', 0),
            'prev_sales_1': data.get('prev_sales_1', 0),
            'prev_sales_2': data.get('prev_sales_2', 0),
            'rolling_mean_3': data.get('rolling_mean_3', 0),
        }

        day_encoding = day_map.get(day_of_week)  # Default all zeros

        # Construct the feature array
        feature_array = [
            features['event_weight'],
            features['weather_weight'],
            features['temp_weight'],
            features['prev_sales_1'],
            features['prev_sales_2'],
            features['rolling_mean_3']
        ] + day_encoding  # Append the encoded day of the week

        # Debugging
        print("Feature array for prediction:", feature_array)
        print("Number of features:", len(feature_array))

        # Validate feature length
        if len(feature_array) != 12:  # Ensure it matches the expected number of features
            return jsonify({'error': f'Feature mismatch: Expected 12 features, got {len(feature_array)}'}), 400

        # Convert to DataFrame for prediction
        feature_df = pd.DataFrame([feature_array])

        # Perform prediction
        try:
            prediction = model.predict(feature_df)[0]
        except Exception as e:
            return jsonify({'error': f'Prediction failed: {str(e)}'}), 500


        # Return prediction as JSON
        return jsonify({'predicted_attendance': prediction})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
