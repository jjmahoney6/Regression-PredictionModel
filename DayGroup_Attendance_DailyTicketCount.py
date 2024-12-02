import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data
data = pd.read_csv(r"C:\Users\Busti\OneDrive - Worcester Polytechnic Institute (wpi.edu)\MQP\MQP Python\sales_report_updated.csv", low_memory=False)

# Filter out specific event dates
data = data[~data['EVENT_USAGE_DATE'].isin(['2024-04-02', '2024-07-04'])]

# Define day-of-week groups
day_of_week_mapping = {
    'Fri': 'Fri-Sat', 'Sat': 'Fri-Sat',
    'Sun': 'Sun',
    'Tue': 'Tue-Thu', 'Wed': 'Tue-Thu', 'Thu': 'Tue-Thu'
}
data['Day_Group'] = data['GameDay'].map(day_of_week_mapping)

# Group by both Day_Group and ADJ.PGS (ticket type) to calculate attendance rate
attendance_data = data.groupby(['Day_Group', 'ADJ.PGS']).agg(
    total_tickets=('SCANNED', 'count'),
    attended=('SCANNED', 'sum')
)
attendance_data['ATTENDANCE_RATE'] = (attendance_data['attended'] / attendance_data['total_tickets']) * 100
attendance_data = attendance_data.reset_index()

# Prepare total and average tickets by day of the week
data['EVENT_USAGE_DATE'] = pd.to_datetime(data['EVENT_USAGE_DATE'])
days_of_week = ['Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
total_tickets_by_day = data.groupby('GameDay').size().reindex(days_of_week, fill_value=0)
game_counts_by_day = data.groupby('GameDay')['EVENT_USAGE_DATE'].nunique().reindex(days_of_week, fill_value=1)
avg_tickets_by_day = (total_tickets_by_day / game_counts_by_day).round().astype(int)

# Plot setup
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# Plot 1: Attendance rate by Day_Group and Ticket Type
bar_width = 0.2
x_labels = attendance_data['Day_Group'].unique()
x_pos = np.arange(len(x_labels))
left_colors = ['#ab162b', 'black', 'gray']

for i, (ticket_type, color) in enumerate(zip(['S', 'P', 'G'], left_colors)):
    subset = attendance_data[attendance_data['ADJ.PGS'] == ticket_type]
    x_offset = x_pos + i * bar_width
    ax1.bar(x_offset, subset['ATTENDANCE_RATE'], width=bar_width, label=f'{ticket_type}', color=color, alpha=0.7)

ax1.set_xlabel('Day Group')
ax1.set_ylabel('Attendance Rate (%)')
ax1.set_title('Attendance Rate by Day Group and Ticket Type')
ax1.set_xticks(x_pos + bar_width)
ax1.set_xticklabels(x_labels)
ax1.legend(title='Ticket Type')

# Plot 2: Total and Average Tickets Purchased by Day of the Week
x_positions = np.arange(len(days_of_week))
ax2.bar(x_positions - 0.2, total_tickets_by_day, width=0.4, label='Total Tickets', color='#ab162b')
ax2.bar(x_positions + 0.2, avg_tickets_by_day, width=0.4, label='Average Tickets', color='black')

ax2.set_xlabel('Day of the Week')
ax2.set_ylabel('Tickets Purchased', fontsize=8)
ax2.yaxis.set_label_coords(0, 0.53)
ax2.set_title('Total and Average Tickets Purchased by Day of the Week')
ax2.set_xticks(x_positions)
ax2.set_xticklabels(days_of_week)
ax2.legend()

plt.tight_layout()
plt.show()
