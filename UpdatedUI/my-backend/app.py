from flask import Flask, jsonify, request
from flask_cors import CORS  # Import the CORS extension
import pandas as pd
import pickle

# Load the saved model
# with open("attendance_model.pkl", "rb") as f:
with open("sum_model.pkl", "rb") as f:
    model = pickle.load(f)
    print(type(model))

app = Flask(__name__)

# Set up CORS to allow all origins
CORS(app)

weather_conditions = {
    'Sunny': 400,
    'Clear': 300,
    'Partly Cloudy': 200,
    'Cloudy': 100,
    'Overcast': 0,
    'Drizzle': 0,
    'Rain': -100
}

event_types = {
    'Opening Day': 2543,
    'Fireworks': 1234,
    'Promotions': 403,
    'Regular': 302,
    'None': 50
}

temperature_bins = {
    (1, 10): 20,
    (11, 20): 20,
    (21, 30): 21,
    (31, 40): 41,
    (41, 50): 321,
    (51, 60): 345,
    (61, 70): 432,
    (71, 80): 432,
    (81, 90): 543,
    (91, 100): 543,
    (101, 110): 567
}

def get_weight(temperature, bins):
    for bin_range, weight in bins.items():
        if bin_range[0] <= temperature <= bin_range[1]:
            return weight
    return 100  # Return None if the temperature is out of all ranges

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json

    # Extract features
    features = {
        'event_weight': data.get('event', 1),
        'weather_weight': data.get('weather', 1),
        'temp_weight': float(data.get('temperature', 95)),
        'prev_sales_1': data.get('prev_sales_1', 100),
        'prev_sales_2': data.get('prev_sales_2', 100),
        'rolling_mean_3': data.get('rolling_mean_3', 1),
        'day_of_week': data.get('day_of_week', 'Tuesday')  # Default value
    }
    features['weather_weight'] = weather_conditions.get(features['weather_weight'], 400)  # Default all zeros
    features['event_weight'] = event_types.get(features['event_weight'], 534)  # Default all zeros
    print("The input feature for temperature is " + str(type(features['temp_weight'])))
    features['temp_weight'] = get_weight(features['temp_weight'], temperature_bins)
    
    # Map day_of_week to one-hot encoded features
    day_map = {
        'Friday': [5436, 0, 0, 0, 0, 0],  # Adjust for your dataset
        'Saturday': [0, 6042, 0, 0, 0, 0],
        'Sunday': [0, 0, 5690, 0, 0, 0],
        'Thursday': [0, 0, 0, 4783, 0, 0],
        'Tuesday': [0, 0, 0, 0, 3242, 0],
        'Wednesday': [0, 0, 0, 0, 0, 3299]
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

    print(feature_array)
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
    # return jsonify({'predicted_attendance': prediction})
    return str(round(prediction))
    # print(data)
    # print("POST request received")
    # return "123", 200

if __name__ == '__main__':
    app.run(debug=True)















    # try:
    #     # Get JSON data from request
    #     data = request.get_json()

    #     # Ensure all necessary fields are provided
    #     if not all(key in data for key in ('weather', 'temperature', 'event', 'day_of_week')):
    #         return jsonify({'error': 'Missing required fields'}), 400

    #     # Simulate model prediction (replace this with your actual model logic)
    #     predicted_attendance = 123  # For now, it's static

    #     # Return the prediction
    #     return jsonify(predicted_attendance=predicted_attendance)
    # except Exception as e:
    #     return jsonify({'error': str(e)}), 500

# from flask import Flask, request, jsonify
# from flask_cors import CORS
# import pickle

# app = Flask(__name__)
# CORS(app)

# with open("attendance_model.pkl", "rb") as f:
#     model = pickle.load(f)

# # Maps for categorical inputs
# weather_map = {'Sunny': 0, 'Rainy': 1, 'Cloudy': 2}
# event_map = {'Sports': 0, 'Concert': 1, 'Conference': 2}
# day_map = {'Monday': 0, 'Tuesday': 1, 'Wednesday': 2, 'Thursday': 3, 'Friday': 4, 'Saturday': 5, 'Sunday': 6}

# @app.route('/predict', methods=['POST'])
# def predict():
#     try:
#         data = request.json
#         weather = data.get('weather')
#         event = data.get('event')
#         day_of_week = data.get('day_of_week')

#         if not weather or not event or not day_of_week:
#             return jsonify({'error': 'Missing input fields'}), 400

#         # Convert inputs to numerical values
#         features = [
#             weather_map[weather],
#             event_map[event],
#             day_map[day_of_week],
#         ]

#         # Predict
#         prediction = model.predict([features])[0]
#         # return jsonify({'predicted_attendance': prediction})
#         return jsonify({'predicted_attendance': 1000})

#     except Exception as e:
#         return jsonify({'error': str(e)}), 500

# if __name__ == '__main__':
#     app.run(debug=True)
