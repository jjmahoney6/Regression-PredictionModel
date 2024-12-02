import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Parameters for filtering
price_min = 9   # Minimum ticket price to include
price_max = 27  # Maximum ticket price to include
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

# Group by TICKET_PAID_AMOUNT and SECTION_DESC to calculate total tickets and attended tickets
attendance_data = data.groupby(['TICKET_PAID_AMOUNT', 'SECTION_DESC']).agg(
    total_tickets=('SCANNED', 'count'),
    attended_tickets=('SCANNED', 'sum')
).reset_index()

# Calculate the attendance percentage
attendance_data['ATTENDANCE_RATE'] = (attendance_data['attended_tickets'] / attendance_data['total_tickets']) * 100

# Filter out TICKET_PAID_AMOUNT entries with fewer total tickets than the threshold
attendance_data = attendance_data[attendance_data['total_tickets'] >= min_ticket_threshold]

# Define unique ticket prices and sections for consistent order in plotting
unique_ticket_prices = sorted(attendance_data['TICKET_PAID_AMOUNT'].unique())
unique_sections = sorted(attendance_data['SECTION_DESC'].unique())
num_sections = len(unique_sections)
bar_width = 0.05
x_positions = np.arange(len(unique_ticket_prices))

# Plotting the attendance percentage by ticket price and section
fig, ax = plt.subplots(figsize=(14, 8))

for i, section in enumerate(unique_sections):
    # Filter data for each section and reindex by ticket price
    subset = attendance_data[attendance_data['SECTION_DESC'] == section].set_index('TICKET_PAID_AMOUNT').reindex(unique_ticket_prices, fill_value=0).reset_index()
    
    # Plot attendance rate for each section
    ax.bar(x_positions + i * bar_width, subset['ATTENDANCE_RATE'], width=bar_width, label=section)

# Labeling and customizations
ax.set_xlabel('Ticket Paid Amount')
ax.set_ylabel('Attendance Rate (%)')
ax.set_title('Attendance Rate by Ticket Paid Amount and Section (Singles Only)')
ax.set_xticks(x_positions + (num_sections - 1) * bar_width / 2)
ax.set_xticklabels(unique_ticket_prices, rotation=45)
ax.legend(title="Ballpark Section")

# Show the plot
plt.tight_layout()
plt.show()
