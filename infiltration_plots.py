#!/usr/bin/env python3
# -*- coding: utf-8 -*-

"""
Created on Wed Nov  1 15:32:36 2023

@author: Vedang Narain (vedang.narain@msdtc.ox.ac.uk)

Question: Response 1 or 2? Drop extreme value?

"""

# Import the required libaries
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Import the infiltration dataset
infiltration_dataset = '/Users/vedang/Desktop/Moffitt/Data/Infiltration Data/P12_Infiltration_CD3+CD8+CD103+_500um_25um_All Pos Layers.xlsx'
df_1 = pd.read_excel(infiltration_dataset)

# Remove unecessary columns
keywords = ['Band area', 'count', 'Algorithm', 'interface area', 'density', 'distance', 'Count']
columns_to_drop = [col for col in df_1.columns if any(keyword in col for keyword in keywords)]
df_1 = df_1.drop(columns=columns_to_drop)
df_1 = df_1.rename(columns={'Image Tag': 'ID'})

# Import the outcomes dataset
outcomes_dataset = '/Users/vedang/Desktop/Moffitt/Data/Infiltration Data/mIF-MasterList-05-24-2023-clean.xlsx'
df_2 = pd.read_excel(outcomes_dataset, sheet_name='Panel 12')

# Remove unecessary columns
keywords = ['MO', 'Unnamed']
columns_to_drop = [col for col in df_2.columns if any(keyword in col for keyword in keywords)]
df_2 = df_2.drop(columns=columns_to_drop)

# Merge the two dataframes where they have IDs in common
merged_df = pd.merge(df_1, df_2, on='ID', how='inner')
merged_df = merged_df.dropna(subset=['Response'])
merged_df = merged_df.drop_duplicates()
df_CR = merged_df[merged_df['Response'] == 'CR']
df_PR = merged_df[merged_df['Response'] == 'PR']
df_PR = df_PR.iloc[:-1, :]  # drop extreme value
df_PD = merged_df[merged_df['Response'] == 'PD']

# Plot all the patients
window_size = 5  # Adjust this to control the level of smoothing
distance = np.linspace(-480,480,25)

# Plot the average cell count
#'''
plt.figure()
plt.xlabel('distance from tumour-stroma layer (μm)')
plt.ylabel('[CD3+ CD8+ CD103+] per mm²')
#    plt.plot(-distance, dataframe.mean(axis=0))  #, label=merged_df['ID'])
plt.plot(distance, df_CR.mean(axis=0), label='CR')  #, label=merged_df['ID'])
plt.plot(distance, df_PR.mean(axis=0), label='PR')  #, label=merged_df['ID'])
plt.plot(distance, df_PD.mean(axis=0), label='PD')  #, label=merged_df['ID'])
#    for patient in range(0, dataframe.shape[0]):
#        infiltration_line = dataframe.iloc[patient, 1:-2]
#        smoothed_values = infiltration_line.rolling(window=window_size).mean()
#        plt.plot(distance, infiltration_line)  #, label=merged_df['ID'])
plt.xlim(-500, 500)
plt.ylim(0, 3)
plt.title('Average Cell Density')
plt.legend()
plt.show()
#'''

# Plot the individual patients
'''
fig, axs = plt.subplots(3, 1, figsize=(8, 12))
dataframe = df_CR
plot_title = 'Complete Response (n=3)'
for patient in range(0, dataframe.shape[0]):
    infiltration_line = dataframe.iloc[patient, 1:-2]
    smoothed_values = infiltration_line.rolling(window=window_size).mean()
    axs[0].plot(distance, infiltration_line)
    axs[0].set_ylabel('[CD3+ CD8+ CD103+] per mm²')
    axs[0].set_xlabel('distance from tumour-stroma layer (μm)')
    axs[0].set_xlim(-500, 500)
    axs[0].set_ylim(0, 15)
    axs[0].set_title(plot_title)

dataframe = df_PR
plot_title = 'Partial Response (n=12)'
for patient in range(0, dataframe.shape[0]):
    infiltration_line = dataframe.iloc[patient, 1:-2]
    smoothed_values = infiltration_line.rolling(window=window_size).mean()
    axs[1].plot(distance, infiltration_line)
    axs[1].set_ylabel('[CD3+ CD8+ CD103+] per mm²')
    axs[1].set_xlabel('distance from tumour-stroma layer (μm)')
    axs[1].set_xlim(-500, 500)
    axs[1].set_ylim(0, 15)
    axs[1].set_title(plot_title)
 
dataframe = df_PD
plot_title = 'Disease Progression (n=5)'
for patient in range(0, dataframe.shape[0]):
    infiltration_line = dataframe.iloc[patient, 1:-2]
    smoothed_values = infiltration_line.rolling(window=window_size).mean()
    axs[2].plot(distance, infiltration_line)
    axs[2].set_ylabel('[CD3+ CD8+ CD103+] per mm²')
    axs[2].set_xlabel('distance from tumour-stroma layer (μm)')
    axs[2].set_xlim(-500, 500)
    axs[2].set_ylim(0, 15)
    axs[2].set_title(plot_title)

plt.subplots_adjust(hspace=0.5)
#plt.legend()
plt.show()
'''

# Extra code
'''
def plot_infiltrations(dataframe, plot_title, row):
#    plt.figure()
    plt.xlabel('distance from tumour-stroma layer (μm)')
    plt.ylabel('[CD3+ CD8+ CD103+] per mm²')
#    plt.plot(-distance, dataframe.mean(axis=0))  #, label=merged_df['ID'])
#    plt.plot(distance, dataframe.mean(axis=0))  #, label=merged_df['ID'])
    for patient in range(0, dataframe.shape[0]):
        infiltration_line = dataframe.iloc[patient, 1:-2]
        smoothed_values = infiltration_line.rolling(window=window_size).mean()
        axs[row].plot(distance, infiltration_line)  #, label=merged_df['ID'])
#    plt.ylim(0,10)
    plt.xlim(-500, 500)
    plt.title(plot_title)
    #plt.legend()
    plt.show()

# Plot values
    
plot_infiltrations(df_CR, 'Complete Response (n=3)',0)
plot_infiltrations(df_PR, 'Partial Response (n=12)',1)
plot_infiltrations(df_PD, 'Disease Progression (n=5)',2)
#'''
