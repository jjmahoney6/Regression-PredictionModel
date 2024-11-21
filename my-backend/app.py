from flask import Flask, request, jsonify
import pandas as pd
import pickle

# Load the saved model
with open("attendance_model.pkl", "rb") as f:
    model = pickle.load(f)

app = Flask(__name__)

@app.route("/")
def home():
    return "Welcome to the Attendance Prediction API!"

@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get JSON request data
        data = request.get_json()

        # Extract features
        features = {
            'event_weight': data.get('event_weight', 0),
            'weather_weight': data.get('weather_weight', 0),
            'temp_weight': data.get('temp_weight', 0),
            'prev_sales_1': data.get('prev_sales_1', 0),
            'prev_sales_2': data.get('prev_sales_2', 0),
            'rolling_mean_3': data.get('rolling_mean_3', 0),
            'day_of_week': data.get('day_of_week', 'Monday')  # Default value
        }

        # Map day_of_week to one-hot encoded features
        day_map = {
            'Fri': [1, 0, 0, 0, 0, 0],  # Adjust for your dataset
            'Sat': [0, 1, 0, 0, 0, 0],
            'Sun': [0, 0, 1, 0, 0, 0],
            'Thu': [0, 0, 0, 1, 0, 0],
            'Tue': [0, 0, 0, 0, 1, 0],
            'Wed': [0, 0, 0, 0, 0, 1]
        }
        day_encoding = day_map.get(features['day_of_week'], [0, 0, 0, 0, 0, 0])  # Default all zeros

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
        prediction = model.predict(feature_df)[0]

        # Return prediction as JSON
        return jsonify({'predicted_attendance': prediction})

    except Exception as e:
        return jsonify({'error': str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True)
