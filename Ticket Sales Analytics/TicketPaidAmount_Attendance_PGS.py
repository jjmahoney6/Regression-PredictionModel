import pandas as pd
import matplotlib.pyplot as plt
import numpy as np

# Parameters for filtering ticket price range
price_min = 0    # Minimum ticket price to include
price_max = 60   # Maximum ticket price to include

# Load the CSV file
data = pd.read_csv(r"C:\Users\Busti\OneDrive - Worcester Polytechnic Institute (wpi.edu)\MQP\MQP Python\sales_report_updated.csv", low_memory=False)

# Filter by the specified TICKET_PAID_AMOUNT range
data = data[(data['TICKET_PAID_AMOUNT'] >= price_min) & (data['TICKET_PAID_AMOUNT'] <= price_max)]

# Filter by ADJ.PGS column values
data = data[data['ADJ.PGS'].isin(['S', 'P', 'G'])]

# Create a DataFrame with all possible TICKET_PAID_AMOUNT and ADJ.PGS combinations in the specified range
ticket_prices = np.arange(price_min, price_max + 1)  # Adjust based on your price range
ticket_types = ['S', 'P', 'G']
all_combinations = pd.MultiIndex.from_product([ticket_prices, ticket_types], names=['TICKET_PAID_AMOUNT', 'ADJ.PGS'])
attendance_data = pd.DataFrame(index=all_combinations).reset_index()

# Merge with actual data, filling missing entries with zero for `total_tickets` and `attended`
merged_data = data.groupby(['TICKET_PAID_AMOUNT', 'ADJ.PGS']).agg(
    total_tickets=('SCANNED', 'count'),
    attended=('SCANNED', 'sum')
).reset_index()

attendance_data = attendance_data.merge(merged_data, on=['TICKET_PAID_AMOUNT', 'ADJ.PGS'], how='left').fillna(0)
attendance_data['ATTENDANCE_RATE'] = (attendance_data['attended'] / attendance_data['total_tickets']).fillna(0) * 100

# Define colors for each category
colors = {'S': 'skyblue', 'P': 'orange', 'G': 'green'}
categories = attendance_data['ADJ.PGS'].unique()

# Graph 1: Attendance Rate by TICKET_PAID_AMOUNT with Singles, Packages, and Groups
plt.figure(figsize=(14, 8))

for i, category in enumerate(categories):
    subset = attendance_data[attendance_data['ADJ.PGS'] == category]
    positions = np.arange(len(subset['TICKET_PAID_AMOUNT'])) + i * 0.25
    plt.bar(positions, subset['ATTENDANCE_RATE'], width=0.25, color=colors[category], label=category)

# Label axes and add title
plt.xlabel('Ticket Paid Amount')
plt.ylabel('Attendance Rate (%)')
plt.title('Attendance Rate by Ticket Paid Amount (Singles, Packages, and Groups)')
plt.xticks(np.arange(len(ticket_prices)) + 0.25, ticket_prices, rotation=45)
plt.legend(title='Ticket Type', labels=['Singles', 'Packages', 'Groups'])

# Attendance rate labels above each bar, excluding 0.0% labels
for i, category in enumerate(categories):
    subset = attendance_data[attendance_data['ADJ.PGS'] == category]
    for j in range(len(subset)):
        if subset['ATTENDANCE_RATE'].iloc[j] > 0:  # Only show label if attendance rate > 0
            plt.text(j + i * 0.25, subset['ATTENDANCE_RATE'].iloc[j] + 1,
                     f'{subset["ATTENDANCE_RATE"].iloc[j]:.1f}%', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()

# Graph 2: Total Tickets Purchased by TICKET_PAID_AMOUNT for Singles, Packages, and Groups
plt.figure(figsize=(14, 8))

for i, category in enumerate(categories):
    subset = attendance_data[attendance_data['ADJ.PGS'] == category]
    positions = np.arange(len(subset['TICKET_PAID_AMOUNT'])) + i * 0.25
    plt.bar(positions, subset['total_tickets'], width=0.25, color=colors[category], label=category)

# Label axes and add title
plt.xlabel('Ticket Paid Amount')
plt.ylabel('Total Tickets Purchased')
plt.title('Total Tickets Purchased by Ticket Paid Amount (Singles, Packages, and Groups)')
plt.xticks(np.arange(len(ticket_prices)) + 0.25, ticket_prices, rotation=45)
plt.legend(title='Ticket Type', labels=['Singles', 'Packages', 'Groups'])

# Total ticket labels above each bar, excluding 0 labels
for i, category in enumerate(categories):
    subset = attendance_data[attendance_data['ADJ.PGS'] == category]
    for j in range(len(subset)):
        if subset['total_tickets'].iloc[j] > 0:  # Only show label if total tickets > 0
            plt.text(j + i * 0.25, subset['total_tickets'].iloc[j] + 1,
                     f'{int(subset["total_tickets"].iloc[j])}', ha='center', va='bottom', fontsize=8)

plt.tight_layout()
plt.show()
