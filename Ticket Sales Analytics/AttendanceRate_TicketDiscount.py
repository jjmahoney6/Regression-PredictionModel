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

# Filter for 'singles' only
data = data[data['ADJ.PGS'] == 'S']

# Create a new column for discount category
def discount_category(row):
    if row['TICKET_PAID_AMOUNT'] > row['TICKET_REF_PRICE']:
        return 'Paid Above Ref Price'
    elif row['TICKET_PAID_AMOUNT'] == row['TICKET_REF_PRICE']:
        return 'No Discount (0%)'
    elif row['TICKET_PAID_AMOUNT'] == 0:
        return '100% Discount'
    elif row['TICKET_PAID_AMOUNT'] / row['TICKET_REF_PRICE'] < 0.5:
        return 'More than 50% Discount'
    else:
        return 'Less than 50% Discount'

# Apply the updated function
data['DISCOUNT_CATEGORY'] = data.apply(discount_category, axis=1)


# Group data by discount category and calculate total tickets and attendance rate
attendance_data = data.groupby('DISCOUNT_CATEGORY').agg(
    total_tickets=('SCANNED', 'count'),
    attended=('SCANNED', 'sum')
)

# Calculate attendance rate as a percentage
attendance_data['ATTENDANCE_RATE'] = (attendance_data['attended'] / attendance_data['total_tickets']) * 100

# Define the desired order for the discount categories
category_order = [
    'Paid Above Ref Price',
    'No Discount (0%)',
    'Less than 50% Discount',
    'More than 50% Discount',
    '100% Discount'
]

# Reorder the DataFrame based on the category order
attendance_data = attendance_data.reindex(category_order)

# Create the combined bar and line graph
fig, ax1 = plt.subplots(figsize=(10, 6))
categories = attendance_data.index
positions = range(len(categories))

# Plot bar graph for total tickets
bars_total = ax1.bar(positions, attendance_data['total_tickets'], color='#ab162b', label='Total Tickets')

# Set x and y labels
ax1.set_xlabel('Discount Category')
ax1.set_ylabel('Number of Tickets')
plt.title('Total Tickets and Attendance Rate by Discount Category (2024)', color='black')

# Add labels above each bar
for i, bar in enumerate(bars_total):
    height = bar.get_height()
    ax1.text(bar.get_x() + bar.get_width() / 2, height + 50, f'{int(height)}', ha='center', va='bottom', color='black')

# Create a second y-axis to plot the attendance rate as a line graph
ax2 = ax1.twinx()
line_attendance_rate, = ax2.plot(positions, attendance_data['ATTENDANCE_RATE'], color='black', marker='o', label='Attendance Rate')
ax2.set_ylabel('Attendance Rate (%)')

# Add labels above each point on the line graph
for i, rate in enumerate(attendance_data['ATTENDANCE_RATE']):
    ax2.text(positions[i], rate + 2, f'{rate:.1f}%', ha='center', va='bottom', color='black')

# Set y-axis range for attendance rate to 0-100%
ax2.set_ylim(0, 100)

# Combine legends from both axes
handles, labels = ax1.get_legend_handles_labels()
handles2, labels2 = ax2.get_legend_handles_labels()
ax1.legend(handles + [line_attendance_rate], labels + [line_attendance_rate.get_label()], loc='upper right', bbox_to_anchor=(1, 0.8))

# Show x-ticks with discount categories and rotate labels for readability
plt.xticks(positions, categories, rotation=45)

# Adjust layout to prevent overlap
fig.tight_layout()

# Display the plot
plt.show()
