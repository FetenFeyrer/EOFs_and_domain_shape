from climnet.myutils import *
from climnet.grid import FeketeGrid
from sklearn.gaussian_process.kernels import Matern
import numpy as np

def rand_cor_noise():
    grid = FeketeGrid(num_points=3120, num_iter=50)

    lon, lat = grid.grid['lon'], grid.grid['lat']

    cartesian_grid = spherical2cartesian(lon,lat)

    ar_coeff = np.zeros(3120)

    kernel = 1.0 * Matern(length_scale=0.2, nu=1.5)
    cov = kernel(cartesian_grid)

    np.random.seed(18360)
    data = diag_var_process(ar_coeff, cov, n_time=365)

    return data