import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
data = pd.read_csv(r"C:\Users\Busti\OneDrive\Documents\PythonWork\MQP Python\sales_report_updated.csv", low_memory=False)
data = data[data['ADJ.PGS'] == 'S']  # Filter for 'singles' only

# Exclude "Saint Patricks Day" from BUYER_TYPE_DESCRIPTION
data = data[data['BUYER_TYPE_DESC'] != "St. Paddy's Day Parade Special"]

# Convert the dates to datetime format
data['EVENT_USAGE_DATE'] = pd.to_datetime(data['EVENT_USAGE_DATE'])
data['TRANSACTION_DATE'] = pd.to_datetime(data['TRANSACTION_DATE'])

# Calculate the number of days between transaction and event
data['DAYS_BEFORE_EVENT'] = (data['EVENT_USAGE_DATE'] - data['TRANSACTION_DATE']).dt.days

# Filter to include only non-negative days before the event
data = data[data['DAYS_BEFORE_EVENT'] >= 0]

# Group by DAYS_BEFORE_EVENT to calculate attendance rate
attendance_data = data.groupby('DAYS_BEFORE_EVENT').agg(
    total_tickets=('SCANNED', 'count'),
    attended=('SCANNED', 'sum')
)

# Calculate the attendance rate
attendance_data['ATTENDANCE_RATE'] = (attendance_data['attended'] / attendance_data['total_tickets']) * 100

# Set customizable range for days before the event
min_days = 0  # Set the minimum number of days
max_days = 20  # Set the maximum number of days

# Filter days based on the customizable range and reset index for numeric indexing
attendance_data = attendance_data[(attendance_data.index >= min_days) & (attendance_data.index <= max_days)].reset_index()

# Create the first bar graph for Attendance Rate
plt.figure(figsize=(10, 6))
plt.bar(attendance_data['DAYS_BEFORE_EVENT'], attendance_data['ATTENDANCE_RATE'], color='skyblue')
plt.xlabel('Days Between Transaction Date and Event Date')
plt.ylabel('Attendance Rate (%)')
plt.title(f'Attendance Rate vs. Days Before Event (Singles Only, Days {min_days}-{max_days})')
plt.xticks(rotation=45)

# Add attendance rate labels on top of each bar
for i in range(len(attendance_data)):
    plt.text(attendance_data['DAYS_BEFORE_EVENT'][i], attendance_data['ATTENDANCE_RATE'][i] + 1,
             f'{attendance_data["ATTENDANCE_RATE"][i]:.1f}%', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()

# Create the second bar graph for Total Tickets
plt.figure(figsize=(10, 6))
plt.bar(attendance_data['DAYS_BEFORE_EVENT'], attendance_data['total_tickets'], color='skyblue')
plt.xlabel('Days Between Transaction Date and Event Date')
plt.ylabel('Total Tickets')
plt.title(f'Total Tickets vs. Days Before Event (Singles Only, Days {min_days}-{max_days})')
plt.xticks(rotation=45)

# Add total tickets labels on top of each bar
for i in range(len(attendance_data)):
    plt.text(attendance_data['DAYS_BEFORE_EVENT'][i], attendance_data['total_tickets'][i] + 1,
             f'{attendance_data["total_tickets"][i]}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()
