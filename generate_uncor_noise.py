from climnet.myutils import *
from climnet.grid import FeketeGrid
from sklearn.gaussian_process.kernels import Matern
import numpy as np

def rand_uncor_noise():
    grid = FeketeGrid(num_points=3120, num_iter=1000)

    lon, lat = grid.grid['lon'], grid.grid['lat']

    cartesian_grid = spherical2cartesian(lon, lat)

    ar_coeff = np.zeros(3120)

    np.random.seed(18360)
    data = np.random.multivariate_normal(np.zeros(3120), np.eye(3120), size=365)

    print(data)
    return data
