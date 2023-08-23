
# README for EOF Analysis Repository

## Overview

This repository contains code for computing and visualising Empirical Orthogonal Functions (EOFs) of various datasets. The datasets include artificial flow patterns, sea surface temperature (SST) data, and correlated noise on isotropic random fields.

## Repository Structure

1. **flowPatterns.py**: Contains functions for plotting isolines and adding Gaussian noise to data. 
2. **sst.py**: Focuses on handling and processing SST data. The data is subset into various regions of the Pacific for analysis.
3. **ComputeEOFs.py**: Provides a class for computing EOFs using the `xeofs` package.
4. **MIGRF.py**: Generates and analyses datasets with correlated and uncorrelated noise. For each dataset, EOFs are computed and visualised.
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


## main classes

### Class: `Data` (from `Data.py`)

- **Attributes**:
    - `data`: The dataset to be created.
    - `num_points`: Number of grid points.
    - `num_timepoints`: Number of time points in the time series.
    - `lon`: Longitudes of the grid.
    - `lat`: Latitudes of the grid.
    - `title`: Title for the dataset.



### Class: `myEOF` (from `ComputeEOFs.py`)

- **Attributes**:
    - `data`: The input dataset (expected to be an xarray data-array).
    - `lon`: Longitudes of the dataset.
    - `lat`: Latitudes of the dataset.
    - `title`: Title for the dataset.
    - `eofs`: EOFs computed from the data (initialised to `None`).
    - `explained_variances`: Variance explained by each EOF (initialised to `None`).

## References

1. **Artificial Flow Patterns**: [Reference](https://rmets.onlinelibrary.wiley.com/doi/abs/10.1002/joc.1574)
2. **MIGRF Data Sets**: [Reference](https://journals.ametsoc.org/view/journals/clim/36/10/JCLI-D-22-0549.1.xml)
3. **SST Data Sets**: [Reference](https://psl.noaa.gov/data/gridded/data.noaa.ersst.v5.html)
