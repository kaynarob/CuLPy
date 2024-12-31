# This file is part of CuLPy
# This program is free software distributed under the MIT License 
# A copy of the MIT License can be found at 
# https://github.com/kaynarob/CuLPy/blob/main/LICENSE.md

import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.patches import Patch
import matplotlib.lines as mlines
import os
import calendar

############################# INPUTS ##########################################

# Define path of the directory of your data
data_path = r'C:\Ecoological_Informatics_uncertainty'

# Define file names of CSV files
file_paths = {
    "Posterior": os.path.join(data_path,"culpy.2.obs.csv"),
    "Prior": os.path.join(data_path,"culpy.0.obs.csv"),
    "MeasurementNoise": os.path.join(data_path,"culpy.obs+noise.csv"),
    "Measurements": os.path.join(data_path,"observation.csv")
}

# Define threshold values for each variable (use None for no threshold)
variable_thresholds = {
    "nh4": 100,
    "po4": 100,
    "no3": 100,
}

# Define file-specific threshold application
threshold_application = {
    "Prior": True,              # Apply thresholds to Prior
    "Posterior": False,         # Do not apply thresholds to Posterior
    "MeasurementNoise": False   # Do not apply thresholds to Measurement Noise
}

# Define a flag to delete the whole row if any value in it exceeds the threshold
#    if false - replace individual values exceeding the threshold with None
delete_row_if_exceeds = False

# Define flag to convert all values below zero to NaN
drop_zero = False
# Define a flag to convert all values below zero to zero
convert_negatives_to_zero = False

# Define legend positions for each variable
legend_positions = {
    "nh4": "upper right",  # Legend for nh4 will be in the top left
    "po4": "upper left", # Legend for po4 will be in the top right
    "no3": "upper right",  # Adjust as needed for other variables
}


ymin_lim = {
    "nh4": -0,
    "po4": -0,
    "no3": -0,
}

output_fig_path = r'C:\Ecoological_Informatics_uncertainty'

###############################################################################

# Read "Measurements" file separately (keep the first column)
measurements_df = pd.read_csv(file_paths["Measurements"])

# Read other files, discarding the first column
data_frames = {
    name: pd.read_csv(path).iloc[:, 1:]
    for name, path in file_paths.items()
    if name != "Measurements"
}

# Add the measurements DataFrame back into the dictionary
data_frames["Measurements"] = measurements_df

# Drop all values below zero in the DataFrames
if drop_zero:
    for file_name, df in data_frames.items():
        data_frames[file_name] = df.applymap(lambda x: x if x >= 0 else None)
       
if convert_negatives_to_zero:
    for file_name, df in data_frames.items():
        data_frames[file_name] = df.applymap(lambda x: max(x, 0) if pd.notnull(x) else x)

# Track dropped rows for each file
rows_dropped = {}

# Drop rows where any value exceeds the threshold for all variables (excepth measurement data)
for file_name, df in data_frames.items():
   
    if file_name == "Measurements":
        # No threshold filtering for measurements
        rows_dropped[file_name] = 0
        continue
   
    # Keep track of the original number of rows
    original_row_count = len(df)
   
    # Build a boolean mask for rows to drop
    rows_to_drop = pd.Series([False] * len(df), index=df.index)

    for variable, threshold in variable_thresholds.items():
        if threshold is not None:  # Apply filtering only if a threshold is set
            # Identify columns for the specific variable
            variable_columns = [col for col in df.columns if col.startswith(variable)]
            # Find rows where any value in these columns exceeds the threshold
            rows_to_drop |= df[variable_columns].gt(threshold).any(axis=1)

    # Drop the rows where any threshold condition is met
    data_frames[file_name] = df.drop(rows_to_drop[rows_to_drop].index)
   
    # Calculate and store the number of rows dropped
    rows_dropped[file_name] = original_row_count - len(data_frames[file_name])

# Print summary of dropped rows
for file_name, count in rows_dropped.items():
    print(f"File: {file_name}, Rows dropped: {count}")

# Extract unique variable names
def extract_variable_names(df):
    return sorted(set(col.split('_')[0] for col in df.columns))

variables = extract_variable_names(next(iter(data_frames.values())))
if 'dox' in variables:
    variables.remove('dox')
   
   
# Process measurements data
# We assume it has a "Date" column and uppercase variable names (NH4, PO4, NO3).
measurements_df = data_frames["Measurements"]
measurements_df["Date"] = pd.to_datetime(measurements_df["Date"], format="%m/%d/%Y")
measurements_df["Month"] = measurements_df["Date"].dt.month.astype(str)
measurements_df["Day"] = measurements_df["Date"].dt.day.astype(str)

# Build a dictionary: measurement_dict[variable][(month,day)] = measurement_value
measurement_dict = {}
for var in ["NH4", "PO4", "NO3"]:
    var_lower = var.lower()
    if var in measurements_df.columns:
        measurement_dict[var_lower] = {
            (m, d): v for m, d, v in zip(
                measurements_df["Month"],
                measurements_df["Day"],
                measurements_df[var]
            ) if pd.notna(v)
        }

# Build measurement_dict with zero-padded month and day for ALL variables
measurement_dict = {}
for var in ["NH4", "PO4", "NO3"]:
    var_lower = var.lower()
    if var in measurements_df.columns:
        measurement_dict[var_lower] = {
            (f"{int(m):02d}", f"{int(d):02d}"): v
            for m, d, v in zip(
                measurements_df["Month"],
                measurements_df["Day"],
                measurements_df[var]
            ) if pd.notna(v)
        }


# Define colors for the files
file_order = ["Prior", "Posterior", "MeasurementNoise"]  # Enforced order
colors = ['#66C5CC', 'blue', 'red']  # Colors corresponding to the files
legend_labels = ["Prior", "Posterior", "Measurement+Noise"]  # Updated label for MeasurementNoise
legend_patches = [Patch(color=colors[i], label=legend_labels[i]) for i in range(len(file_order))]

# Add a legend entry for measurements
measurement_line = mlines.Line2D([], [], color='red', marker='x', linestyle='None', label='Measurement')


# Create a figure and subplots for all variables, approximately A5 but wider
fig, axes = plt.subplots(nrows=len(variables), ncols=1, figsize=(12, 8.27), sharex=True)
if len(variables) == 1:
    axes = [axes]

for i, variable in enumerate(variables):
    ax = axes[i]

    variable_df = pd.DataFrame()
    all_columns = []
    for file_name in file_order:
        df = data_frames[file_name]
        filtered_cols = [col for col in df.columns if col.startswith(variable)]
        renamed_cols = {col: f"{col}_{file_name}" for col in filtered_cols}
        temp_df = df[filtered_cols].rename(columns=renamed_cols)
        all_columns.extend(temp_df.columns)
        variable_df = pd.concat([variable_df, temp_df], axis=1)
   
    variable_df = variable_df[
        sorted(
            all_columns,
            key=lambda x: (
                x.split('_')[1],  # Month
                x.split('_')[2],  # Day
                file_order.index(x.split('_')[-1])  # File order
            )
        )
    ]
   
    month_day_list = sorted(set(
        (col.split('_')[1], col.split('_')[2]) for col in variable_df.columns
    ), key=lambda x: (x[0], x[1]))
   
    cluster_width = len(file_order) + 1
    labels = []
    for idx, (month, day) in enumerate(month_day_list):
        # Plot the boxplots
        for file_idx, file_name in enumerate(file_order):
            col_name = f"{variable}_{month}_{day}_15_{file_name}"
            if col_name in variable_df.columns:
                data = variable_df[col_name].dropna().values
                if len(data) > 0:
                    pos = idx * cluster_width + file_idx
                    ax.boxplot(
                        data,
                        showfliers=False,
                        positions=[pos],
                        widths=0.8,
                        patch_artist=True,
                        boxprops=dict(facecolor=colors[file_idx]),
                        medianprops=dict(color='black'),
                        flierprops=dict(marker='o', markersize=4, linestyle='none', markeredgecolor='#7e7e7e', markeredgewidth = 0.5)
                    )
                   
        # Check if there's a measurement for this variable, month, and day
        meas_var_dict = measurement_dict.get(variable, {})
        if (month, day) in meas_var_dict:
            val = meas_var_dict[(month, day)]
            x_pos = idx * cluster_width + (len(file_order) - 2)
            ax.plot(x_pos, val, marker='o', color='red', markersize=4)
       
        month_name = calendar.month_abbr[int(month)]
        labels.append(f"{month_name} {day}")
   
    ax.set_xticks([idx * cluster_width + (len(file_order) - 1) / 2 for idx in range(len(month_day_list))])
    ax.set_xticklabels(labels, rotation=0)
   
    #ax.set_ylabel(f"$\\mathrm{{{variable[:-1].upper()}}}_{{\\mathrm{{{variable[-1]}}}}}$")
    
    if variable == "nh4":
        variable_name = '$NH_4^+ (mgL^{-1})$'
    elif variable == "no3":
        variable_name = '$NO_3^- (mgL^{-1})$'
    elif variable == "po4":
        variable_name = '$PO_4^{3-} (mgL^{-1})$'
    elif variable == "o2":
        variable_name = '$O_2$'
    
    ax.set_ylabel(f'{variable_name}\n')
        
   
    y_min = ymin_lim.get(variable, None)
    if y_min is not None:
        ax.set_ylim(bottom=y_min)

ax.set_xlabel("Date")

# Create a single legend at the bottom center of the figure, including measurements
fig.legend(
    handles=legend_patches,
    loc='upper right',
    bbox_to_anchor=(0.99, 0.987),
    ncol=len(legend_patches) + 1,
    fontsize=12
)

fig.tight_layout()

output_path = os.path.join(output_fig_path, "all_variables.png")
plt.savefig(output_path, dpi=300, bbox_inches="tight")
plt.show()