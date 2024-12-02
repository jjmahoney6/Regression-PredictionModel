# March 18 times that seem to be when ticket status was altered
# 8:58, 8:59, 9:00




import pandas as pd

# Load the Excel files
file_0315 = pd.read_csv(r"C:\Users\Busti\Documents\MQP DATA\Ticket Sales Export Singles 20240315.csv")
file_0318 = pd.read_csv(r"C:\Users\Busti\Documents\MQP DATA\Ticket Sales Export Singles 20240318.csv")
file_0322 = pd.read_csv(r"C:\Users\Busti\Documents\MQP DATA\Ticket Sales Export Singles 20240322.csv")
file_0325 = pd.read_csv(r"C:\Users\Busti\Documents\MQP DATA\Ticket Sales Export Singles 20240325.csv")
file_0326 = pd.read_csv(r"C:\Users\Busti\Documents\MQP DATA\Ticket Sales Export Singles 20240326.csv")

# Define the incorrect dates that need replacement
incorrect_dates = ["3/18/2024 8:58", "3/18/2024 8:59", "3/18/2024 9:00"]

# Convert TRANSACTION_DATE columns to datetime for consistency
file_0315['TRANSACTION_DATE'] = pd.to_datetime(file_0315['TRANSACTION_DATE'], errors='coerce')
file_0318['TRANSACTION_DATE'] = pd.to_datetime(file_0318['TRANSACTION_DATE'], errors='coerce')

# Filter rows in file_0318 with the incorrect dates
rows_to_update = file_0318['TRANSACTION_DATE'].isin(pd.to_datetime(incorrect_dates))

# Iterate over the rows that need updating
for index, row in file_0318[rows_to_update].iterrows():
    # Find matching rows in file_0315 based on FINANCIAL_ACCOUNT_ID
    matching_rows = file_0315[file_0315['FINANCIAL_ACCOUNT_ID'] == row['FINANCIAL_ACCOUNT_ID']]
    
    # Check if there's a valid previous TRANSACTION_DATE in file_0315
    if not matching_rows.empty:
        # Use the earliest TRANSACTION_DATE from file_0315 for consistency
        previous_date = matching_rows['TRANSACTION_DATE'].min()
        # Update the TRANSACTION_DATE in file_0318
        file_0318.at[index, 'TRANSACTION_DATE'] = previous_date

# Save the updated file_0318 data to a new CSV file
file_0318.to_csv('SinglesTransactionDataReverted.csv', index=False)

