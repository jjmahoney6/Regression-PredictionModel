import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Define the specific ticket price to filter
specific_ticket_price = 27  # Change this to your desired ticket price

# Load the CSV file
data = pd.read_csv(r"C:\Users\Busti\OneDrive - Worcester Polytechnic Institute (wpi.edu)\MQP\MQP Python\sales_report_updated.csv", low_memory=False)

# Filter for "singles" tickets only and for the specific ticket price
data = data[(data['ADJ.PGS'] == 'S') & (data['TICKET_PAID_AMOUNT'] == specific_ticket_price)]

# Ensure EVENT_USAGE_DATE is in datetime format and exclude specific dates
data['EVENT_USAGE_DATE'] = pd.to_datetime(data['EVENT_USAGE_DATE'])
exclude_dates = pd.to_datetime(['2024-04-02', '2024-07-04'])
data = data[~data['EVENT_USAGE_DATE'].isin(exclude_dates)]

# Map 'GameDay' to day names for consistency
day_mapping = {'Tue': 'Tuesday', 'Wed': 'Wednesday', 'Thu': 'Thursday', 'Fri': 'Friday', 'Sat': 'Saturday', 'Sun': 'Sunday'}
data['GameDay'] = data['GameDay'].map(day_mapping)

# Group by both SECTION_DESC and GameDay to calculate attendance percentage
attendance_data = data.groupby(['SECTION_DESC', 'GameDay']).agg(
    total_tickets=('SCANNED', 'count'),
    attended=('SCANNED', 'sum')
).reset_index()
attendance_data['ATTENDANCE_RATE'] = (attendance_data['attended'] / attendance_data['total_tickets']) * 100

# Prepare data for plotting the attendance percentage by day of week and section
days_of_week = ['Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
sections = attendance_data['SECTION_DESC'].unique()
bar_width = 0.05  # Thinner bars to reduce overlap
x_positions = np.arange(len(days_of_week))

# Plot attendance percentage by day of week and section
fig, ax = plt.subplots(figsize=(14, 8))

for i, section in enumerate(sections):
    subset = attendance_data[attendance_data['SECTION_DESC'] == section].set_index('GameDay').reindex(days_of_week, fill_value=0).reset_index()
    ax.bar(x_positions + i * bar_width, subset['ATTENDANCE_RATE'], width=bar_width, label=section)

# Customize plot for attendance rate
ax.set_xlabel('Day of the Week')
ax.set_ylabel('Attendance Rate (%)')
ax.set_title(f'Attendance Rate by Day of Week and Ballpark Section for Tickets Priced at ${specific_ticket_price}')
ax.set_xticks(x_positions + (len(sections) - 1) * bar_width / 2)
ax.set_xticklabels(days_of_week, rotation=45)
ax.legend(title='Ballpark Section', bbox_to_anchor=(1.05, 1), loc='upper left')

plt.tight_layout()
plt.show()

# ----------------- Follow-Up Graph: Total Tickets Purchased per Section -----------------

# Group by SECTION_DESC to calculate total tickets purchased for each section
total_tickets_data = data.groupby('SECTION_DESC').agg(total_tickets=('SCANNED', 'count')).reset_index()

# Plot the total number of tickets purchased per section
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(total_tickets_data['SECTION_DESC'], total_tickets_data['total_tickets'], color='skyblue')
ax.set_xlabel('Ballpark Section')
ax.set_ylabel('Total Tickets Purchased')
ax.set_title(f'Total Tickets Purchased by Ballpark Section for Tickets Priced at ${specific_ticket_price}')
ax.set_xticklabels(total_tickets_data['SECTION_DESC'], rotation=45, ha='right')

plt.tight_layout()
plt.show()
