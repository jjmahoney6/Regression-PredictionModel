import pandas as pd
import matplotlib.pyplot as plt

# Define the custom plot style settings
plot_style = {
    'font.family': 'Arial',
    'font.size': 12,
    'axes.titlesize': 14,
    'axes.labelsize': 12,
    'xtick.labelsize': 10,
    'ytick.labelsize': 10,
    'axes.titleweight': 'bold',
    'axes.labelweight': 'bold',
    'text.color': '#000000',
    'axes.edgecolor': '#000000',
    'axes.facecolor': '#FFFFFF',
    'xtick.color': '#000000',
    'ytick.color': '#000000',
    'grid.color': '#000000',
    'lines.linewidth': 2,
    'legend.frameon': False,
    'legend.loc': 'upper right'
}

# Apply the style
plt.rcParams.update(plot_style)

# Load the CSV file
data = pd.read_csv(r"C:\Users\Busti\OneDrive - Worcester Polytechnic Institute (wpi.edu)\MQP\MQP Python\sales_report_updated.csv", low_memory=False)
data = data[data['ADJ.PGS'] == 'S']  # Filter for 'singles' only

# Parameters to specify the price range and ticket threshold
price_min = 0    # Minimum ticket price to include
price_max = 50   # Maximum ticket price to include
min_ticket_threshold = 100  # Minimum number of tickets required for a price to be included

# Filter by the specified TICKET_PAID_AMOUNT range
data = data[(data['TICKET_PAID_AMOUNT'] >= price_min) & (data['TICKET_PAID_AMOUNT'] <= price_max)]

# Calculate total tickets and attended tickets for each TICKET_PAID_AMOUNT
attendance_data = data.groupby('TICKET_PAID_AMOUNT').agg(
    total_tickets=('SCANNED', 'count'),
    attended=('SCANNED', 'sum')
)

# Filter out TICKET_PAID_AMOUNT entries with fewer total tickets than the threshold
attendance_data = attendance_data[attendance_data['total_tickets'] >= min_ticket_threshold]

# Calculate the attendance rate as a percentage
attendance_data['ATTENDANCE_RATE'] = (attendance_data['attended'] / attendance_data['total_tickets']) * 100

# Create the combined stacked bar and line graph
fig, ax1 = plt.subplots(figsize=(12, 8))

# Define colors
total_color = '#f2b1b5'  # Light red for total tickets
attended_color = '#ab162b'  # Dark red for attended tickets
line_color = '#000000'  # Black for the attendance rate line

# Plot total tickets as a stacked bar with attended tickets on top
ax1.bar(attendance_data.index, attendance_data['total_tickets'], color=total_color, label='Total Tickets')
ax1.bar(attendance_data.index, attendance_data['attended'], color=attended_color, label='Attended Tickets')

# Set labels for the primary y-axis
ax1.set_xlabel('Ticket Paid Amount')
ax1.set_ylabel('Number of Tickets')
ax1.set_title('Total Tickets, Attended Tickets, and Attendance Rate by Ticket Paid Amount')
ax1.set_xticks(range(len(attendance_data)))
ax1.set_xticklabels(attendance_data.index, rotation=45)
ax1.legend(loc='upper left')

# Add total and attended ticket count labels above each bar
for i, (total, attended) in enumerate(zip(attendance_data['total_tickets'], attendance_data['attended'])):
    ax1.text(i, total + 1, f'{total}', ha='center', va='bottom', fontsize=8)
    ax1.text(i, attended + 1, f'{attended}', ha='center', va='bottom', fontsize=8, color=attended_color)

# Create a second y-axis to plot the attendance rate as a line graph with black color
ax2 = ax1.twinx()
ax2.plot(attendance_data.index, attendance_data['ATTENDANCE_RATE'], color=line_color, marker='o', label='Attendance Rate')
ax2.set_ylabel('Attendance Rate (%)')
ax2.tick_params(axis='y', labelcolor=line_color)

# Add attendance rate labels on top of each data point
for i, rate in enumerate(attendance_data['ATTENDANCE_RATE']):
    ax2.text(i, rate + 1, f'{rate:.1f}%', ha='center', va='bottom', fontsize=8, color=line_color)

# Display the plot with tight layout
fig.tight_layout()
plt.show()
