# -*- coding: utf-8 -*-
"""
Created on Thu Mar 21 00:53:13 2024

@author: burak 
"""
import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.dates as mdates

def read_values_file(filename):
    values = {}
    with open(filename, 'r') as file:
        for line in file:
            variable, value = line.split(': ')
            values[variable.strip()] = float(value.strip())
    return values

def plot_all_variables(df_output, df_observation, plot_start_date, plot_end_date, 
                       r2_values_calibration, pbias_values_calibration, 
                       r2_values_validation, pbias_values_validation, 
                       text_x, text_y, legend_loc, separation_start_date, calibration_on_left=True):
    
    #df_output['Cpy'] = df_output['Cpy'] / 45 * 1000
    
    # Filter datasets for the specified date range
    df_output = df_output[(df_output.index >= plot_start_date) & (df_output.index <= plot_end_date)]
    df_output = df_output.resample('D').mean()
    df_observation = df_observation[(df_observation.index >= plot_start_date) & (df_observation.index <= plot_end_date)]
    
    
    # Prepare the figure and subplots
    fig, axs = plt.subplots(3, 1, figsize=(32, 24), dpi=100, sharex=True)
    
    # Text and legend size settings
    label_fontsize = 30
    value_fontsize = 30
    tick_fontsize = 25
    legend_fontsize = 25
    
    
    # Hardcoded minimum and maximum values for each variable
    axis_limits = {
        "NH4": (-0.001, 1.3E-01),
        "NO3": (-0.001, 1.90),
        "PO4": (-0.001, 0.036)
    }
    
    graph_names = {
        "NH4": '(a)',
        "NO3": '(b)',
        "PO4": '(c)'
    }
    
    # Variables to plot
    variable_to_plot = ["NH4", "NO3", "PO4"]
    
    # Convert the separation start date to datetime
    separation_date_dt = pd.to_datetime(separation_start_date)
    
    # Define text positions and labels based on calibration_on_left flag
    if calibration_on_left:
        calibration_label_pos = 0.30  # Position for overall Calibration text
        validation_label_pos = 0.75  # Position for overall Validation text
        calibration_stats_pos = 0.25  # Position for calibration statistics
        validation_stats_pos = 0.75  # Position for validation statistics
        calibration_color = 'blue'
        validation_color = 'black'
        calibration_label = 'Calibration'
        validation_label = 'Validation'
    else:
        calibration_label_pos = 0.75
        validation_label_pos = 0.30
        calibration_stats_pos = 0.75
        validation_stats_pos = 0.25
        calibration_color = 'black'
        validation_color = 'blue'
        calibration_label = 'Validation'
        validation_label = 'Calibration'
    
    for i, variable in enumerate(variable_to_plot):
        
        axs[i].plot(df_output.index, df_output[variable], label='Simulation', linestyle='-', color='red', linewidth=4.0)
        axs[i].scatter(df_observation.index, df_observation[variable], color='black', label='Observation', linewidth=4.0)
        
        # Set y-axis limits based on hardcoded values
        if variable in axis_limits:
            axs[i].set_ylim(axis_limits[variable])
        
        if variable == "NH4":
            variable_name = '$NH_4^+ (mgL^{-1})$'
            n_calib = 12 #!!! sample_size
            n_valid = 9  #!!! sample_size
        elif variable == "NO3":
            variable_name = '$NO_3^- (mgL^{-1})$'
            n_calib = 12 #!!! sample_size
            n_valid = 9  #!!! sample_size
        elif variable == "PO4":
            variable_name = '$PO_4^{3-} (mgL^{-1})$'
            n_calib = 12 #!!! sample_size
            n_valid = 9  #!!! sample_size

        
        axs[i].set_ylabel(f'{variable_name}\n', fontsize=label_fontsize)
        
        # Draw vertical dashed line for separation between calibration and validation periods
        axs[i].axvline(separation_date_dt, color='grey', linestyle='--', linewidth=2) 

        # Annotate statistics for calibration period (left or right based on calibration_on_left)
        text_obj_calibration = (#f'      n  : {n_calib}\n'
                                f'      R² : {r2_values_calibration.get(variable, "n/a"):.2f}\n'
                                f'     RE : {re_values_calibration.get(variable, "n/a"):.2f}\n'
                                f'PBIAS : {pbias_values_calibration.get(variable, "n/a"):.1f}')
        axs[i].text(calibration_stats_pos, 0.85, text_obj_calibration, transform=axs[i].transAxes, color=calibration_color, fontsize=value_fontsize, 
                    verticalalignment='top')  # Bounded box for better readability
        
        # Annotate statistics for validation period (left or right based on calibration_on_left)
        text_obj_validation = (#f'      n  : {n_valid}\n'
                               f'      R² : {r2_values_validation.get(variable, "n/a"):.2f}\n'
                               f'     RE : {re_values_validation.get(variable, "n/a"):.2f}\n'
                               f'PBIAS : {pbias_values_validation.get(variable, "n/a"):.1f}')
        axs[i].text(validation_stats_pos, 0.85, text_obj_validation, transform=axs[i].transAxes,color=validation_color, fontsize=value_fontsize, 
                    verticalalignment='top')  # , bbox=dict(facecolor='white', alpha=0.5) Bounded box for better readability
        
        graph_name = graph_names[variable]
        axs[i].text(0.95, 0.95, graph_name, transform=axs[i].transAxes, fontsize=value_fontsize, verticalalignment='top')
        
        # Set tick parameters for both axes
        axs[i].tick_params(axis='both', labelsize=tick_fontsize)

        if i == 0:
            axs[i].legend(fontsize=legend_fontsize, loc=legend_loc)

        if i == len(variable_to_plot) - 1:
            #axs[i].xaxis.set_major_locator(mdates.MonthLocator())
            axs[i].xaxis.set_major_locator(mdates.MonthLocator(interval=2))  # Adjust the interval here if needed
            axs[i].xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
            plt.xticks(rotation=45)
    
    

    # Add "Calibration" and "Validation" texts only on top of the figure, not individual subplots
    if calibration_on_left:
        fig.text(calibration_label_pos, 1.00, calibration_label, ha='center', fontsize=35, color=calibration_color)
        fig.text(validation_label_pos, 1.00, validation_label, ha='center', fontsize=35, color=validation_color)
    else:
        fig.text(calibration_label_pos, 1.00, validation_label, ha='center', fontsize=35, color=calibration_color)
        fig.text(validation_label_pos, 1.00, calibration_label, ha='center', fontsize=35, color=validation_color)\

    plt.tight_layout()
    plt.show()




option = 1
if option == 1:
    output_file_name = "output_1.csv"
    observation_name = 'observation_2014_15'


df_output = pd.read_csv(output_file_name, parse_dates=[0], index_col=0)
df_observation = pd.read_csv(f'{observation_name}.csv', parse_dates=[0], index_col=0)


# Load the datasets
plot_start_date = "2014-04-01"
plot_end_date = "2015-12-10"

# Read the R² and RE values from files
# r2_values = read_values_file('r2_values_Dum.txt')
#re_values = read_values_file(f'outputs/re_values_{observation_name}.txt')
# pbias_values = read_values_file('pbias_values_Dum.txt')

r2_values_calibration = read_values_file('r2_values_observation.txt')
re_values_calibration = read_values_file('re_values_observation.txt')
pbias_values_calibration = read_values_file('pbias_values_observation.txt')

r2_values_validation = read_values_file('r2_values_observation_validation_2014.txt')
re_values_validation = read_values_file('re_values_observation_validation_2014.txt')
pbias_values_validation = read_values_file('pbias_values_observation_validation_2014.txt')


# Call the function with the option to specify calibration on the left or right
separation_start_date = '2015-01-01'
calibration_on_left = False  # Set to False to place calibration on the right

plot_all_variables(df_output, df_observation, plot_start_date, plot_end_date, 
                   r2_values_calibration, pbias_values_calibration, 
                   r2_values_validation, pbias_values_validation, 
                   text_x=0.50, text_y=0.95, legend_loc='upper left', 
                   separation_start_date=separation_start_date, 
                   calibration_on_left=calibration_on_left)

# Calling the function with custom text and legend positions
#plot_all_variables(df_output, df_observation, plot_start_date, plot_end_date, r2_values, re_values, pbias_values, text_x=0.50, text_y=0.95, legend_loc='upper left')
