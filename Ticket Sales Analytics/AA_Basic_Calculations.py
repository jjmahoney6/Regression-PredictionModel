import pandas as pd

# Load the CSV file
data = pd.read_csv(r"C:\Users\Busti\OneDrive - Worcester Polytechnic Institute (wpi.edu)\MQP\MQP Python\2023 Ticket Sales Data - Cleaned.csv", low_memory=False)

# 2024 data --- "C:\Users\Busti\OneDrive - Worcester Polytechnic Institute (wpi.edu)\MQP\MQP Python\sales_report_updated.csv"
# 2023 data --- "C:\Users\Busti\OneDrive - Worcester Polytechnic Institute (wpi.edu)\MQP\MQP Python\2023 Ticket Sales Data - Cleaned.csv"

# Filter for single-game tickets only
data = data[data['ADJ.PGS'] == 'S']

# Convert dates to datetime format
data['EVENT_USAGE_DATE'] = pd.to_datetime(data['EVENT_USAGE_DATE'])
data['TRANSACTION_DATE'] = pd.to_datetime(data['TRANSACTION_DATE'])

# Calculate the number of days between TRANSACTION_DATE and EVENT_USAGE_DATE
data['DAYS_BEFORE_EVENT'] = (data['EVENT_USAGE_DATE'] - data['TRANSACTION_DATE']).dt.days

# Define the filter range for days
min_days = 0  # Minimum days before the event (inclusive)
max_days = 0  # Maximum days before the event (inclusive)

# Apply the filter for tickets bought within the specified date range
filtered_tickets = data[(data['DAYS_BEFORE_EVENT'] >= min_days) & (data['DAYS_BEFORE_EVENT'] <= max_days)]

# Calculate the total number of tickets in the filtered range
total_tickets = len(filtered_tickets)

# Calculate the number of attended tickets (those marked as 'SCANNED')
attended_tickets = filtered_tickets['SCANNED'].sum()

# Calculate the attendance rate as a percentage
attendance_rate = (attended_tickets / total_tickets) * 100 if total_tickets > 0 else 0

# Calculate the percentage of tickets bought within the specified range
percentage_filtered = (total_tickets / len(data)) * 100

# Print the results
print(f"Percentage of single-game tickets bought between {min_days} and {max_days} days before EVENT_USAGE_DATE: {percentage_filtered:.2f}%")
print(f"Attendance rate for tickets bought between {min_days} and {max_days} days before EVENT_USAGE_DATE: {attendance_rate:.2f}%")
