import pandas as pd
import matplotlib.pyplot as plt

# Define the specific ticket price to filter
specific_ticket_price = 27  # Change this to your desired ticket price

# Load the CSV file
data = pd.read_csv(r"C:\Users\Busti\OneDrive - Worcester Polytechnic Institute (wpi.edu)\MQP\MQP Python\sales_report_updated.csv", low_memory=False)

# Filter for "singles" tickets only and for the specific ticket price
data = data[(data['ADJ.PGS'] == 'S') & (data['TICKET_PAID_AMOUNT'] == specific_ticket_price)]

# Ensure EVENT_USAGE_DATE is in datetime format
data['EVENT_USAGE_DATE'] = pd.to_datetime(data['EVENT_USAGE_DATE'])

# Filter out specific event dates
exclude_dates = pd.to_datetime(['2024-04-02', '2024-07-04'])
data = data[(~data['EVENT_USAGE_DATE'].isin(exclude_dates))]

# Section capacity data (use the section capacities from the image)
section_capacity = {
    "Section 1": 393, "Section 2": 278, "Section 3": 314, "Section 4": 185, "Section 5": 319,
    "Section 6": 279, "Section 7": 366, "Section 8": 275, "Section 9": 403, "Section 10": 296,
    "Section 11": 361, "Section 12": 241, "Section 13": 298, "Section 14": 231, "Section 15": 261,
    "Section 16": 121, "Suites": 460, "Bridge": 35, "Section 201": 36, "Section 202": 46,
    "Section 203": 59, "Section 204": 48, "Section 205": 77, "Section 206": 79, "Section 207": 55,
    "Section 101": 46, "Section 102": 50, "Section 103": 50, "Section 104": 50, "Section 105": 65,
    "Yuengling Flight Deck": 34, "Shaw's Home Bullpen Terrace": 100, "Triple Decker Garden": 150,
    "Flexcon Landing": 100, "Hanover Deck": 225, "Shaw's Visitors Bullpen Terrace": 200,
    "University Dental Group Berm": 700, "Big Blue Bug Batter's Box": 15, "General Admission": 5000
}

# Map total sellable capacity to each section in the data
data['Total_Sellable_Capacity'] = data['SECTION_DESC'].map(section_capacity)

# Group by SECTION_DESC and EVENT_USAGE_DATE to calculate attendance rate per event
attendance_data = data.groupby(['SECTION_DESC', 'EVENT_USAGE_DATE']).agg(
    total_tickets=('SCANNED', 'count'),
    attended=('SCANNED', 'sum'),
    capacity=('Total_Sellable_Capacity', 'first')
).reset_index()

# Calculate attendance rate for each event and section
attendance_data['ATTENDANCE_RATE'] = (attendance_data['attended'] / attendance_data['capacity']) * 100

# Calculate the average attendance rate across all events for each section
average_attendance = attendance_data.groupby('SECTION_DESC')['ATTENDANCE_RATE'].mean().reset_index()

# Plot the average attendance rate by ballpark section
fig, ax = plt.subplots(figsize=(12, 6))
ax.bar(average_attendance['SECTION_DESC'], average_attendance['ATTENDANCE_RATE'], color='skyblue')
ax.set_xlabel('Ballpark Section')
ax.set_ylabel('Average Attendance Rate (%)')
ax.set_title(f'Average Attendance Rate by Ballpark Section for Tickets Priced at ${specific_ticket_price}')
ax.set_xticklabels(average_attendance['SECTION_DESC'], rotation=45, ha='right')

plt.tight_layout()
plt.show()
