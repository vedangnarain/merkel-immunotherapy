#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Thu Nov  2 10:04:25 2023

@author: Vedang Narain (vedang.narain@msdtc.ox.ac.uk)

Drop extreme value?

"""

# Import the required libaries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.signal import savgol_filter

# Import the infiltration dataset
infiltration_dataset = '/Users/vedang/Desktop/Moffitt/Data/Infiltration Data/P12_Infiltration_CD3+CD8+CD103+_500um_25um_All Pos Layers.xlsx'
df_1 = pd.read_excel(infiltration_dataset)

# Remove unecessary columns
keywords = ['Band area', 'count', 'Algorithm', 'interface area', 'density', 'distance', 'Count']
columns_to_drop = [col for col in df_1.columns if any(keyword in col for keyword in keywords)]
df_1 = df_1.drop(columns=columns_to_drop)
df_1 = df_1.rename(columns={'Image Tag': 'ID'})
df_1['ID'] = df_1['ID'].str.extract(r'06S(.*)')  # keep relevant part of ID

# Import the outcomes dataset
outcomes_dataset = '/Users/vedang/Desktop/Moffitt/Data/Infiltration Data/Classification-Global-03-21-2023.xlsx'
df_2 = pd.read_excel(outcomes_dataset)
df_2 = df_2.iloc[:, :5]  # retain relevant columns
df_2['ID'] = df_2['ID'].str.extract(r'06S(.*)')  # keep relevant part of ID
df_2 = df_2.dropna(subset=['ID'])  # remove irrelevant IDs
df_2 = df_2[df_2['BEST RESPONSE'] != 'NOT']  # remove failed classifications

## Merge the two dataframes where they have IDs in common
merged_df = pd.merge(df_1, df_2, on='ID', how='inner')
#merged_df = merged_df.dropna(subset=['Response'])
merged_df = merged_df.drop_duplicates()
df_NR = merged_df[merged_df['BEST RESPONSE'] == 'NR']
df_RE = merged_df[merged_df['BEST RESPONSE'] == 'RE']
#df_RE = df_RE.iloc[:-2, :]
df_RE = df_RE.drop(13)  # drop extreme value
#df_PD = merged_df[merged_df['Response'] == 'PD']
#
## Plot all the patients
#window_size =3  # Adjust this to control the level of smoothing
#poly_order = 1   # Adjust this to control the degree of the polynomial
#NR = savgol_filter(df_NR.mean(axis=0), window_size, poly_order)
#RE = savgol_filter(df_RE.mean(axis=0), window_size, poly_order)
distance = np.linspace(-480,480,25)

# Plot the average cell count
#'''
plt.figure()
plt.xlabel('distance from tumour-stroma layer (μm)')
plt.ylabel('[CD3+ CD8+ CD103+] per mm²')
#    plt.plot(-distance, dataframe.mean(axis=0))  #, label=merged_df['ID'])
plt.plot(distance, df_NR.mean(axis=0), label='NR')  #, label=merged_df['ID'])
plt.plot(distance, df_RE.mean(axis=0), label='RE')  #, label=merged_df['ID'])
#    for patient in range(0, dataframe.shape[0]):
#        infiltration_line = dataframe.iloc[patient, 1:-2]
#        smoothed_values = infiltration_line.rolling(window=window_size).mean()
#        plt.plot(distance, infiltration_line)  #, label=merged_df['ID'])
plt.xlim(-500, 500)
plt.ylim(0, 2.5)
plt.title('Average Cell Density')
plt.legend()
plt.show()
#'''

# Plot the individual patients
#'''
fig, axs = plt.subplots(2, 1, figsize=(8, 12))
dataframe = df_NR
plot_title = 'Non-responsive (n=4)'
for patient in range(0, dataframe.shape[0]):
    infiltration_line = dataframe.iloc[patient, 1:-4]
#    smoothed_values = infiltration_line.rolling(window=window_size).mean()
    axs[0].plot(distance, infiltration_line)
    axs[0].set_ylabel('[CD3+ CD8+ CD103+] per mm²')
    axs[0].set_xlabel('distance from tumour-stroma layer (μm)')
    axs[0].set_xlim(-500, 500)
#    axs[0].set_ylim(0, 15)
    axs[0].set_title(plot_title)
dataframe = df_RE
plot_title = 'Responsive (n=13)'
for patient in range(0, dataframe.shape[0]):
    infiltration_line = dataframe.iloc[patient, 1:-4]
#    smoothed_values = infiltration_line.rolling(window=window_size).mean()
    axs[1].plot(distance, infiltration_line)
    axs[1].set_ylabel('[CD3+ CD8+ CD103+] per mm²')
    axs[1].set_xlabel('distance from tumour-stroma layer (μm)')
    axs[1].set_xlim(-500, 500)
#    axs[1].set_ylim(0, 15)
    axs[1].set_title(plot_title)

plt.subplots_adjust(hspace=0.25)
#plt.legend()
plt.show()
#'''
