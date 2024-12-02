import json
import pandas as pd

with open('cleaned_file.json', 'r') as f:
    data = json.load(f)

# Convert JSON data into a DataFrame
dfs = []
for entry in data:
    df = pd.json_normalize(entry['forecast']['forecastday'])
    dfs.append(df)

#create combined Dataframe with all entries
combined_df = pd.concat(dfs, ignore_index=True)
#Specifically look at date, max, min and avg temp, chance of rain or snow, and the condition
combined_df = combined_df[['date', 'day.maxtemp_f', 'day.mintemp_f', 'day.avgtemp_f', 'day.daily_chance_of_rain', 'day.daily_chance_of_snow', 'day.condition.text']]

# Display the DataFrame
combined_df.rename(columns={'date': 'GAME_DATE', 'day.maxtemp_f': 'max_temp', 'day.mintemp_f' : 'min_temp', 'day.avgtemp_f': 'avgtemp', 'day.daily_chance_of_rain' : 'Rain', 'day.daily_chance_of_snow' : 'Snow', 'day.condition.text': 'Condition'}, inplace=True)

print(combined_df.head(5))

#save as a csv file
combined_df.to_csv('weather_data.csv')

#%%
import pandas as pd

#Load in promotion and weather dataset 
promotion_df = pd.read_csv('promotions.csv')
weather_df = pd.read_csv('weather_data.csv')
promotion_df = promotion_df[['GAME_DATE', 'DAY', 'Weather', 'Temp', 'Game']]

#format GameDate to the same as weather dataset
promotion_df['GAME_DATE'] = pd.to_datetime(promotion_df['GAME_DATE'], format='%m/%d/%Y')
promotion_df['GAME_DATE'] = promotion_df['GAME_DATE'].dt.strftime('%Y-%m-%d')

#merge datasets (grab weather data for only gamedays)
final_df = pd.merge(weather_df, promotion_df, how='inner', on='GAME_DATE')

#convert to CSV file
final_df.to_csv('Promotions+Weather24.csv')
# %%
