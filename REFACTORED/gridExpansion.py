from sklearn.gaussian_process import GaussianProcessRegressor
from sklearn.gaussian_process.kernels import Matern
from sklearn.preprocessing import StandardScaler
import numpy as np

def extend_grid_with_data(lon, lat, data, num_extension_points):
    """
    Extend the given grid with additional points and assign data to the new grid points using Gaussian Process regression.

    Parameters:
    ----------
    lon: numpy array
        Original longitudes of the grid.
    lat: numpy array
        Original latitudes of the grid.
    data: xarray.DataArray
        Original data values on the original grid.
    num_extension_points: int
        Number of additional points to add in each direction.

    Returns:
    -------
    extended_lon: numpy array
        Extended longitudes of the grid.
    extended_lat: numpy array
        Extended latitudes of the grid.
    extended_data: numpy array
        Extended data values assigned to the new grid points using Gaussian Process regression.
    """
    # Find the min and max of the original longitude and latitude arrays
    lon_min, lon_max = lon.min(), lon.max()
    lat_min, lat_max = lat.min(), lat.max()

    # Compute the longitude and latitude step sizes of the original grid
    lon_step = lon[1] - lon[0]
    lat_step = lat[1] - lat[0]

    # Extend the longitude and latitude arrays in both directions
    extended_lon = np.arange(lon_min - num_extension_points * lon_step, lon_max + (num_extension_points + 1) * lon_step, lon_step)
    extended_lat = np.arange(lat_min - num_extension_points * lat_step, lat_max + (num_extension_points + 1) * lat_step, lat_step)

    # Create a meshgrid of the extended longitude and latitude points
    extended_lon_mesh, extended_lat_mesh = np.meshgrid(extended_lon, extended_lat)

    # Combine the original grid and extended grid coordinates
    all_lon = np.concatenate((lon, extended_lon_mesh.ravel()))
    all_lat = np.concatenate((lat, extended_lat_mesh.ravel()))

    # Flatten the data for Gaussian Process regression
    data_flat = data.values.ravel()

    # Fit a Gaussian Process regressor to interpolate the data
    kernel = 1.0 * Matern(length_scale=0.2, nu=1.5)
    regressor = GaussianProcessRegressor(kernel=kernel, n_restarts_optimizer=10)

    # Initialize the array to hold the extended data
    extended_data = np.empty((extended_lat_mesh.shape[0], extended_lon_mesh.shape[1]))

    # Perform interpolation for each grid point in the extended grid
    for i in range(extended_lat_mesh.shape[0]):
        for j in range(extended_lon_mesh.shape[1]):
            X_train = np.column_stack((lon.ravel(), lat.ravel()))
            X_test = np.array([[extended_lon_mesh[i, j], extended_lat_mesh[i, j]]])

            scaler = StandardScaler()
            data_scaled = scaler.fit_transform(data_flat.reshape(-1, 1))
            regressor.fit(X_train, data_scaled)

            # Predict data value for the current grid point
            extended_data_scaled = regressor.predict(X_test)

            # Rescale the predicted data to the original scale
            extended_data[i, j] = scaler.inverse_transform(extended_data_scaled)

    return extended_lon, extended_lat, extended_data
