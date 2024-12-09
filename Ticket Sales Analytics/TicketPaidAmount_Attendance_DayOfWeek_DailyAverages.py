import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the CSV file
data = pd.read_csv(r"C:\Users\Busti\OneDrive - Worcester Polytechnic Institute (wpi.edu)\MQP\MQP Python\sales_report_updated.csv", low_memory=False)

# Filter out "Saint Patricks Day" from BUYER_TYPE_DESC
data = data[data['BUYER_TYPE_DESC'] != 'Saint Patricks Day']

# Ensure EVENT_USAGE_DATE is in datetime format
data['EVENT_USAGE_DATE'] = pd.to_datetime(data['EVENT_USAGE_DATE'])

# Explicitly cast the exclusion dates to datetime
exclude_dates = pd.to_datetime(['2024-04-02', '2024-07-04'])
data = data[~data['EVENT_USAGE_DATE'].isin(exclude_dates)]

# Total tickets by day of the week
total_tickets_by_day = data.groupby('GameDay').size().reindex(['Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], fill_value=0)

# Average tickets purchased per day (by dividing total by the number of games for each day)
game_counts_by_day = data.groupby('GameDay')['EVENT_USAGE_DATE'].nunique().reindex(['Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun'], fill_value=1)
avg_tickets_by_day = total_tickets_by_day / game_counts_by_day

# Set up x positions for the days of the week
days_of_week = ['Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
x_positions = np.arange(len(days_of_week))

# Plot the data
fig, ax = plt.subplots(figsize=(10, 6))

# Plot total tickets purchased per day
ax.bar(x_positions - 0.2, total_tickets_by_day, width=0.4, label='Total Tickets', color='lightblue')

# Plot average tickets purchased per day
ax.bar(x_positions + 0.2, avg_tickets_by_day, width=0.4, label='Average Tickets', color='lightgreen')

# Customize the labels and layout
ax.set_xlabel('Day of the Week')
ax.set_ylabel('Tickets Purchased')
ax.set_title('Total and Average Tickets Purchased by Day of the Week')
ax.set_xticks(x_positions)
ax.set_xticklabels(days_of_week)
ax.legend()

plt.tight_layout()
plt.show()
