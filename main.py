
import compute_pca_xeofs as xeofs
import xarray as xr
import eof_plot as plt
import numpy as np

import compute_adj_matrix as adj
import compute_pca_manual as eof_man


def main(data, title):

    minimum_std_dev = 1e-5
    valid_x = data.stack(x=['lat', 'lon']).std('time') > minimum_std_dev
    data = data.stack(x=['lat', 'lon']).sel(x=valid_x).unstack()
    
    #weights = adj.compute_adj_matrix(data)
    #print(weights)
    
    time, lat, lon = data.shape

    window = np.outer(np.hanning(lat), np.hanning(lon))

    data = data * window

    # Compute eofs and varimax rotated eofs
    cov_pcs, cov_eofs, rot_cov_eofs, cov_exp_var, rot_cov_exp_var = xeofs.compute_pca(data, custom_weights='coslat')
    #
    #cov_eofs, rot_cov_eofs, x = eof_man.compute_pca(data)
    plt.plot(cov_eofs, rot_cov_eofs, title)



if __name__== '__main__':
    data = xr.tutorial.open_dataset('ersstv5')['sst']

    # Define the latitude and longitude range for the Pacific region
    lat_range = slice(-70, 70)  # Specify the desired latitude range (-30 to 30 degrees)
    lon_range = slice(100, 300)  # Specify the desired longitude range (120 to 280 degrees)

    # Crop the dataset to the specified region
    #data = data.sel(lat=lat_range, lon=lon_range)

    # Crop the dataset to the specified window
    data_pacific = data.where(
        (data.lat >= lat_range.start) & (data.lat <= lat_range.stop) &
        (data.lon >= lon_range.start) & (data.lon <= lon_range.stop),
        drop=True
    )

    # Define the latitude and longitude range for the Pacific region
    lat_range = slice(-70, -30)  # Specify the desired latitude range (-30 to 30 degrees)
    lon_range = slice(120, 280)  # Specify the desired longitude range (120 to 280 degrees)

    data_pacific_top = data.where(
        (data.lat >= lat_range.start) & (data.lat <= lat_range.stop) &
        (data.lon >= lon_range.start) & (data.lon <= lon_range.stop),
        drop=True
    )
    #data_pacific_top = data_pacific_top.sortby('lat')


    # Define the latitude and longitude range for the Pacific region
    lat_range = slice(-30, 30)  # Specify the desired latitude range (-30 to 30 degrees)
    lon_range = slice(120, 280)  # Specify the desired longitude range (120 to 280 degrees)

    data_pacific_middle = data.where(
        (data.lat >= lat_range.start) & (data.lat <= lat_range.stop) &
        (data.lon >= lon_range.start) & (data.lon <= lon_range.stop),
        drop=True
    )


    # Define the latitude and longitude range for the Pacific region
    lat_range = slice(30, 70)  # Specify the desired latitude range (-30 to 30 degrees)
    lon_range = slice(120, 280)  # Specify the desired longitude range (120 to 280 degrees)

    data_pacific_bottom = data.where(
        (data.lat >= lat_range.start) & (data.lat <= lat_range.stop) &
        (data.lon >= lon_range.start) & (data.lon <= lon_range.stop),
        drop=True
    )
    
    
    # Define the latitude and longitude range for the Pacific region
    lat_range = slice(-70, -30)  # Specify the desired latitude range (-30 to 30 degrees)
    lon_range = slice(200, 260)  # Specify the desired longitude range (120 to 280 degrees)

    data_pacific_ocean = data.where(
        (data.lat >= lat_range.start) & (data.lat <= lat_range.stop) &
        (data.lon >= lon_range.start) & (data.lon <= lon_range.stop),
        drop=True
    )

    # Define the latitude and longitude range for the Pacific region
    lat_range = slice(30, 70)  # Specify the desired latitude range (-30 to 30 degrees)
    lon_range = slice(190, 280)  # Specify the desired longitude range (120 to 280 degrees)
    data_pacific_midAmerica = data.where(
        (data.lat >= lat_range.start) & (data.lat <= lat_range.stop) &
        (data.lon >= lon_range.start) & (data.lon <= lon_range.stop),
        drop=True
    )

    #main(data, 'Whole')
    main(data_pacific, 'Pacific')
    #print(data_pacific)
    main(data_pacific_top, 'PacificTop')
    main(data_pacific_ocean, 'PacificOcean')
    main(data_pacific_midAmerica, 'PacificOcean')
    main(data_pacific_middle, 'PacificMiddle')
    main(data_pacific_bottom, 'PacificBottom')
    
    
    
    
    
