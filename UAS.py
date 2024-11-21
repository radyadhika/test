import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import streamlit as st

# Read CSV and JSON files
df = pd.read_csv('produksi_minyak_mentah.csv')
df_json = pd.read_json('kode_negara_lengkap.json')

# Clean and merge data
df_json.rename(columns={'alpha-3': 'kode_negara', 'country-code': 'Kode_Negara', 'sub-region': 'Sub-Region'}, inplace=True)
df_csv_clean = df[df['kode_negara'].isin(df_json['kode_negara'])].copy()
df_csv_clean = df_csv_clean.merge(df_json[['kode_negara', 'name', 'Kode_Negara', 'region', 'Sub-Region']], on='kode_negara', how='left')
df_csv_clean.rename(columns={'name': 'Nama_Negara', 'region': 'Region'}, inplace=True)

# Set up Streamlit app
st.set_page_config(layout="wide")
st.title("Informasi Seputar Data Produksi Minyak Mentah dari Berbagai Negara di Seluruh Dunia")
st.markdown("*Aplikasi ini dibuat oleh Radya Evandhika Novaldi/12220135/Teknik Perminyakan/Institut Teknologi Bandung*")

# Sidebar configuration
st.sidebar.title("Pengaturan")
st.sidebar.subheader("Konfigurasi Grafik")
width = st.sidebar.slider("Lebar Grafik", 1, 25, 16)
height = st.sidebar.slider("Tinggi Grafik", 1, 25, 5)

# Display raw data table
col1a, col1b = st.columns(2)
col1a.subheader("Tabel Representasi Data Mentah")
n_tampil = col1b.number_input("Jumlah Baris dalam Tabel yang Ingin Ditampilkan", min_value=1, value=10)
S = col1b.selectbox("Filter", df_csv_clean.columns.tolist())
col1a.dataframe(df_csv_clean.sort_values(by=S, ascending=False).head(n_tampil))

# Information about oil production in a selected country
st.subheader("Informasi Produksi Minyak pada Suatu Negara")
N = st.selectbox("Pilih Negara", df_json['name'].unique())
selected_country_info = df_json[df_json['name'] == N].iloc[0]
kodenegarahuruf = selected_country_info['kode_negara']
country_data = df_csv_clean[df_csv_clean['kode_negara'] == kodenegarahuruf]

# Plot production over the years for the selected country
fig, ax = plt.subplots(figsize=(width, height))
ax.plot(country_data['tahun'], country_data['produksi'], label=N)
ax.set_title(f'Grafik Produksi Negara {N}', fontsize=14)
ax.set_xlabel('Tahun', fontsize=12)
ax.set_ylabel('Produksi', fontsize=12)
ax.grid(axis='y')
ax.legend()
st.pyplot(fig)

# Information about countries with the highest production in a selected year
st.subheader("Informasi Jumlah Produksi Minyak Terbesar pada Tahun Tertentu")
T = st.number_input("Pilih Tahun", min_value=int(df_csv_clean['tahun'].min()), max_value=int(df_csv_clean['tahun'].max()), value=1990)
B1 = st.number_input("Pilih Banyaknya Negara", min_value=1, value=10)
dftahun = df_csv_clean[df_csv_clean['tahun'] == T].sort_values(by='produksi', ascending=False).head(B1)

# Plot top countries in the selected year
fig, ax = plt.subplots(figsize=(width, height))
ax.bar(dftahun['Nama_Negara'], dftahun['produksi'])
ax.set_title(f'Grafik {B1} Negara Produksi Terbesar pada Tahun {T}', fontsize=13)
ax.set_xlabel('Negara', fontsize=12)
plt.xticks(rotation=90)
ax.set_ylabel('Produksi', fontsize=12)
ax.grid(axis='y')
st.pyplot(fig)

# Cumulative production information
st.subheader("Informasi Produksi Minyak Terbesar Secara Kumulatif Keseluruhan Tahun")
B2 = st.number_input("Banyak Negara", min_value=1, value=10, key='B2')
df_cumulative = df_csv_clean.groupby(['kode_negara', 'Nama_Negara', 'Kode_Negara', 'Region', 'Sub-Region'], as_index=False)['produksi'].sum()
df_cumulative.rename(columns={'produksi': 'produksi_kumulatif'}, inplace=True)
df_cumulative = df_cumulative.sort_values(by='produksi_kumulatif', ascending=False).head(B2)

# Plot cumulative production
fig, ax = plt.subplots(figsize=(width, height))
ax.bar(df_cumulative['Nama_Negara'], df_cumulative['produksi_kumulatif'])
ax.set_title(f'Grafik {B2} Negara Produksi Kumulatif Terbesar', fontsize=13)
ax.set_xlabel('Negara', fontsize=12)
plt.xticks(rotation=90)
ax.set_ylabel('Produksi', fontsize=12)
ax.grid(axis='y')
st.pyplot(fig)

# Summary information
st.write("\n")
col5a, col5b = st.columns(2)

# Cumulative summary
col5a.subheader("Summary Kumulatif")
df_cumulative_nonzero = df_cumulative[df_cumulative['produksi_kumulatif'] > 0]
if not df_cumulative_nonzero.empty:
    max_cumulative = df_cumulative_nonzero.iloc[0]
    min_cumulative = df_cumulative_nonzero.iloc[-1]
    col5a.markdown("**Negara dengan Produksi Kumulatif Terbesar:**")
    col5a.markdown(f"Nama Negara: {max_cumulative['Nama_Negara']}")
    col5a.markdown(f"Kode Negara: {max_cumulative['kode_negara']}")
    col5a.markdown(f"Region: {max_cumulative['Region']}")
    col5a.markdown(f"Sub-region: {max_cumulative['Sub-Region']}")
    col5a.markdown(f"Produksi Kumulatif: {max_cumulative['produksi_kumulatif']} TMT")

    col5a.markdown("\n**Negara dengan Produksi Kumulatif Terkecil (lebih dari nol):**")
    col5a.markdown(f"Nama Negara: {min_cumulative['Nama_Negara']}")
    col5a.markdown(f"Kode Negara: {min_cumulative['kode_negara']}")
    col5a.markdown(f"Region: {min_cumulative['Region']}")
    col5a.markdown(f"Sub-region: {min_cumulative['Sub-Region']}")
    col5a.markdown(f"Produksi Kumulatif: {min_cumulative['produksi_kumulatif']} TMT")
else:
    col5a.markdown("Tidak ada negara dengan produksi kumulatif lebih dari nol.")

col5a.markdown("\n**Negara dengan Produksi Kumulatif Sama Dengan Nol:**")
df_cumulative_zero = df_cumulative[df_cumulative['produksi_kumulatif'] == 0]
col5a.dataframe(df_cumulative_zero[['Nama_Negara', 'kode_negara', 'Region', 'Sub-Region', 'produksi_kumulatif']])

# Summary for a selected year
col5b.subheader("Summary Tahun Tertentu")
T2 = col5b.number_input("Tahun Berapa", min_value=int(df_csv_clean['tahun'].min()), max_value=int(df_csv_clean['tahun'].max()), value=1990, key='T2')
dftahun2 = df_csv_clean[df_csv_clean['tahun'] == T2]
dftahun2_nonzero = dftahun2[dftahun2['produksi'] > 0].sort_values(by='produksi', ascending=False)

if not dftahun2_nonzero.empty:
    max_prod_year = dftahun2_nonzero.iloc[0]
    min_prod_year = dftahun2_nonzero.iloc[-1]
    col5b.markdown(f"**Negara dengan Produksi Minyak Terbesar pada Tahun {T2}:**")
    col5b.markdown(f"Nama Negara: {max_prod_year['Nama_Negara']}")
    col5b.markdown(f"Kode Negara: {max_prod_year['kode_negara']}")
    col5b.markdown(f"Region: {max_prod_year['Region']}")
    col5b.markdown(f"Sub-Region: {max_prod_year['Sub-Region']}")
    col5b.markdown(f"Produksi: {max_prod_year['produksi']} TMT")

    col5b.markdown(f"\n**Negara dengan Produksi Minyak Terkecil (lebih dari nol) pada Tahun {T2}:**")
    col5b.markdown(f"Nama Negara: {min_prod_year['Nama_Negara']}")
    col5b.markdown(f"Kode Negara: {min_prod_year['kode_negara']}")
    col5b.markdown(f"Region: {min_prod_year['Region']}")
    col5b.markdown(f"Sub-Region: {min_prod_year['Sub-Region']}")
    col5b.markdown(f"Produksi: {min_prod_year['produksi']} TMT")
else:
    col5b.markdown(f"Tidak ada negara dengan produksi lebih dari nol pada tahun {T2}.")

col5b.markdown(f"\n**Negara dengan Produksi Minyak Sama Dengan Nol pada Tahun {T2}:**")
dftahun2_zero = dftahun2[dftahun2['produksi'] == 0]
col5b.dataframe(dftahun2_zero[['Nama_Negara', 'kode_negara', 'Region', 'Sub-Region', 'produksi']])
