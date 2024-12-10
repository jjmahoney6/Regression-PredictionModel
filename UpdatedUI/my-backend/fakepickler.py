import numpy as np
from sklearn.linear_model import LinearRegression
import pickle

# Generate sample data
np.random.seed(42)
X = np.random.rand(1000, 12)
y = np.sum(X, axis=1)

# Train the model
model = LinearRegression()
model.fit(X, y)

# Save the model to a file using pickle
with open('sum_model.pkl', 'wb') as file:
    pickle.dump(model, file)

print("Model saved successfully!")

# Load the model from the pickle file
with open('sum_model.pkl', 'rb') as file:
    loaded_model = pickle.load(file)

# Test the loaded model
example_input = np.random.rand(1, 12)
predicted_sum = loaded_model.predict(example_input)
actual_sum = np.sum(example_input)

print(f"Input: {example_input}")
print(f"Actual Sum: {actual_sum}")
print(f"Predicted Sum: {predicted_sum[0]}")
