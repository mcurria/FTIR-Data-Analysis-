# FTIR Data Analysis

This repository contains a Python script for analyzing in situ FTIR data (in .csv format as exported with TimeBase) with customizable plotting options. The script allows users to process FTIR data, integrate signals over specified wavenumber ranges, and plot the results against time or temperature profiles.

## Features

- **Transmittance and Absorbance Conversion**: The script can handle data in both transmittance and absorbance formats.
- **Customizable Temperature Profiles**: Users can input complex temperature profiles with isotherms and ramps.
- **Flexible Plotting**: Plot data against time (in seconds or minutes) or temperature, with customizable axes limits.

## Installation

Clone the repository and install the required packages:

```bash
git clone https://github.com/yourusername/FTIR-Data-Analysis.git
cd FTIR-Data-Analysis
pip install -r requirements.txt

## Usage
## Example Code

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

from FTIR_analysis import plot_integrated_signal

# Define the sample_dict with label, wavenumber range, and color for each sample
sample_dict = {
    'CO2': ('CO2 Signal', (2400, 2240), 'blue'),
    'H2O': ('H2O Signal', (2150, 1200), 'green')
}

# Load example data
file_path = 'example_data/Port_CarbC_v1.csv'
df = pd.read_csv(file_path, skiprows=4)

# Plot the data
plot_integrated_signal(df, sample_dict, 
                       input_format='Transmittance', 
                       output_format='Absorbance', 
                       x_input='seconds', 
                       x_output='temperature',
                       temp_profile=[(30, 5), (30, 100, 10), (100, 10)],
                       xlim=[0,800], 
                       ylim=[0,15])
## Parameters
input_format: 'Transmittance' or 'Absorbance'.
output_format: 'Transmittance' or 'Absorbance'.
x_input: 'seconds' or 'minutes'.
x_output: 'time' or 'temperature'.
temp_profile: A list defining the temperature profile, consisting of tuples representing isotherms or ramps.
Example Temperature Profile
Isotherm: (temperature, duration), e.g., (30, 5) for 30°C held for 5 minutes.
Ramp: (start_temperature, end_temperature, ramp_rate), e.g., (30, 100, 10) for a ramp from 30°C to 100°C at 10°C/min.

Contributing
Contributions are welcome! Please fork the repository and submit a pull request.
