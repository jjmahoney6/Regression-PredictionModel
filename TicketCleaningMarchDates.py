import pandas as pd


# Function to change the TRANSACTION_DATE in the more recent file to the original TRANSACTION_DATE, where file_to_update is the file path
# that you want to change, reference_file is the file path that provides the TRANSACTION_DATE file_to_update will be changed to, and
# output_file is the name of the file
def update_transaction_dates(file_to_update, reference_file, output_file):
    # Load the recent and old CSV files
    recent_file = pd.read_csv(file_to_update)
    old_file = pd.read_csv(reference_file)

    # Convert TRANSACTION_DATE columns to datetime, ignore errors for empty values
    recent_file['TRANSACTION_DATE'] = pd.to_datetime(recent_file['TRANSACTION_DATE'], errors='coerce')
    old_file['TRANSACTION_DATE'] = pd.to_datetime(old_file['TRANSACTION_DATE'], errors='coerce')

    # Keep only the date (no time) in TRANSACTION_DATE for old_file
    old_file['TRANSACTION_DATE'] = old_file['TRANSACTION_DATE'].dt.date

    # Create a dictionary from old_file with FINANCIAL_ACCOUNT_ID as keys and TRANSACTION_DATE as values
    transaction_date_dict = old_file.set_index('FINANCIAL_ACCOUNT_ID')['TRANSACTION_DATE'].to_dict()

    # Function to apply the replacement logic
    def replace_date(row):
        # Get the old date based on FINANCIAL_ACCOUNT_ID
        old_date = transaction_date_dict.get(row['FINANCIAL_ACCOUNT_ID'])
        # Replace only if old date is valid and differs from recent TRANSACTION_DATE
        if old_date and row['TRANSACTION_DATE'].date() != old_date:
            return old_date  # Use date-only format
        return row['TRANSACTION_DATE'].date()  # Keep original date if no replacement

    # Apply the replacement function to recent_file
    recent_file['TRANSACTION_DATE'] = recent_file.apply(replace_date, axis=1)

    # Save the updated file_0318_data to a new CSV file
    recent_file.to_csv(output_file, index=False)
    print(f"Updated TRANSACTION_DATE values in {file_to_update} based on {reference_file} and saved as {output_file}.")


# Runs the function to change the TRANSACTION_DATE back to the initial TRANSACTION_DATE
update_transaction_dates(r"C:\Users\Busti\Documents\MQP DATA\Ticket Sales Export Singles 20240318.csv",
                         r"C:\Users\Busti\Documents\MQP DATA\Ticket Sales Export Singles 20240315.csv",
                         'SinglesTicketDataUpdated.csv')
update_transaction_dates(r"C:\Users\Busti\Documents\MQP DATA\Ticket Sales Export Packages 20240319.csv",
                         r"C:\Users\Busti\Documents\MQP DATA\Ticket Sales Export Packages 20240318.csv",
                         '0318_PackagesTicketDataUpdated.csv')                         
