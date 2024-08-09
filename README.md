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
