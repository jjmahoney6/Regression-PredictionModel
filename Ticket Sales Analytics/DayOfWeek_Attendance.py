import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Load the data
data = pd.read_csv(r"C:\Users\Busti\OneDrive - Worcester Polytechnic Institute (wpi.edu)\MQP\MQP Python\sales_report_updated.csv", low_memory=False)

# Filter out specific event dates
data = data[~data['EVENT_USAGE_DATE'].isin(['2024-04-02', '2024-07-04'])]

# Filter out "Saint Patricks Day" from BUYER_TYPE_DESC
data = data[(data['BUYER_TYPE_DESC'] != 'Saint Patricks Day')]

# Define day-of-week groups
day_of_week_mapping = {
    'Fri': 'Fri-Sat', 'Sat': 'Fri-Sat',
    'Sun': 'Sun',
    'Tue': 'Tue-Thu', 'Wed': 'Tue-Thu', 'Thu': 'Tue-Thu'
}
data['Day_Group'] = data['GameDay'].map(day_of_week_mapping)

# Group by both Day_Group and ADJ.PGS (ticket type)
attendance_data = data.groupby(['Day_Group', 'ADJ.PGS']).agg(
    total_tickets=('SCANNED', 'count'),
    attended=('SCANNED', 'sum')
)
attendance_data['ATTENDANCE_RATE'] = (attendance_data['attended'] / attendance_data['total_tickets']) * 100
attendance_data = attendance_data.reset_index()

# Set up plot for each Day_Group and Ticket Type
fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(16, 8))

# Define bar width and offset positions for side-by-side bars
bar_width = 0.2
x_labels = attendance_data['Day_Group'].unique()
x_pos = np.arange(len(x_labels))
left_colors = ['#ab162b', 'black', 'gray']
right_colors = ['#ab162b', 'black', 'gray']

# Plot 1: Attendance rate by Day_Group and Ticket Type
for i, (ticket_type, color) in enumerate(zip(['S', 'P', 'G'], left_colors)):
    subset = attendance_data[attendance_data['ADJ.PGS'] == ticket_type]
    x_offset = x_pos + i * bar_width
    ax1.bar(x_offset, subset['ATTENDANCE_RATE'], width=bar_width, label=f'{ticket_type}', color=color, alpha=0.7)

ax1.set_xlabel('Day Group')
ax1.set_ylabel('Attendance Rate (%)')
ax1.set_title('Attendance Rate by Day Group and Ticket Type (2024)')
ax1.set_xticks(x_pos + bar_width)
ax1.set_xticklabels(x_labels)
ax1.legend(title='Ticket Type')

# Plot 2: Total tickets vs. attended tickets by Day_Group and Ticket Type
for i, (ticket_type, color) in enumerate(zip(['S', 'P', 'G'], right_colors)):
    subset = attendance_data[attendance_data['ADJ.PGS'] == ticket_type]
    x_offset = x_pos + i * bar_width
    ax2.bar(x_offset, subset['total_tickets'], width=bar_width, label=f'{ticket_type} - Total', color=color, alpha=0.5)
    ax2.bar(x_offset, subset['attended'], width=bar_width, label=f'{ticket_type} - Attended', color=color, alpha=0.9)

ax2.set_xlabel('Day Group')
ax2.set_ylabel('Number of Tickets')
ax2.set_title('Total vs. Attended Tickets by Day Group and Ticket Type (2024)')
ax2.set_xticks(x_pos + bar_width)
ax2.set_xticklabels(x_labels)
ax2.legend(title='Ticket Type')

plt.tight_layout()
plt.show()
