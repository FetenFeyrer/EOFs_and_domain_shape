import numpy as np
import numpy.ma as ma 
import xarray as xr
import sklearn as s
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler
import old.compute_adj_matrix as adj

# input: a data set (n x 36(=p)), (number of components computed))
#
# returns: PC loadings (nx36)
def compute_pca(data, n_components=3, correlation_mode=False):
    
    
    if correlation_mode:
        scaler = StandardScaler()
        data = scaler.fit_transform(data)
    
    #print(data)

    reshaped_data = data.values.reshape(data.values.shape[0], -1)

    #print(reshaped_data)
    #nan_counts = np.isnan(reshaped_data).sum(axis=0)
    #non_zero_counts = np.count_nonzero(nan_counts)
    #np.set_printoptions(threshold=np.inf)
    #print(nan_counts)
    #print(non_zero_counts)
    
    print(reshaped_data.shape)

    # Create a masked array, replacing NaN values with masked values
    #masked_array = ma.masked_invalid(reshaped_data)

    # Calculate the covariance matrix of the masked array
    #cov = ma.cov(masked_array, rowvar=False)

    cov = np.cov(reshaped_data, rowvar=False)
    #print(cov)

    #cov = ma.filled(cov, np.nan)
    print(cov.shape)

    adj_matrix = adj.compute_adj_matrix(data)

    scaled_cov = cov * adj_matrix.T

    print(adj_matrix.shape)

    ev , eig = np.linalg.eig(cov)
    #a = eig.dot(reshaped_data.T)
    

    eig = np.real(eig.reshape((21, 31, 651)))

    #print(eig)

    # Define the coordinate values
    lat_values = np.linspace(-70, -30, 21)
    lon_values = np.linspace(200, 260, 31)
    mode_values = np.arange(1, 652)

    # Create the coordinate variables
    lat = xr.DataArray(lat_values, dims='lat', name='lat')
    lon = xr.DataArray(lon_values, dims='lon', name='lon')
    mode = xr.DataArray(mode_values, dims='mode', name='mode')

    # Create the xarray DataArray
    data_array = xr.DataArray(eig, dims=('lat', 'lon', 'mode'), coords=(lat, lon, mode), name='EOFs')

    #print(eig)
    return data_array, data_array, [1,1,1]
