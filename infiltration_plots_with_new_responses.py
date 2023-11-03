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
merged_df = merged_df.drop(13)  # drop extreme value
df_NR = merged_df[merged_df['BEST RESPONSE'] == 'NR']
df_RE = merged_df[merged_df['BEST RESPONSE'] == 'RE']
#df_RE = df_RE.iloc[:-2, :]
#df_PD = merged_df[merged_df['Response'] == 'PD']
#
## Plot all the patients
#window_size =3  # Adjust this to control the level of smoothing
#poly_order = 1   # Adjust this to control the degree of the polynomial
#NR = savgol_filter(df_NR.mean(axis=0), window_size, poly_order)
#RE = savgol_filter(df_RE.mean(axis=0), window_size, poly_order)
distance = np.linspace(-480,480,25)
width = 3
orange = '#ff914d'
line_styles = ['-', '--', '-.', ':', '-', '--', '-.', ':', '-', '--', '-.', ':', '-', '--', '-.', ':', '-', '--']
threshold = 2  # Adjust this threshold as needed
# Apply condition and keep only rows where all values are below the threshold
df_RE_big = df_RE[df_RE.max(axis=1) >= threshold]
df_RE_small = df_RE[df_RE.max(axis=1) <= threshold]

# Plot the average cell count for three groups
'''
plt.figure()
plt.xlabel('distance from tumour-stroma layer (μm)')
plt.ylabel('[CD3+ CD8+ CD103+] per mm²')
#    plt.plot(-distance, dataframe.mean(axis=0))  #, label=merged_df['ID'])
plt.plot(distance, df_NR.mean(axis=0), label='NR (n=' + str(df_NR.shape[0]) + ')', lw=width, ls = line_styles[0])  #, label=merged_df['ID'])
plt.plot(distance, df_RE_big.mean(axis=0), label='RE big (n=' + str(df_RE_big.shape[0]) + ')', lw=width, ls = line_styles[1])  #, label=merged_df['ID'])
plt.plot(distance, df_RE_small.mean(axis=0), label='RE small (n=' + str(df_RE_small.shape[0]) + ')', lw=width, ls = line_styles[2])  #, label=merged_df['ID'])
#    for patient in range(0, dataframe.shape[0]):
#        infiltration_line = dataframe.iloc[patient, 1:-2]
#        smoothed_values = infiltration_line.rolling(window=window_size).mean()
#        plt.plot(distance, infiltration_line)  #, label=merged_df['ID'])
plt.xlim(-500, 500)
plt.ylim(0, 5)
plt.title('Average Cell Density')
plt.legend()
plt.grid(True)
plt.show()
'''

# Plot the average cell count for three groups
'''
plt.figure()
plt.ylabel('[CD3+ CD8+ CD103+] per mm²')
dataframe = df_NR
dataframe_values = dataframe.iloc[:, 1:-4]
dataframe_values = dataframe_values.sum(axis=1)
plt.bar(range(len(dataframe_values)), dataframe_values, color='r')
tally = len(dataframe_values)
#dataframe_categories = dataframe['BEST RESPONSE']
dataframe = df_RE_big
dataframe_values = dataframe.iloc[:, 1:-4]
dataframe_values = dataframe_values.sum(axis=1)
plt.bar(range(tally, len(dataframe_values)+tally), dataframe_values, color='g')
tally = tally+len(dataframe_values)
dataframe = df_RE_small
dataframe_values = dataframe.iloc[:, 1:-4]
dataframe_values = dataframe_values.sum(axis=1)
plt.bar(range(tally, len(dataframe_values)+tally), dataframe_values, color='b')
plt.title('Average Cell Density')
#plt.legend()
#plt.grid(True)
#plt.xticks(range(5,9), ['NR', 'CR'], rotation=45)
plt.tight_layout()
#plt.subplots_adjust(wspace=0.5) 
plt.show()
'''

# Plot the average cell count for three groups
'''
plt.figure(figsize=(3,4))
plt.ylabel('[CD3+ CD8+ CD103+] per mm²')
dataframe = merged_df
condition_orange = dataframe['BEST RESPONSE'] == 'RE'
condition_blue = dataframe['BEST RESPONSE'] == 'NR'
dataframe_values = dataframe.iloc[:, 1:-4]
dataframe_values = dataframe_values.sum(axis=1)
dataframe_categories = dataframe['BEST RESPONSE']
dataframe_categories.replace('NR', 'non-responsive', regex=False)
plt.scatter(dataframe_categories[condition_orange], dataframe_values[condition_orange], color=orange, s=100, alpha=0.5)
plt.scatter(dataframe_categories[condition_blue], dataframe_values[condition_blue], color='C0', s=100, alpha=0.5)
#plt.scatter(dataframe_categories, dataframe_values,  marker='o', alpha=0.5, c=dataframe_values, cmap='viridis', s=100)
plt.title('Total Patient Cell Count')
#plt.legend()
#plt.grid(True)
#plt.xticks(range(5,9), ['NR', 'CR'], rotation=45)
plt.tight_layout()
#plt.subplots_adjust(wspace=0.5) 
plt.show()
'''

# Plot the average cell count
'''
plt.figure()
plt.xlabel('distance from tumour-stroma layer (μm)')
plt.ylabel('[CD3+ CD8+ CD103+] per mm²')
#    plt.plot(-distance, dataframe.mean(axis=0))  #, label=merged_df['ID'])
plt.plot(distance, df_NR.mean(axis=0), label='NR (n=' + str(df_NR.shape[0]) + ')', lw=width, ls = line_styles[0])  #, label=merged_df['ID'])
plt.plot(distance, df_RE.mean(axis=0), label='RE (n=' + str(df_RE.shape[0]) + ')', lw=width, ls = line_styles[1])  #, label=merged_df['ID'])
#    for patient in range(0, dataframe.shape[0]):
#        infiltration_line = dataframe.iloc[patient, 1:-2]
#        smoothed_values = infiltration_line.rolling(window=window_size).mean()
#        plt.plot(distance, infiltration_line)  #, label=merged_df['ID'])
plt.xlim(-500, 500)
plt.ylim(0, 3)
plt.title('Average Cell Density (n=' + str(df_NR.shape[0]+df_RE.shape[0]) + ')')
plt.legend()
plt.grid(True)
plt.show()
'''

# Plot the individual patients
#'''
fig, axs = plt.subplots(1, 2, figsize=(16, 6))
dataframe = df_NR
plot_title = 'Non-responsive (n=' + str(dataframe.shape[0]) + ')'
for patient in range(0, dataframe.shape[0]):
    infiltration_line = dataframe.iloc[patient, 1:-4]
#    smoothed_values = infiltration_line.rolling(window=window_size).mean()
    axs[0].plot(distance, infiltration_line, lw=width, ls = line_styles[patient])
    axs[0].set_ylabel('[CD3+ CD8+ CD103+] per mm²')
    axs[0].set_xlabel('distance from tumour-stroma layer (μm)')
    axs[0].set_xlim(-500, 500)
    axs[0].set_ylim(0, 12)
    axs[0].set_title(plot_title)
    axs[0].grid(True)

dataframe = df_RE
#dataframe = df_RE_small
plot_title = 'Responsive (n=' + str(dataframe.shape[0]) + ')'
for patient in range(0, dataframe.shape[0]):
    infiltration_line = dataframe.iloc[patient, 1:-4]
#    smoothed_values = infiltration_line.rolling(window=window_size).mean()
    axs[1].plot(distance, infiltration_line, lw=width, ls = line_styles[patient])
    axs[1].set_ylabel('[CD3+ CD8+ CD103+] per mm²')
    axs[1].set_xlabel('distance from tumour-stroma layer (μm)')
    axs[1].set_xlim(-500, 500)
    axs[1].set_ylim(0, 12)
    axs[1].set_title(plot_title)
    axs[1].grid(True)

plt.subplots_adjust(hspace=0.25)
#plt.legend()
plt.show()
#'''
