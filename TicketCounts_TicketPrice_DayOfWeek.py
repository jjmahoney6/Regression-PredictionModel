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

# Use the GameDay column to group data by each specific day
day_order = ['Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
data['GameDay'] = pd.Categorical(data['GameDay'], categories=day_order, ordered=True)

# Group by TICKET_PAID_AMOUNT and GameDay, then calculate total tickets
attendance_data = data.groupby(['TICKET_PAID_AMOUNT', 'GameDay']).size().reset_index(name='total_tickets')

# Filter out TICKET_PAID_AMOUNT entries with fewer total tickets than the threshold
attendance_data = attendance_data[attendance_data['total_tickets'] >= min_ticket_threshold]

# Get unique ticket prices and days for setting bar positions
unique_ticket_prices = sorted(attendance_data['TICKET_PAID_AMOUNT'].unique())
bar_width = 0.1  # Width of each bar

# Define x positions for side-by-side bars for each day
positions = {day: i for i, day in enumerate(day_order)}
x_base = np.arange(len(unique_ticket_prices))

# Plot: Total Tickets Purchased by TICKET_PAID_AMOUNT and GameDay
fig, ax = plt.subplots(figsize=(14, 8))

for i, day in enumerate(day_order):
    subset = attendance_data[attendance_data['GameDay'] == day]
    x_positions = x_base + i * bar_width
    ax.bar(x_positions, subset.set_index('TICKET_PAID_AMOUNT').reindex(unique_ticket_prices, fill_value=0)['total_tickets'], 
           width=bar_width, label=day)

# Labeling and customizations
ax.set_xlabel('Ticket Paid Amount')
ax.set_ylabel('Total Tickets Purchased')
ax.set_title('Total Tickets Purchased by Ticket Paid Amount and Day of Week (Singles Only)')
ax.set_xticks(x_base + (len(day_order) - 1) * bar_width / 2)
ax.set_xticklabels(unique_ticket_prices, rotation=45)
ax.legend(title="Day of Week")

# Display total ticket counts above each bar
for i, row in attendance_data.iterrows():
    day_index = day_order.index(row['GameDay'])
    x_position = x_base[unique_ticket_prices.index(row['TICKET_PAID_AMOUNT'])] + day_index * bar_width
    ax.text(x_position, row['total_tickets'] + 1, f"{int(row['total_tickets'])}", ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()
