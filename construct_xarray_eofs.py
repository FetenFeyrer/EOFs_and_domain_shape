import numpy as np  
import xarray as xr


# inputs:
# data = np.array (eofs) to convert: (features, eofs)
# lats = number of lat points
# lons = number of lon points


def construct_xarray(data, lats, lons, title='data'):
    data = data.reshape(6,lats,lons)

    n_components = data.shape[0]
    

    lat = np.linspace(90, -90, lats)
    lon = np.linspace(0, 360, lons)
    mode = np.arange(1, n_components+1, dtype=np.int64)

    # Create the attributes for the new Xarray data array
    attributes = {
        'long_name': title,
        'description': 'Empirical Orthogonal Functions'
    }

    # Create the new Xarray data array
    eofs_xar = xr.DataArray(
        data,
        dims=('mode', 'lat', 'lon'),
        coords={'lat': lat, 'lon': lon, 'mode': mode},
        attrs=attributes,
    )
    return eofs_xar