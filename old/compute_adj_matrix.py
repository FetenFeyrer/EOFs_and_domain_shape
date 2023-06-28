import numpy as np
import xarray as xr
from scipy.spatial import distance



def compute_adj_matrix(dataset):
    latitudes = dataset.lat.values
    longitudes = dataset.lon.values

    # Calculate the spatial adjacency matrix
    num_locations = len(latitudes) * len(longitudes)
    adjacency_matrix = np.zeros((num_locations, num_locations))

    # Reshape the SST values into a 2D array
    sst_2d = dataset.values.reshape(dataset.values.shape[0], -1).T

    #nan_counts = np.isnan(sst_2d).sum(axis=1)
    #non_zero_counts = np.count_nonzero(nan_counts)
    np.set_printoptions(threshold=np.inf)
    #print(nan_counts)
    #print(non_zero_counts)

    # Calculate the Euclidean distance between locations
    distances = distance.cdist(sst_2d, sst_2d, metric='euclidean')
    print(distances.shape)
    

    # Assign weights to the adjacency matrix based on the distances
    for i in range(num_locations):
        for j in range(num_locations):
            if i != j:
                adjacency_matrix[i, j] = 1 / distances[i, j]  # Inverse distance weighting


    

    # Compute the minimum and maximum values of the array, ignoring NaN values
    min_value = np.nanmin(adjacency_matrix)
    max_value = np.nanmax(adjacency_matrix)

    # Normalize the array, handling NaN values
    adjacency_matrix_norm = (adjacency_matrix - min_value) / (max_value - min_value)

    #print(np.nanmax(adjacency_matrix_norm))

    #np.savetxt('adj_array_norm.txt', adjacency_matrix_norm, fmt='%f')

    # Convert the adjacency matrix to xarray DataArray for further analysis
    adjacency_data = xr.DataArray(adjacency_matrix_norm, dims=['locations', 'locations'],
                                coords={'locations': np.arange(num_locations)})

   
  

    return adjacency_matrix_norm


