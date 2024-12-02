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
data = pd.read_csv(r"C:\Users\Busti\OneDrive - Worcester Polytechnic Institute (wpi.edu)\MQP\MQP Python\2023 Ticket Sales Data - Cleaned.csv", low_memory=False)
data = data[data['ADJ.PGS'] == 'S']  # Filter for 'singles' only

# Parameters to specify the price range
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

# Create the figure
fig, ax1 = plt.subplots(figsize=(12, 8))

# Define bar width and positions for bars
bar_width = 0.8
positions = range(len(attendance_data))

# Plot total tickets as bars on the primary y-axis with updated color
ax1.bar(positions, attendance_data['total_tickets'], width=bar_width, color='#ab162b', label='Total Tickets')

# Labels and title for the primary y-axis
ax1.set_xlabel('Ticket Paid Amount')
ax1.set_ylabel('Number of Tickets')
ax1.set_title('Total Tickets Purchased By Price vs. Attendance Rate (2023)')

# Create the secondary y-axis for the attendance rate
ax2 = ax1.twinx()  # Create a second y-axis sharing the same x-axis
ax2.plot(positions, attendance_data['ATTENDANCE_RATE'], color='black', marker='o', label='Attendance Rate (%)', linestyle='-', linewidth=2)
ax2.set_ylabel('Attendance Rate (%)')  # Label for the secondary y-axis

# Set the y-axis limits for attendance rate to range from 0 to 100
ax2.set_ylim(0, 100)

# Combine legends from both axes
lines, labels = ax1.get_legend_handles_labels()
lines2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(lines + lines2, labels + labels2, loc='upper right', bbox_to_anchor=(1, 0.8))

# Adjust layout to prevent overlap
plt.xticks(positions, attendance_data.index, rotation=45)
plt.tight_layout()

# Show the plot
plt.show()
