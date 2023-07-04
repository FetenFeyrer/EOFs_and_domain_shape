import numpy as np
from xeofs.models import EOF
import varimax_xeofs as rot
import xarray as xr
# input: a data set (n x 36(=p)), (number of components computed))
#
# returns: PC loadings (nx36)
def compute_pca(data, n_components=6, correlation_mode=False, custom_weights=None):
    

   
    model = EOF(data, n_modes=n_components, norm=True)
    model.solve()
    
    #pca.fit(data)
    
    #pc_scores = pca.fit_transform(data)
    eofs = model.eofs()

    #eofs = eofs.reshape()

    

    num_lat_points = int(np.sqrt(data.shape[1] / 2))
    num_lon_points = int(2 * num_lat_points)

    print(num_lon_points*num_lat_points)

    lat = np.linspace(-90, 90, num_lat_points)
    lon = np.linspace(-180, 180, num_lon_points)
    mode = np.arange(1, n_components, dtype=np.int64)

    # Create the attributes for the new Xarray data array
    attributes = {
        'long_name': 'EOFs',
        'units': 'dimensionless',
        'description': 'Empirical Orthogonal Functions',
        'source': 'Some source',
    }

    # Create the new Xarray data array
    eofs_xar = xr.DataArray(
        eofs,
        dims=('lat', 'lon', 'mode'),
        coords={'lat': lat, 'lon': lon, 'mode': mode},
        attrs=attributes,
    )
    

    explained_variances = model.explained_variance_ratio()

    pcs = model.pcs()
    #print(loadings.shape)

    #varimax rotation
    rot_eofs, rot_explained_variances = rot.varimax_xeofs(model)
    
    
    return pcs, eofs, rot_eofs, explained_variances*100, rot_explained_variances*100
