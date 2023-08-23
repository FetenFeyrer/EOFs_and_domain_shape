
# README for EOF Analysis Repository

## Overview

This repository contains code for computing and visualizing Empirical Orthogonal Functions (EOFs) of various datasets. The datasets include artificial flow patterns, sea surface temperature (SST) data, and correlated noise on isotropic random fields.

## Repository Structure

1. **flowPatterns.py**: Contains functions for plotting isolines and adding Gaussian noise to data. 
2. **sst.py**: Focuses on handling and processing SST data. The data is subset into various regions of the Pacific for analysis.
3. **ComputeEOFs.py**: Provides a class for computing EOFs using the `xeofs` package.
4. **MIGRF.py**: Generates and analyzes datasets with correlated and uncorrelated noise. For each dataset, EOFs are computed and visualized.
5. **Data.py**: Contains a class for creating a time series dataset with correlated noise on an isotropic random field using the climnet package.
6. **main.py**: A driver script that runs `flowPatterns.py`, `sst.py`, and `MIGRF.py` in sequence, serving as a starting point to execute the entire EOF analysis workflow.

## Getting Started

### Prerequisites

- Ensure you have Python 3.x installed.
- Install the required libraries:
  - `matplotlib`
  - `numpy`
  - `xarray`
  - `xeofs`
  - `cartopy`
  - `climnet` (may require additional setup)
  - `sklearn`

### Running the Code

1. Clone the repository to your local machine.
2. Navigate to the repository's directory in your terminal.
3. Run `main.py` to execute the entire workflow:
   ```
   python main.py
   ```

## Modifying the Code

- **Changing Data Regions in `sst.py`**: Modify the `lat_range` and `lon_range` variables to change the latitude and longitude range of the Pacific regions.
  
- **Adjusting Noise in `flowPatterns.py`**: To adjust the noise level, modify the `mean` and `std_dev` parameters in the `add_gaussian_noise()` function.

- **Analyzing Different Datasets in `MIGRF.py`**: Adjust parameters like `l` (length scale) and `v` (variance) in the `create_correlated_noise_data()` method for varying noise characteristics.

- **Computing Rotated EOFs in `ComputeEOFs.py`**: Set the `rotate` parameter to `True` in the `compute_eofs()` method to compute rotated EOFs.

## References

1. **Artificial Flow Patterns**: [Reference](https://rmets.onlinelibrary.wiley.com/doi/abs/10.1002/joc.1574)
2. **MIGRF Data Sets**: [Reference](https://journals.ametsoc.org/view/journals/clim/36/10/JCLI-D-22-0549.1.xml)
3. **SST Data Sets**: [Reference](https://psl.noaa.gov/data/gridded/data.noaa.ersst.v5.html)
