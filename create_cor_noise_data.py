from climnet.myutils import *
from climnet.grid import FeketeGrid
from sklearn.gaussian_process.kernels import Matern
import numpy as np
from climnet.myutils import plot_map_lonlat
import eof_plot_scatter as plt

def rand_cor_noise(seed_offset=0, is_uncorrelated=False):
    grid = FeketeGrid(num_points=1500, num_iter=1000)

    #print(grid.grid['lat'].shape)

    lat_range = [-50,49]  # Specify the desired latitude range (-30 to 30 degrees)
    lon_range = [-366,1] # Specify the desired longitude range (120 to 280 degrees)

    cutted_grid = grid.cut_grid(lat_range, lon_range)

    lon_range = [1,359]

    
    #print(cutted_grid['lon'].shape)
    
    #lon, lat = cutted_grid['lon'], cutted_grid['lat']

    lon, lat = grid.grid['lon'], grid.grid['lat']

   

    cartesian_grid = spherical2cartesian(lon,lat)

    ar_coeff = np.zeros(1500)
    #ar_coeff = 0.9 * np.ones(570)

    #np.randint
    # half of the points random have high autocorrealtion


    kernel = 1.0 * Matern(length_scale=0.2, nu=1.5, )
    cov = kernel(cartesian_grid)
    if(is_uncorrelated):
        cov = np.eye(570)

    np.random.seed(18360-seed_offset)
    data = diag_var_process(ar_coeff, cov, n_time=10000)

    sample_time_point = data[:6]
    

    #plt.plot(sample_time_point, sample_time_point, lon, lat, 'test')


    #plot_map_lonlat(lon, lat, sample_time_point)
    #plt.savefig('scatter_plot.pdf')
    #plt.clf()

    return data, lon, lat

