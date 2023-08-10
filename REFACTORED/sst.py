import compute_pca_xeofs as xeofs
import xarray as xr
from Data import *
from ComputeEOFs import *
import matplotlib.pyplot as plt
import eof_plot as plt


data = xr.tutorial.open_dataset('ersstv5')['sst']

minimum_std_dev = 1e-5
valid_x = data.stack(x=['lat', 'lon']).std('time') > minimum_std_dev
data = data.stack(x=['lat', 'lon']).sel(x=valid_x).unstack()

eofs, rot_eofs, exp_var, rot_exp_var = xeofs.compute_pca(data, n_components=10)


plt.plot(eofs, rot_eofs, 'SST EOFs global')