import pandas as pd
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns

# Set style untuk seaborn
st.set_page_config(page_title="Analisis Data Penggunaan Sepeda", layout="wide", initial_sidebar_state="expanded")

# Membaca data dari CSV
hour_df = pd.read_csv("hour.csv", sep=';')
day_df = pd.read_csv("day.csv", sep=';')

# Rename kolom di day.csv untuk lebih mudah dipahami

day_df.rename(columns={
    'season': 'musim',
    'yr': 'tahun',
    'mnth': 'bulan',
    'weekday': 'hari_kerja',
    'weathersit': 'kondisi_cuaca',
    'temp': 'suhu',
    'atemp': 'suhu_terasa',
    'hum': 'kelembaban',
    'windspeed': 'kecepatan_angin',
    'casual': 'pengguna_casual',
    'registered': 'pengguna_terdaftar',
    'cnt': 'total_pengguna'
}, inplace=True)

# Mengubah angka menjadi keterangan
day_df['bulan'] = day_df['bulan'].map({
    1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun',
    7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec'
})
day_df['musim'] = day_df['musim'].map({
    1: 'Musim Semi', 2: 'Musim Panas', 3: 'Musim Gugur', 4: 'Musim Dingin'
})
day_df['kondisi_cuaca'] = day_df['kondisi_cuaca'].map({
    1: 'Cerah/Agak Berawan',
    2: 'Berkabut/Berawan',
    3: 'Salju/Rintik Hujan',
    4: 'Cuaca Ekstrem'
})

# 1. Pengaruh kondisi cuaca terhadap jumlah pengguna sepeda
st.header("Pengaruh Kondisi Cuaca terhadap Penggunaan Sepeda")

# Scatter plot untuk suhu dan kelembaban terhadap jumlah pengguna
fig, ax = plt.subplots(1, 2, figsize=(14, 6))

# Plot 1: Suhu vs Total Pengguna
sns.scatterplot(x='suhu', y='total_pengguna', data=day_df, ax=ax[0], hue='kondisi_cuaca', palette='viridis')
ax[0].set_title('Pengaruh Suhu terhadap Jumlah Pengguna Sepeda')
ax[0].set_xlabel('Suhu')
ax[0].set_ylabel('Jumlah Pengguna')

# Plot 2: Kelembaban vs Total Pengguna
sns.scatterplot(x='kelembaban', y='total_pengguna', data=day_df, ax=ax[1], hue='kondisi_cuaca', palette='coolwarm')
ax[1].set_title('Pengaruh Kelembaban terhadap Jumlah Pengguna Sepeda')
ax[1].set_xlabel('Kelembaban')
ax[1].set_ylabel('Jumlah Pengguna')

st.pyplot(fig)

# 2. Perbandingan pengguna sepeda pada hari kerja, hari libur, dan akhir pekan (hour.csv)
st.header("Perbandingan Pengguna Sepeda: Hari Kerja vs Hari Libur/Akhir Pekan")

# Mengubah nama kolom di hour.csv
hour_df.rename(columns={
    'holiday': 'hari_libur',
    'workingday': 'hari_bekerja',
    'cnt': 'total_pengguna',
    'weekday': 'hari_kerja',
    'hr': 'jam'
}, inplace=True)

# Menambahkan kolom baru untuk kategori hari kerja, hari libur, dan akhir pekan
hour_df['kategori_hari'] = hour_df.apply(
    lambda row: 'Hari Libur' if row['hari_libur'] == 1 else 'Hari Kerja' if row['hari_bekerja'] == 1 else 'Akhir Pekan', axis=1
)

# Membuat boxplot untuk perbandingan jumlah pengguna sepeda pada hari kerja, hari libur, dan akhir pekan
fig, ax = plt.subplots(figsize=(10, 6))
sns.boxplot(x='kategori_hari', y='total_pengguna', data=hour_df, palette='Set2')
ax.set_title('Perbandingan Jumlah Pengguna Sepeda pada Hari Kerja vs Hari Libur/Akhir Pekan')
ax.set_xlabel('Kategori Hari')
ax.set_ylabel('Jumlah Pengguna')

st.pyplot(fig)
