import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
data = pd.read_csv(r"C:\Users\Busti\OneDrive - Worcester Polytechnic Institute (wpi.edu)\MQP\MQP Python\sales_report_updated.csv", low_memory=False)
data = data[data['ADJ.PGS'] == 'S']  # Filter for 'singles' only

# Parameters to specify the price range
price_min = 0    # Minimum ticket price to include
price_max = 100   # Maximum ticket price to include
min_ticket_threshold = 0  # Minimum number of tickets required for a price to be included

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

# Bar Graph 1: Attendance Rate by TICKET_PAID_AMOUNT
plt.figure(figsize=(10, 6))
plt.bar(attendance_data.index, attendance_data['ATTENDANCE_RATE'], color='skyblue')
plt.xlabel('Ticket Paid Amount')
plt.ylabel('Attendance Rate (%)')
plt.title('Attendance Rate by Ticket Paid Amount')
plt.xticks(rotation=45)

# Add attendance rate labels on top of each bar
for i in range(len(attendance_data)):
    plt.text(attendance_data.index[i], attendance_data['ATTENDANCE_RATE'].iloc[i] + 1,
             f'{attendance_data["ATTENDANCE_RATE"].iloc[i]:.1f}%', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()

# Bar Graph 2: Total Tickets and Attended Tickets by TICKET_PAID_AMOUNT
plt.figure(figsize=(12, 8))

# Define bar width and positions for side-by-side bars
bar_width = 0.4
positions = range(len(attendance_data))

# Plot total tickets and attended tickets side by side
plt.bar([p - bar_width/2 for p in positions], attendance_data['total_tickets'], width=bar_width, color='skyblue', label='Total Tickets')
plt.bar([p + bar_width/2 for p in positions], attendance_data['attended'], width=bar_width, color='orange', label='Attended Tickets')

# Labels and title
plt.xlabel('Ticket Paid Amount')
plt.ylabel('Number of Tickets')
plt.title('Total Tickets vs Attended Tickets by Ticket Paid Amount')
plt.xticks(positions, attendance_data.index, rotation=45)
plt.legend()

# Add total tickets and attended tickets labels above each bar
for i in range(len(attendance_data)):
    plt.text(i - bar_width/2, attendance_data['total_tickets'].iloc[i] + 1,
             f'{attendance_data["total_tickets"].iloc[i]}', ha='center', va='bottom', fontsize=8)
    plt.text(i + bar_width/2, attendance_data['attended'].iloc[i] + 1,
             f'{attendance_data["attended"].iloc[i]}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()
