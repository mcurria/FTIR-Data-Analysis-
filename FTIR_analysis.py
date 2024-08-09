import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# Load the CSV file, skipping the first 4 rows and then manually processing the header rows
file_path = r'C:\Users\mcurria\OneDrive - Princeton University\Documents\R_Research\E_MyExperiments\T_TGA_FTIR\Princeton\2020\Port_carbC\Port_CarbC_v1.csv'
raw_data = pd.read_csv(file_path, skiprows=4)

# Extract the times from the 5th row (index 0 after skip)
times = raw_data.columns[1:].astype(float)

# Extract the wavenumber data and intensity data starting from row 7
wavenumbers = raw_data.iloc[1:, 0].astype(float)
intensity_data = raw_data.iloc[1:, 1:].astype(float)

# Create a DataFrame where the index is wavenumber and columns are times
df = pd.DataFrame(intensity_data.values, index=wavenumbers, columns=times)

# Transpose the DataFrame to have times as the index and wavenumbers as columns
df = df.transpose()

# Function to convert between transmittance and absorbance
def convert_signal(df, input_format, output_format):
    if input_format == output_format:
        return df
    elif input_format == 'Transmittance' and output_format == 'Absorbance':
        return 100 - df
    elif input_format == 'Absorbance' and output_format == 'Transmittance':
        return 100 - df
    else:
        raise ValueError("Invalid input/output format combination.")

# Function to integrate signal over a given range of wavenumbers and normalize by the number of points
def integrate_and_normalize_signal(df, wavenumber_range):
    integrated_signal = df.loc[:, wavenumber_range[0]:wavenumber_range[1]].sum(axis=1)
    num_points = df.loc[:, wavenumber_range[0]:wavenumber_range[1]].shape[1]
    normalized_signal = integrated_signal / num_points
    return normalized_signal

# Revised function to calculate temperature profile based on isotherms and ramps
def calculate_temperature_profile(time_min, temp_profile):
    total_duration = sum(segment[1] if len(segment) == 2 else abs(segment[1] - segment[0]) / segment[2] for segment in temp_profile)
    
    temperatures = []
    current_time = 0
    
    for segment in temp_profile:
        if len(segment) == 2:  # Isotherm (temperature, duration)
            temp, duration = segment
            segment_time_fraction = duration / total_duration
            segment_length = int(segment_time_fraction * len(time_min))
            temps = np.full(segment_length, temp)
            temperatures.extend(temps)
        elif len(segment) == 3:  # Ramp (start_temp, end_temp, ramp_rate)
            start_temp, end_temp, ramp_rate = segment
            duration = abs(end_temp - start_temp) / ramp_rate
            segment_time_fraction = duration / total_duration
            segment_length = int(segment_time_fraction * len(time_min))
            temps = np.linspace(start_temp, end_temp, segment_length)
            temperatures.extend(temps)
        else:
            raise ValueError("Invalid segment in temp_profile.")
    
    # Ensure the temperature profile matches the length of time_min
    if len(temperatures) < len(time_min):
        # If too short, extend the last temperature value to match the length
        temperatures.extend([temperatures[-1]] * (len(time_min) - len(temperatures)))
    elif len(temperatures) > len(time_min):
        # If too long, truncate the profile to match the length
        temperatures = temperatures[:len(time_min)]
    
    return np.array(temperatures)

# Function to plot the integrated signal with options for input and output formats and customizations
def plot_integrated_signal(df, sample_dict, input_format='Transmittance', output_format='Absorbance', x_input='seconds', x_output='centigrades', temp_profile=None, xlim=[4000,550], ylim=[0,10]):
    df_converted = convert_signal(df, input_format, output_format)
    
    if x_input =='seconds':
        time_min = df.index / 60
    elif x_input == 'minutes':
        time_min = df.index
    
    # Determine x-axis values based on input and output settings
    if x_output == 'time':
        x_label = 'Time (minutes)'
        x_values = time_min
    elif x_output == 'temperature' and temp_profile is not None:
        x_values = calculate_temperature_profile(time_min, temp_profile)
        x_label = 'Temperature (°C)'
    else:
        raise ValueError("Invalid x_output value or missing temp_profile for temperature conversion.")
    
    plt.figure(figsize=(14, 8))
    
    for sample, (label, wavenumber_range, color) in sample_dict.items():
        # Integrate and normalize signal for each sample
        signal = integrate_and_normalize_signal(df_converted, wavenumber_range)
        
        # Calculate baseline as a straight line between the first and last points
        baseline = np.linspace(signal.iloc[0], signal.iloc[-1], len(signal))
        
        # Plot the integrated and normalized signals and their baselines
        plt.plot(x_values, signal, label=f'{label} ({output_format})', color=color)
        plt.plot(x_values, baseline, '--', color=color, alpha=0.7)
    
    # Set plot limits and labels
    plt.xlim(xlim)
    plt.ylim(ylim)
    plt.xlabel(x_label)
    plt.ylabel(f'Normalized Integrated Signal ({output_format})')
    plt.title(f'In situ FTIR Analysis: Integrated Signals Over {x_label} ({output_format})')
    
    # Customize plot appearance
    plt.legend()
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.grid(False)
    plt.show()

