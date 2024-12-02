import pandas as pd 
import glob

#add path to Sales Report Data Cleaning.xlsx
sales_df = pd.read_excel('Sales Report Data Cleaning.xlsx')
#add path to Promotions+Weather24.csv created from 
promotion_df = pd.read_csv('24GameWeather/Promotions+Weather24.csv')

def combineAttendanceFiles():
    #Group all weekly attendance data into one csv file
    attendance_files = glob.glob('Attendance_Files/' + '*.csv')
    df = pd.concat((pd.read_csv(file) for file in attendance_files), ignore_index=True)
    df.to_csv('attendance.csv')
    return df

attendence_df = combineAttendanceFiles()

def getTicketCounts(sales_df, attendance_df):
    #clean out all complementary tickets
    sales_df['EVENT_USAGE_DATE'] = pd.to_datetime(sales_df['EVENT_USAGE_DATE'], format='%Y-%m-%d', utc=True)
    sales_df['EVENT_USAGE_DATE'] = sales_df['EVENT_USAGE_DATE'].dt.strftime('%Y-%m-%d')
    sales_df = sales_df[~sales_df['ADJ.PGS'].isin(['C','N','W'])]
    attendance_df = attendance_df[attendance_df['TICKET_ID'].isin(sales_df['TICKET_ID'])]
    
    attendance_df['EVENT_DATE'] = pd.to_datetime(attendance_df['EVENT_DATE'], format='%d-%b-%Y %I:%M %p', utc=True)
    attendance_df['EVENT_DATE'] = attendance_df['EVENT_DATE'].dt.strftime('%Y-%m-%d')
    
    #Rename tickets to different categories column
    sales_df['Name'] = sales_df['Name'].apply(categorize_name)

    sales_singles_df = sales_df[sales_df['Name'] == 'Singles']
    attendance_singles_df = attendance_df[attendance_df['TICKET_ID'].isin(sales_singles_df['TICKET_ID'])]
    sales_singles_df = sales_singles_df.groupby('EVENT_USAGE_DATE').size().reset_index(name='Sales_Singles_Count')
    attendance_singles_df = attendance_singles_df.groupby('EVENT_DATE').size().reset_index(name='Attendance_Singles_Count')
    singles_df = pd.merge(sales_singles_df, attendance_singles_df, how= 'inner', right_on='EVENT_DATE', left_on='EVENT_USAGE_DATE')
    singles_df = singles_df.drop(columns=['EVENT_DATE'])

    sales_groups_df = sales_df[sales_df['Name'] == 'Groups']
    attendance_groups_df = attendance_df[attendance_df['TICKET_ID'].isin(sales_groups_df['TICKET_ID'])]
    sales_groups_df = sales_groups_df.groupby('EVENT_USAGE_DATE').size().reset_index(name='Sales_Groups_Count')
    attendance_groups_df = attendance_groups_df.groupby('EVENT_DATE').size().reset_index(name='Attendance_Groups_Count')
    groups_df = pd.merge(sales_groups_df, attendance_groups_df, how= 'inner', right_on='EVENT_DATE', left_on ='EVENT_USAGE_DATE')
    groups_df = groups_df.drop(columns=['EVENT_DATE'])

    sales_packages_df = sales_df[sales_df['Name'] == 'Packages']
    attendance_packages_df = attendance_df[attendance_df['TICKET_ID'].isin(sales_packages_df['TICKET_ID'])]
    sales_packages_df = sales_packages_df.groupby('EVENT_USAGE_DATE').size().reset_index(name='Sales_Packages_Count')
    attendance_packages_df = attendance_packages_df.groupby('EVENT_DATE').size().reset_index(name='Attendance_Packages_Count')
    packages_df = pd.merge(sales_packages_df, attendance_packages_df, how= 'inner', right_on='EVENT_DATE', left_on ='EVENT_USAGE_DATE')
    packages_df = packages_df.drop(columns=['EVENT_DATE'])
    
    final_df = pd.merge(singles_df, groups_df, how='inner', on='EVENT_USAGE_DATE')
    final_df = pd.merge(final_df, packages_df, how='inner', on='EVENT_USAGE_DATE')
    final_df['Sales_Count'] = final_df['Sales_Singles_Count'] + final_df['Sales_Groups_Count'] + final_df['Sales_Packages_Count']
    final_df['Attendance_Count'] = final_df['Attendance_Singles_Count'] + final_df['Attendance_Groups_Count'] + final_df['Attendance_Packages_Count']
    return final_df

def categorize_name(condition):
    if 'Single' in str(condition):
        return 'Singles'
    elif 'Group' in str(condition):
        return 'Groups'
    elif 'Package' in str(condition):
        return 'Packages'
    else:
        return 'N/A'
    
def mergePromotions(sales_df, promotion_df):
    promotion_df['GAME_DATE'] = pd.to_datetime(promotion_df['GAME_DATE'], format='%m/%d/%y', utc=True)
    promotion_df['GAME_DATE'] = promotion_df['GAME_DATE'].dt.strftime('%Y-%m-%d')

    #Drop Faulty data columns 
    promotion_df = promotion_df.drop(columns=['Unnamed: 0', 'Unnamed: 13', 'Unnamed: 14'])
    final_df = pd.merge(sales_df, promotion_df, how='inner', left_on='EVENT_USAGE_DATE', right_on='GAME_DATE')
    final_df = final_df.drop(columns=['GAME_DATE'])
    final_df.sort_values(by='EVENT_USAGE_DATE', ascending=True, inplace=True)

    return final_df


final_df = getTicketCounts(sales_df=sales_df, attendance_df=attendence_df)
final_df = mergePromotions(sales_df=final_df, promotion_df=promotion_df)
final_df.drop(columns=['Unnamed: 0'])
final_df.to_csv('testScript.csv')
