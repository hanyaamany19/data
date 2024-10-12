import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Set style untuk seaborn
st.set_page_config(page_title="Bike Usage Data Analysis", layout="wide", initial_sidebar_state="expanded")

# Membaca data dari CSV
hour_df = pd.read_csv("hour1.csv", sep=";")
day_df = pd.read_csv("day.csv")

st.write("Columns in day_df:", day_df.columns)
st.write("Columns in hour_df:", hour_df.columns)

st.write(day_df.head())
st.write(hour_df.head())

# Rename kolom di day.csv untuk lebih mudah dipahami
day_df.rename(columns={
    'season': 'season',
    'yr': 'year',
    'mnth': 'month',  # Mengganti 'mnth' menjadi 'month' untuk lebih mudah dipahami
    'holiday': 'holiday',
    'weekday': 'weekday',
    'workingday': 'working_day',
    'weathersit': 'weather_condition',
    'temp': 'temperature',
    'atemp': 'feels_like_temperature',
    'hum': 'humidity',
    'windspeed': 'wind_speed',
    'casual': 'casual_users',
    'registered': 'registered_users',
    'cnt': 'total_users'
}, inplace=True)

# Mengubah angka menjadi keterangan
day_df['month'] = day_df['month'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
})
day_df['season'] = day_df['season'].map({
    1: 'Spring', 2: 'Summer', 3: 'Fall', 4: 'Winter'
})
day_df['weather_condition'] = day_df['weather_condition'].map({
    1: 'Clear/Partly Cloudy',
    2: 'Foggy/Cloudy',
    3: 'Snow/Light Rain',
    4: 'Extreme Weather'
})

# 1. Effect of weather conditions on bike usage
st.header("Effect of Weather Conditions on Bike Usage")

# Scatter plot for temperature and humidity against total users
fig, ax = plt.subplots(1, 2, figsize=(14, 6))

# Plot 1: Temperature vs Total Users
sns.scatterplot(x='temperature', y='total_users', data=day_df, ax=ax[0], hue='weather_condition', palette='viridis')
ax[0].set_title('Effect of Temperature on Bike Usage')
ax[0].set_xlabel('Temperature')
ax[0].set_ylabel('Total Users')

# Plot 2: Humidity vs Total Users
sns.scatterplot(x='humidity', y='total_users', data=day_df, ax=ax[1], hue='weather_condition', palette='coolwarm')
ax[1].set_title('Effect of Humidity on Bike Usage')
ax[1].set_xlabel('Humidity')
ax[1].set_ylabel('Total Users')

st.pyplot(fig)

# 2. Comparison of bike usage on weekdays, holidays, and weekends (hour.csv)
st.header("Comparison of Bike Usage: Weekdays vs Holidays/Weekends")

# Rename columns in hour.csv
hour_df.rename(columns={
    'holiday': 'holiday',
    'workingday': 'working_day',
    'cnt': 'total_users',
    'weekday': 'weekday',
    'hr': 'hour'
}, inplace=True)

# Add a new column for weekday, holiday, and weekend categories
hour_df['day_category'] = hour_df.apply(
    lambda row: 'Holiday' if row['holiday'] == 1 else 'Weekday' if row['working_day'] == 1 else 'Weekend', axis=1
)

# Create boxplot for comparing bike usage on weekdays, holidays, and weekends
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(x='day_category', y='total_users', data=hour_df, palette='Set2')
ax.set_title('Comparison of Bike Usage on Weekdays vs Holidays/Weekends')
ax.set_xlabel('Day Category')
ax.set_ylabel('Total Users')

st.pyplot(fig)
