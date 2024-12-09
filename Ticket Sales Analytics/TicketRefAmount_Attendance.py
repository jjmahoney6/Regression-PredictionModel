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
    'text.color': '#FFFFFF',
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
fig, ax1 = plt.subplots(figsize=(12, 8))

# Plot stacked bar graph for total tickets (light color) and attended tickets (dark red)
ax1.bar(attendance_data.index, attendance_data['total_tickets'], color='lightgray', label='Total Tickets')
ax1.bar(attendance_data.index, attendance_data['attended'], color='#ab162b', label='Attended Tickets')

# Set x and y labels
ax1.set_xlabel('Ticket Paid Amount')
ax1.set_ylabel('Number of Tickets')
plt.title('Total Tickets and Attended Tickets by Ticket Paid Amount', color='black')

# Add total tickets and attended tickets labels above each bar
for i in range(len(attendance_data)):
    ax1.text(attendance_data.index[i], attendance_data['total_tickets'].iloc[i] + 1,
             f'{attendance_data["total_tickets"].iloc[i]}', ha='center', va='bottom', fontsize=8)
    ax1.text(attendance_data.index[i], attendance_data['attended'].iloc[i] + 1,
             f'{attendance_data["attended"].iloc[i]}', ha='center', va='bottom', fontsize=8)

# Create a second y-axis to plot the attendance rate as a line graph
ax2 = ax1.twinx()
ax2.plot(attendance_data.index, attendance_data['ATTENDANCE_RATE'], color='black', marker='o', label='Attendance Rate')
ax2.set_ylabel('Attendance Rate (%)')

# Set y-axis range for attendance rate to 0-100%
ax2.set_ylim(0, 100)

# Add attendance rate labels on top of the line graph
for i in range(len(attendance_data)):
    ax2.text(attendance_data.index[i], attendance_data['ATTENDANCE_RATE'].iloc[i] + 1,
             f'{attendance_data["ATTENDANCE_RATE"].iloc[i]:.1f}%', ha='center', va='bottom', fontsize=8)

# Show the plot with tight layout
fig.tight_layout()

# Display the plot
plt.show()
