import compute_pca_xeofs as xeofs
import xarray as xr
from Data import *
from ComputeEOFs import *
import matplotlib.pyplot as plt
import eof_plot as plt

# load SST data
data = xr.tutorial.open_dataset('ersstv5')['sst']

# assert that std deviation is not zero for normalisation
minimum_std_dev = 1e-5
valid_x = data.stack(x=['lat', 'lon']).std('time') > minimum_std_dev
data = data.stack(x=['lat', 'lon']).sel(x=valid_x).unstack()

# Define the latitude and longitude range for the Pacific region
lat_range = slice(-70, 70) 
lon_range = slice(100, 300)  


# Crop the dataset to the specified window
data_pacific = data.where(
    (data.lat >= lat_range.start) & (data.lat <= lat_range.stop) &
    (data.lon >= lon_range.start) & (data.lon <= lon_range.stop),
    drop=True
)

# Define the latitude and longitude range for the northern pacific region
lat_range = slice(-70, -30)  
lon_range = slice(120, 280)  

data_pacific_top = data.where(
    (data.lat >= lat_range.start) & (data.lat <= lat_range.stop) &
    (data.lon >= lon_range.start) & (data.lon <= lon_range.stop),
    drop=True
)


# Define the latitude and longitude range for the middle pacific region
lat_range = slice(-30, 30)
lon_range = slice(120, 280) 

data_pacific_middle = data.where(
    (data.lat >= lat_range.start) & (data.lat <= lat_range.stop) &
    (data.lon >= lon_range.start) & (data.lon <= lon_range.stop),
    drop=True
)


# Define the latitude and longitude range for the southern pacific region
lat_range = slice(30, 70) 
lon_range = slice(120, 280)  

data_pacific_bottom = data.where(
    (data.lat >= lat_range.start) & (data.lat <= lat_range.stop) &
    (data.lon >= lon_range.start) & (data.lon <= lon_range.stop),
    drop=True
)


# Define the latitude and longitude range for a pacific region, only ocean
lat_range = slice(-70, -30) 
lon_range = slice(200, 260) 

data_pacific_ocean = data.where(
    (data.lat >= lat_range.start) & (data.lat <= lat_range.stop) &
    (data.lon >= lon_range.start) & (data.lon <= lon_range.stop),
    drop=True
)

# Define the latitude and longitude range for a middle-american region
lat_range = slice(30, 70)  
lon_range = slice(190, 280)  

data_pacific_midAmerica = data.where(
    (data.lat >= lat_range.start) & (data.lat <= lat_range.stop) &
    (data.lon >= lon_range.start) & (data.lon <= lon_range.stop),
    drop=True
)


#compute EOFs and rotated EOFs
eofs, rot_eofs, exp_var, rot_exp_var = xeofs.compute_pca(data)

# plot first 3 global EOFs and rotated EOFs
plt.plot(eofs, rot_eofs, 'SST EOFs global')

#compute EOFs and rotated EOFs
eofs, rot_eofs, exp_var, rot_exp_var = xeofs.compute_pca(data_pacific)

# plot first 3 global EOFs and rotated EOFs
plt.plot(eofs, rot_eofs, 'SST EOFs pacific', True)

#compute EOFs and rotated EOFs
eofs, rot_eofs, exp_var, rot_exp_var = xeofs.compute_pca(data_pacific_bottom)

# plot first 3 global EOFs and rotated EOFs
plt.plot(eofs, rot_eofs, 'SST EOFs northern pacific', True)

#compute EOFs and rotated EOFs
eofs, rot_eofs, exp_var, rot_exp_var = xeofs.compute_pca(data_pacific_middle)

# plot first 3 global EOFs and rotated EOFs
plt.plot(eofs, rot_eofs, 'SST EOFs central pacific', True)

#compute EOFs and rotated EOFs
eofs, rot_eofs, exp_var, rot_exp_var = xeofs.compute_pca(data_pacific_top)

# plot first 3 global EOFs and rotated EOFs
plt.plot(eofs, rot_eofs, 'SST EOFs southern pacific', True)

#compute EOFs and rotated EOFs
eofs, rot_eofs, exp_var, rot_exp_var = xeofs.compute_pca(data_pacific_ocean)

# plot first 3 global EOFs and rotated EOFs
plt.plot(eofs, rot_eofs, 'SST EOFs pacific ocean', True)

#compute EOFs and rotated EOFs
eofs, rot_eofs, exp_var, rot_exp_var = xeofs.compute_pca(data_pacific_midAmerica)

# plot first 3 global EOFs and rotated EOFs
plt.plot(eofs, rot_eofs, 'SST EOFs middle america', True)