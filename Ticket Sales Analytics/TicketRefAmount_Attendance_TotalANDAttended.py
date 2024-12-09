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

# 2024 data --- "C:\Users\Busti\OneDrive - Worcester Polytechnic Institute (wpi.edu)\MQP\MQP Python\sales_report_updated.csv"

# 2023 data --- "C:\Users\Busti\OneDrive - Worcester Polytechnic Institute (wpi.edu)\MQP\MQP Python\2023 Ticket Sales Data - Cleaned.csv"

data = data[data['ADJ.PGS'] == 'S']  # Filter for 'singles' only

# Parameters to specify the price range
price_min = 0    # Minimum ticket price to include
price_max = 50   # Maximum ticket price to include
min_ticket_threshold = 0  # Minimum number of tickets required for a price to be included

# Filter by the specified TICKET_REF_PRICE range
data = data[(data['TICKET_REF_PRICE'] >= price_min) & (data['TICKET_REF_PRICE'] <= price_max)]

# Calculate total tickets and attended tickets for each TICKET_REF_PRICE
attendance_data = data.groupby('TICKET_REF_PRICE').agg(
    total_tickets=('SCANNED', 'count'),
    attended=('SCANNED', 'sum')
)

# Filter out TICKET_REF_PRICE entries with fewer total tickets than the threshold
attendance_data = attendance_data[attendance_data['total_tickets'] >= min_ticket_threshold]

# Calculate the attendance rate as a percentage
attendance_data['ATTENDANCE_RATE'] = (attendance_data['attended'] / attendance_data['total_tickets']) * 100

# Create the combined stacked bar graph and attendance rate line graph
fig, ax1 = plt.subplots(figsize=(10, 6))
positions = range(len(attendance_data))

# Plot stacked bar graph for total tickets (light color) and attended tickets (dark red)
bars_total = ax1.bar(positions, attendance_data['total_tickets'], color='#f1948a', label='Total Tickets')
bars_attended = ax1.bar(positions, attendance_data['attended'], color='#ab162b', label='Attended Tickets')

# Set x and y labels
ax1.set_xlabel('Ticket Reference Amount')
ax1.set_ylabel('Number of Tickets')
plt.title('Total Tickets and Attended Tickets vs. Ticket Reference Price (2023)', color='black')

# Create a second y-axis to plot the attendance rate as a line graph
ax2 = ax1.twinx()
line_attendance_rate, = ax2.plot(positions, attendance_data['ATTENDANCE_RATE'], color='black', marker='o', label='Attendance Rate')
ax2.set_ylabel('Attendance Rate (%)')

# Set y-axis range for attendance rate to 0-100%
ax2.set_ylim(0, 100)

# Combine legends from both axes
handles, labels = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(handles + [line_attendance_rate], labels + [line_attendance_rate.get_label()], loc='upper right', bbox_to_anchor=(1,0.8))

# Show x-ticks with the ticket prices and rotate labels for readability
plt.xticks(positions, attendance_data.index, rotation=45)

# Adjust layout to prevent overlap
fig.tight_layout()

# Display the plot
plt.show()
