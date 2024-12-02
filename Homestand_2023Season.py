import pandas as pd
from datetime import datetime, timedelta

# Load the CSV file
file_path = r"C:\Users\Busti\OneDrive - Worcester Polytechnic Institute (wpi.edu)\MQP\MQP Python\Sales+AttenadanceCounts23.csv"
df = pd.read_csv(file_path)

# Convert EVENT_USAGE_DATE to datetime format if it's not already
df['EVENT_USAGE_DATE'] = pd.to_datetime(df['EVENT_USAGE_DATE'])

# Sort by EVENT_USAGE_DATE to ensure we process the games in chronological order
df = df.sort_values('EVENT_USAGE_DATE')

# Initialize variables to track homestand number and start of each homestand
homestand_num = 1
homestand_start = None

# Create a new column 'homestand'
df['homestand'] = 0

# Iterate over the rows to assign homestand numbers
for index, row in df.iterrows():
    event_date = row['EVENT_USAGE_DATE']
    
    # If it's the first date or the current game is after the current homestand has ended
    if homestand_start is None or event_date > homestand_start + timedelta(days=6):
        # Find the start of the next homestand (the next Tuesday)
        # The homestand starts on Tuesday, so calculate the next Tuesday after the current event date
        days_ahead = (1 - event_date.weekday()) % 7  # days_ahead gives the number of days to the next Tuesday
        homestand_start = event_date + timedelta(days=days_ahead)
    
    # Assign the homestand number
    df.at[index, 'homestand'] = homestand_num
    
    # If the event is on a Sunday, increment the homestand number
    if event_date.weekday() == 6:  # Sunday
        homestand_num += 1

# Save the updated DataFrame back to a new CSV file
output_file = r"C:\Users\Busti\OneDrive - Worcester Polytechnic Institute (wpi.edu)\MQP\MQP Python\Sales+AttenadanceCounts23_with_homestand.csv"
df.to_csv(output_file, index=False)

print("Homestand column added successfully!")
