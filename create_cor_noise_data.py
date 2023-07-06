from climnet.myutils import *
from climnet.grid import FeketeGrid
from sklearn.gaussian_process.kernels import Matern
import numpy as np
from climnet.myutils import plot_map_lonlat
import eof_plot_scatter as plt

def rand_cor_noise(length_scale=1.5, is_uncorrelated=False):
    grid = FeketeGrid(num_points=1500, num_iter=1000)

    lon, lat = grid.grid['lon'], grid.grid['lat']
   

    cartesian_grid = spherical2cartesian(lon,lat)

    ar_coeff = np.zeros(1500)
    #ar_coeff = 0.9 * np.ones(760)

    #np.randint
    # half of the points random have high autocorrealtion


    kernel = 1.0 * Matern(length_scale=0.2, nu=1.5, )
    cov = kernel(cartesian_grid)
    if(is_uncorrelated):
        cov = np.eye(760)

    np.random.seed(18360)
    data = diag_var_process(ar_coeff, cov, n_time=365)

    sample_time_point = data[:6]
    

    #plt.plot(sample_time_point, sample_time_point, lon, lat, 'test')


    #plot_map_lonlat(lon, lat, sample_time_point)
    #plt.savefig('scatter_plot.pdf')
    #plt.clf()

    return data, lon, lat

