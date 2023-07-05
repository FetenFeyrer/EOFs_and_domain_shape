from climnet.myutils import *
from climnet.grid import FeketeGrid
from sklearn.gaussian_process.kernels import Matern
import numpy as np

def rand_cor_noise(length_scale=1.5, is_uncorrelated=False):
    grid = FeketeGrid(num_points=7080, num_iter=1000)

    lon, lat = grid.grid['lon'], grid.grid['lat']

    cartesian_grid = spherical2cartesian(lon,lat)

    ar_coeff = np.zeros(7080)

    kernel = 1.0 * Matern(length_scale=length_scale, nu=1.5, )
    cov = kernel(cartesian_grid)
    if(is_uncorrelated):
        cov = np.eye(7080)

    np.random.seed(18360)
    data = diag_var_process(ar_coeff, cov, n_time=365)

    return data