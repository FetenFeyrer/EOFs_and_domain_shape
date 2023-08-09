import numpy as np  
import xarray as xr


# inputs:
# data = np.array (eofs) to convert: (features, eofs)
# lats = number of lat points
# lons = number of lon points
# title = str


def construct_xarray(data, lats, lons, title='data'):
    data = data.reshape(10000,lats,lons)
    
    n_time_samples = data.shape[0]
    

    lat = np.linspace(87, -87, lats)
    lon = np.linspace(0, 357, lons)
    time = np.arange(1, n_time_samples+1, dtype=np.int64)

    # Create the attributes for the new Xarray data array
    attributes = {
        'long_name': title,
        'units': 'int64',
        'description': ' input_dataset'
    }

    # Create the new Xarray data array
    data_xr = xr.DataArray(
        data,
        dims=('time', 'lat', 'lon'),
        coords={'lat': lat, 'lon': lon, 'time': time},
        attrs=attributes,
    )

    data_xr['lat'] = data_xr['lat'].astype(np.float32)
    data_xr['lon'] = data_xr['lon'].astype(np.float32)
    return data_xr