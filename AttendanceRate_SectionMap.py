import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.image as mpimg

# Load the CSV file
data = pd.read_csv(r"C:\Users\Busti\OneDrive - Worcester Polytechnic Institute (wpi.edu)\MQP\MQP Python\sales_report_updated.csv", low_memory=False)

# Filter for "singles" tickets only
# data = data[data['ADJ.PGS'] == 'S']

# Specify the days of the week to include in the analysis (e.g., 'Mon', 'Tue', 'Wed', etc.)
# chosen_days = ['Fri', 'Sat']  # Adjust this list as needed

# Filter the data for the chosen days of the week
data = data[data['GameDay'].isin(chosen_days)]

# Ensure EVENT_USAGE_DATE is in datetime format
data['EVENT_USAGE_DATE'] = pd.to_datetime(data['EVENT_USAGE_DATE'])

# Filter out specific event dates
exclude_dates = pd.to_datetime(['2024-04-02', '2024-07-04'])
data = data[~data['EVENT_USAGE_DATE'].isin(exclude_dates)]

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

# Group by SECTION_DESC and EVENT_USAGE_DATE to calculate attendance rate for each game
attendance_data = data.groupby(['SECTION_DESC', 'EVENT_USAGE_DATE']).agg(
    attended=('SCANNED', 'sum'),
    capacity=('Total_Sellable_Capacity', 'first')
).reset_index()

# Calculate attendance rate for each game
attendance_data['ATTENDANCE_RATE'] = (attendance_data['attended'] / attendance_data['capacity']) * 100

# Calculate the average attendance rate across all events for each section
average_attendance = attendance_data.groupby('SECTION_DESC')['ATTENDANCE_RATE'].mean().reset_index()

# Coordinates for each section on the ballpark blueprint (example values)
section_coordinates = {
    "Section 1": (689,184), "Section 2": (661,162), "Section 3": (626,148), "Section 4": (609,137), "Section 5": (585,124),
    "Section 6": (564,112), "Section 7": (538,96), "Section 8": (513,88), "Section 9": (481,96), "Section 10": (441,87),
    "Section 11": (422,99), "Section 12": (399,113), "Section 13": (376,126), "Section 14": (341,136), "Section 15": (326,150),
    "Section 16": (307,165), "Suites": (291,91), "Bridge": (198,162), "Section 201": (555,62), "Section 202": (530,49),
    "Section 203": (511,49), "Section 204": (484,50), "Section 205": (449,46), "Section 206": (422,51), "Section 207": (398,63),
    "Section 101": (108,275), "Section 102": (121,302), "Section 103": (140,325), "Section 104": (157,341), "Section 105": (177,372),
    "Yuengling Flight Deck": (490,577), "Shaw's Home Bullpen Terrace": (258,184), "Triple Decker Garden": (260,465),
    "Flexcon Landing": (320,499), "Hanover Deck": (801,182), "Shaw's Visitors Bullpen Terrace": (823,249),
    "University Dental Group Berm": (684,531), "Big Blue Bug Batter's Box": (415,142), "General Admission": (785,469)
}

# Load the ballpark blueprint
blueprint_img = mpimg.imread(r"C:\Users\Busti\OneDrive - Worcester Polytechnic Institute (wpi.edu)\MQP\MQP Python\PolarPark_SeatingMap.jpg")  # Update with the actual path

# Plot the blueprint
fig, ax = plt.subplots(figsize=(14, 10))
ax.imshow(blueprint_img)

# Overlay attendance percentages on the blueprint
for _, row in average_attendance.iterrows():
    section = row['SECTION_DESC']
    attendance_rate = row['ATTENDANCE_RATE']
    if section in section_coordinates:
        x, y = section_coordinates[section]
        ax.text(x, y, f"{attendance_rate:.1f}%", color="black", fontsize=8, ha="center", va="center", bbox=dict(facecolor='white', edgecolor='none', alpha=0.8, pad=1))

# Customize the plot
ax.axis('off')  # Hide axes
plt.title("Average Attendance Rate by Ballpark Section", fontsize=16)
plt.show()
