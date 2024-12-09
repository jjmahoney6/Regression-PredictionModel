import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file
data = pd.read_csv(r"C:\Users\Busti\OneDrive - Worcester Polytechnic Institute (wpi.edu)\MQP\MQP Python\sales_report_updated.csv", low_memory=False)

# Filter the dataset to only include rows where ADJ.PGS is 'S', 'P', or 'G'
data = data[data['ADJ.PGS'].isin(['S', 'P', 'G'])]

# Convert EVENT_USAGE_DATE to datetime if not already
data['EVENT_USAGE_DATE'] = pd.to_datetime(data['EVENT_USAGE_DATE'])

# Define exclusion dates and filter them out
exclude_dates = pd.to_datetime(['2024-04-02', '2024-07-04'])
data = data[~data['EVENT_USAGE_DATE'].isin(exclude_dates)]

# Set Day_Group based on GameDay
data['Day_Group'] = data['GameDay']

# Group by Day_Group and ADJ.PGS for total tickets and attended tickets
attendance_data = data.groupby(['Day_Group', 'ADJ.PGS']).agg(
    total_tickets=('SCANNED', 'count'),
    attended=('SCANNED', 'sum')
).reset_index()

# Define custom order for days of the week
day_order = ['Tue', 'Wed', 'Thu', 'Fri', 'Sat', 'Sun']
attendance_data['Day_Group'] = pd.Categorical(attendance_data['Day_Group'], categories=day_order, ordered=True)

# Sort data by day order
attendance_data = attendance_data.sort_values('Day_Group')

# Define different shades of red for each ticket type
ticket_type_colors = {
    'S': ('lightcoral', 'darkred'),  # Shade for singles
    'P': ('lightpink', 'darkmagenta'),  # Shade for packages
    'G': ('lightsalmon', 'darkorange')  # Shade for groups
}

# Plotting
fig, ax = plt.subplots(figsize=(10, 6))

# Bar positions for total tickets by day and ticket type
ticket_types = attendance_data['ADJ.PGS'].unique()
bar_width = 0.2
positions = {day: i for i, day in enumerate(day_order)}

# Plot stacked bar graph for total and attended tickets by day of the week and ticket type
for i, ticket_type in enumerate(ticket_types):
    subset = attendance_data[attendance_data['ADJ.PGS'] == ticket_type]
    x_positions = [positions[day] + i * bar_width for day in subset['Day_Group']]
    
    # Use the color for total and attended tickets
    total_color, attended_color = ticket_type_colors[ticket_type]
    
    # Stacked bar plot: plot total tickets first and attended tickets on top
    ax.bar(x_positions, subset['total_tickets'], width=bar_width, label=f'Total {ticket_type}', alpha=0.5, color=total_color)
    ax.bar(x_positions, subset['attended'], width=bar_width, label=f'Attended {ticket_type}', alpha=0.8, color=attended_color)

# Labeling and customizations
ax.set_xlabel('Day of the Week')
ax.set_ylabel('Ticket Count')
ax.set_title('Total Tickets Purchased vs Attended Tickets by Day of Week and Ticket Type (2024)')
ax.set_xticks(list(positions.values()))
ax.set_xticklabels(day_order)
ax.legend(title="Ticket Type", loc='upper right')

# Adjust layout for readability
plt.tight_layout()
plt.show()
