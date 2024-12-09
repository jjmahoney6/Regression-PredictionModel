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

# Create a new column 'Day_Group' based on 'GameDay' to categorize days
data['Day_Group'] = data['GameDay'].apply(lambda x: 
    'Fri-Sat' if x in ['Fri', 'Sat'] else 
    'Sun' if x == 'Sun' else 
    'Tue-Wed-Thu' if x in ['Tue', 'Wed', 'Thu'] else 
    'Other'
)

# Group by TICKET_PAID_AMOUNT and Day_Group, then aggregate attendance data
attendance_data = data.groupby(['TICKET_PAID_AMOUNT', 'Day_Group']).agg(
    total_tickets=('SCANNED', 'count'),
    attended=('SCANNED', 'sum')
).reset_index()

# Filter out TICKET_PAID_AMOUNT entries with fewer total tickets than the threshold
attendance_data = attendance_data[attendance_data['total_tickets'] >= min_ticket_threshold]

# Calculate the attendance rate
attendance_data['ATTENDANCE_RATE'] = (attendance_data['attended'] / attendance_data['total_tickets']) * 100

# Get the unique TICKET_PAID_AMOUNT values and set up x positions
unique_ticket_prices = sorted(attendance_data['TICKET_PAID_AMOUNT'].unique())
num_groups = len(unique_ticket_prices)
bar_width = 0.25  # Width of each bar

# Define x positions for side-by-side bars
x_base = np.arange(num_groups)
x_pos_fri_sat = x_base - bar_width
x_pos_sun = x_base
x_pos_tue_thu = x_base + bar_width

# Reindex each group to include all unique ticket prices, filling missing values with 0
fri_sat_data = attendance_data[attendance_data['Day_Group'] == 'Fri-Sat'].set_index('TICKET_PAID_AMOUNT').reindex(unique_ticket_prices, fill_value=0).reset_index()
sun_data = attendance_data[attendance_data['Day_Group'] == 'Sun'].set_index('TICKET_PAID_AMOUNT').reindex(unique_ticket_prices, fill_value=0).reset_index()
tue_thu_data = attendance_data[attendance_data['Day_Group'] == 'Tue-Wed-Thu'].set_index('TICKET_PAID_AMOUNT').reindex(unique_ticket_prices, fill_value=0).reset_index()

# Plot 1: Attendance Rate by TICKET_PAID_AMOUNT and Day_Group
fig, ax = plt.subplots(figsize=(14, 8))

ax.bar(x_pos_fri_sat, fri_sat_data['ATTENDANCE_RATE'], width=bar_width, label='Fri-Sat', color='skyblue')
ax.bar(x_pos_sun, sun_data['ATTENDANCE_RATE'], width=bar_width, label='Sun', color='lightgreen')
ax.bar(x_pos_tue_thu, tue_thu_data['ATTENDANCE_RATE'], width=bar_width, label='Tue-Wed-Thu', color='salmon')

# Labeling and customizations
ax.set_xlabel('Ticket Paid Amount')
ax.set_ylabel('Attendance Rate (%)')
ax.set_title('Attendance Rate by Ticket Paid Amount and Day Group (Singles Only)')
ax.set_xticks(x_base)
ax.set_xticklabels(unique_ticket_prices, rotation=45)
ax.legend(title="Game Day")

# Attendance rate labels above each bar
for i, row in fri_sat_data.iterrows():
    if row['ATTENDANCE_RATE'] > 0:
        ax.text(x_pos_fri_sat[i], row['ATTENDANCE_RATE'] + 1, f"{row['ATTENDANCE_RATE']:.1f}%", 
                ha='center', va='bottom', fontsize=8)
for i, row in sun_data.iterrows():
    if row['ATTENDANCE_RATE'] > 0:
        ax.text(x_pos_sun[i], row['ATTENDANCE_RATE'] + 1, f"{row['ATTENDANCE_RATE']:.1f}%", 
                ha='center', va='bottom', fontsize=8)
for i, row in tue_thu_data.iterrows():
    if row['ATTENDANCE_RATE'] > 0:
        ax.text(x_pos_tue_thu[i], row['ATTENDANCE_RATE'] + 1, f"{row['ATTENDANCE_RATE']:.1f}%", 
                ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()

# Plot 2: Total Tickets Purchased by TICKET_PAID_AMOUNT and Day_Group
fig, ax = plt.subplots(figsize=(14, 8))

ax.bar(x_pos_fri_sat, fri_sat_data['total_tickets'], width=bar_width, label='Fri-Sat', color='skyblue')
ax.bar(x_pos_sun, sun_data['total_tickets'], width=bar_width, label='Sun', color='lightgreen')
ax.bar(x_pos_tue_thu, tue_thu_data['total_tickets'], width=bar_width, label='Tue-Wed-Thu', color='salmon')

# Labeling and customizations
ax.set_xlabel('Ticket Paid Amount')
ax.set_ylabel('Total Tickets Purchased')
ax.set_title('Total Tickets Purchased by Ticket Paid Amount and Day Group (Singles Only)')
ax.set_xticks(x_base)
ax.set_xticklabels(unique_ticket_prices, rotation=45)
ax.legend(title="Game Day")

# Total ticket labels above each bar
for i, row in fri_sat_data.iterrows():
    if row['total_tickets'] > 0:
        ax.text(x_pos_fri_sat[i], row['total_tickets'] + 1, f"{int(row['total_tickets'])}", 
                ha='center', va='bottom', fontsize=8)
for i, row in sun_data.iterrows():
    if row['total_tickets'] > 0:
        ax.text(x_pos_sun[i], row['total_tickets'] + 1, f"{int(row['total_tickets'])}", 
                ha='center', va='bottom', fontsize=8)
for i, row in tue_thu_data.iterrows():
    if row['total_tickets'] > 0:
        ax.text(x_pos_tue_thu[i], row['total_tickets'] + 1, f"{int(row['total_tickets'])}", 
                ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()
