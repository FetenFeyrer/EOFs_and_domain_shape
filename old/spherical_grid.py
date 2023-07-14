import xarray as xr
import numpy as np
import plot_spherical as plt
import cdsapi as cds

# Create latitude and longitude arrays
lat = np.arange(-90, 91, 5)
lon = np.arange(-180, 181, 5)

# Create a meshgrid of latitude and longitude
lon_mesh, lat_mesh = np.meshgrid(lon, lat)

# Create an empty DataArray with coordinates
#data = 1008 + (lat_mesh + lon_mesh) % 25  # Apply a pattern to the data
#ds = xr.DataArray(data, coords=[('lat', lat), ('lon', lon)], dims=['lat', 'lon'])


c = cds.Client()

request = {
    'product_type': 'reanalysis',
    'format': 'netcdf',
    'variable': 'mean_sea_level_pressure',
    'year': '2022',
    'month': '01',
    'day': '01',
    'time': '12:00',
    'area': [-90, -180, 90, 180],  # South, West, North, East
    'grid': [5.0, 5.0],  # Latitude, Longitude grid spacing
}
c.retrieve('reanalysis-era5-pressure-levels', request, 'era5_pressure.nc')

dataset = xr.open_dataset('era5_pressure.nc')

slp = dataset['msl']



plt.plot_isolines(dataset)
