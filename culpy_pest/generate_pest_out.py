# This file is part of CuLPy
# This program is free software distributed under the MIT License 
# A copy of the MIT License can be found at 
# https://github.com/kaynarob/CuLPy/blob/main/LICENSE.md

# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 00:53:13 2024

@author: burak
"""

import pandas as pd
import numpy as np
import scipy

def relative_error(y_true, y_pred):
    return np.sum(np.abs(y_true - y_pred) / np.sum(y_true))


def r2_score(y_true, y_pred):
    slope, intercept, r_value, p_value, std_err = scipy.stats.linregress(y_true, y_pred)
    return r_value**2

def pbias(y_true, y_pred):
    return (np.sum(y_true - y_pred)/np.sum(y_true))*100

def write_out():
    # Load the data
    simulation_df = pd.read_csv('output_1.csv')
    observation_df = pd.read_csv('observation.csv')

    # Correct the 'date' column format for both dataframes
    simulation_df['Date'] = pd.to_datetime(simulation_df['Date'], format='mixed')
    observation_df['Date'] = pd.to_datetime(observation_df['Date'], format='%m/%d/%Y')

    # Resample the simulation output to daily frequency
    simulation_daily_df = simulation_df.set_index('Date').resample('D').mean().reset_index()

    # Align the simulation output with the observation data
    aligned_df = pd.merge(simulation_daily_df, observation_df, on='Date', suffixes=('_sim', '_obs'))

    # Calculate R2 and RE for each column
    r2_values = {}
    re_values = {}
    pbias_values = {}
    
    # Write outputs to text files
    with open('pest.out', 'w') as file:
        columns = ['NH4', 'NO3', 'PO4']
        for column in columns:
            sim_column = column + '_sim'
            obs_column = column + '_obs'
            # Ensure no NaN values before calculation
            valid_idx = ~aligned_df[[sim_column, obs_column]].isnull().any(axis=1)
            r2_values[column] = r2_score(aligned_df.loc[valid_idx, obs_column], aligned_df.loc[valid_idx, sim_column])
            re_values[column] = relative_error(aligned_df.loc[valid_idx, obs_column], aligned_df.loc[valid_idx, sim_column])
            pbias_values[column] = pbias(aligned_df.loc[valid_idx, obs_column], aligned_df.loc[valid_idx, sim_column])
            
            out_array = aligned_df.loc[valid_idx, sim_column]
            for i in range(len(out_array)):
                value = out_array[i]
                # name = out_array.name
                # file.write(f'{name}: {value}\n')
                file.write(f'{value}\n')
    
    # Write outputs to text files
    with open('r2_values.txt', 'w') as file:
        for column, value in r2_values.items():
            #file.write(f'{column}: {value}\n')
            file.write(f'{column}: {value}\n')

    with open('re_values.txt', 'w') as file:
        for column, value in re_values.items():
            file.write(f'{column}: {value}\n')
            # file.write(f'{value}\n')

    with open('pbias_values.txt', 'w') as file:
        for column, value in pbias_values.items():
            file.write(f'{column}: {value}\n')
            # file.write(f'{value}\n')
