import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Parameters for filtering
price_min = 0   # Minimum ticket price to include
price_max = 50  # Maximum ticket price to include
min_ticket_threshold = 5  # Minimum number of tickets required for a price to be included

# Load the CSV file
data = pd.read_csv(r"C:\Users\Busti\OneDrive - Worcester Polytechnic Institute (wpi.edu)\MQP\MQP Python\sales_report_updated.csv", low_memory=False)

# Filter out "Saint Patricks Day" from BUYER_TYPE_DESC and filter for 'singles' tickets only
data = data[(data['BUYER_TYPE_DESC'] != 'Saint Patricks Day') & (data['ADJ.PGS'] == 'S')]

# Filter ticket prices within the specified range
data = data[(data['TICKET_PAID_AMOUNT'] >= price_min) & (data['TICKET_PAID_AMOUNT'] <= price_max)]

# Ensure EVENT_USAGE_DATE is in datetime format
data['EVENT_USAGE_DATE'] = pd.to_datetime(data['EVENT_USAGE_DATE'])

# Explicitly cast the exclusion dates to datetime
exclude_dates = pd.to_datetime(['2024-04-02', '2024-07-04'])
data = data[~data['EVENT_USAGE_DATE'].isin(exclude_dates)]

# Group by TICKET_PAID_AMOUNT and GameDay to get ticket counts for each day
attendance_data = data.groupby(['TICKET_PAID_AMOUNT', 'GameDay'], observed=True).size().reset_index(name='total_tickets')

# Filter out TICKET_PAID_AMOUNT entries with fewer total tickets than the threshold
attendance_data = attendance_data[attendance_data['total_tickets'] >= min_ticket_threshold]

# Count the unique event dates (games) for each day of the week (Tue-Sun)
# Get the day of the week for each unique event date
data['day_of_week'] = data['EVENT_USAGE_DATE'].dt.day_name()

# Count the unique games (EVENT_USAGE_DATE) per day of the week
unique_games_per_day = data.drop_duplicates(subset=['EVENT_USAGE_DATE', 'day_of_week'])
games_per_day = unique_games_per_day['day_of_week'].value_counts().reindex(['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday'], fill_value=0)

# Convert 'TICKET_PAID_AMOUNT' to a non-categorical type for reindexing
attendance_data['TICKET_PAID_AMOUNT'] = attendance_data['TICKET_PAID_AMOUNT'].astype(float)

# Normalize the 'GameDay' to match the full day names for consistency
attendance_data['GameDay'] = attendance_data['GameDay'].map({
    'Tue': 'Tuesday', 
    'Wed': 'Wednesday', 
    'Thu': 'Thursday', 
    'Fri': 'Friday', 
    'Sat': 'Saturday', 
    'Sun': 'Sunday'
})

# Define days of the week to ensure we have a consistent order and create x positions
days_of_week = ['Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday', 'Saturday', 'Sunday']
unique_ticket_prices = sorted(attendance_data['TICKET_PAID_AMOUNT'].unique())
num_prices = len(unique_ticket_prices)
bar_width = 0.15  # Width of each bar
x_positions = np.arange(num_prices)


# Plot for each day
fig, ax = plt.subplots(figsize=(14, 8))

for i, day in enumerate(days_of_week):
    # Filter data for the specific day and reindex
    subset = attendance_data[attendance_data['GameDay'] == day].set_index('TICKET_PAID_AMOUNT').reindex(unique_ticket_prices, fill_value=0).reset_index()
    
    # Calculate the average tickets purchased by dividing by the number of games that occurred on that day
    avg_tickets = subset['total_tickets'] / games_per_day[day]
    
    # Only plot if avg_tickets is greater than zero
    if avg_tickets.sum() > 0:
        ax.bar(x_positions + i * bar_width, avg_tickets, width=bar_width, label=day)

# Labeling and customizations
ax.set_xlabel('Ticket Paid Amount')
ax.set_ylabel('Average Tickets Purchased')
ax.set_title('Average Tickets Purchased by Ticket Paid Amount and Day of Week (Singles Only)')
ax.set_xticks(x_positions + (len(days_of_week) - 1) * bar_width / 2)
ax.set_xticklabels(unique_ticket_prices, rotation=45)
ax.legend(title="Day of the Week")

# Show the plot
plt.tight_layout()
plt.show()
