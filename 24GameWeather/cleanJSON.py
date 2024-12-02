import requests
import json

#clean JSON file to only look at day weather data not hourly
with open('api_responses.json', 'r') as f:
    data = json.load(f)

for i in range(len(data)):
    days = data[i]
    for day in days['forecast']['forecastday']:
        if 'hour' in day:
            del day['hour']
        if 'astro' in day: 
            del day['astro']

# Save the cleaned data back to a new JSON file
with open('cleaned_file.json', 'w') as f:
    json.dump(data, f, indent=4)