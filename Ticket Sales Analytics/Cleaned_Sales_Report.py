import pandas as pd

# Load the Excel files
sales_report = pd.read_csv(r"C:\Users\Busti\Documents\MQP DATA\Sales Report Data Cleaning.csv")
singles_cleaned = pd.read_csv(r"C:\Users\Busti\OneDrive\Documents\PythonWork\MQP Python\SinglesTicketDataUpdated.csv")

# Remove rows where ADJ.PGS contains 'C', 'W', or 'N'
sales_report = sales_report[~sales_report['ADJ.PGS'].isin(['C', 'W', 'N'])]

# Remove the 4 singles tickets that have a TRANSACTION_DATE  over a month after the EVENT_USAGE_DATE
# Define the list of TICKET_IDs to remove
ticket_ids_to_remove = [160568093, 160568094, 160568095, 160568096]

# Remove rows where TICKET_ID is in the list of IDs to remove
sales_report = sales_report[~sales_report['TICKET_ID'].isin(ticket_ids_to_remove)]

# Convert TRANSACTION_DATE columns to datetime for consistency
sales_report['TRANSACTION_DATE'] = pd.to_datetime(sales_report['TRANSACTION_DATE'], errors='coerce')
singles_cleaned['TRANSACTION_DATE'] = pd.to_datetime(singles_cleaned['TRANSACTION_DATE'], errors='coerce')

# Remove time from TRANSACTION_DATE in singles_cleaned
singles_cleaned['TRANSACTION_DATE'] = singles_cleaned['TRANSACTION_DATE'].dt.date

# Create a dictionary from singles_cleaned with TICKET_ID as keys and TRANSACTION_DATE as values
transaction_date_dict = singles_cleaned.set_index('TICKET_ID')['TRANSACTION_DATE'].to_dict()

# Update TRANSACTION_DATE in sales_report using the dictionary, keeping only the date
sales_report['TRANSACTION_DATE'] = sales_report.apply(
    lambda row: transaction_date_dict.get(row['TICKET_ID'], row['TRANSACTION_DATE'].date()) 
                if pd.notnull(row['TRANSACTION_DATE']) else row['TRANSACTION_DATE'],
    axis=1
)

# Save the updated sales_report data to a new CSV file
sales_report.to_csv('sales_report_updated.csv', index=False)

print("Updated TRANSACTION_DATE values in sales_report with date-only format and saved as sales_report_updated.csv.")
