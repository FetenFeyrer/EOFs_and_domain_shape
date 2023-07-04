
import compute_pca_xeofs as xeofs
import xarray as xr
import eof_plot as plt
import numpy as np
import create_cor_noise_data as cnd
import plot_eofs_np as plt_np
from construct_xarray_data import construct_xarray


def main(data, title):

    #minimum_std_dev = 1e-5
    #valid_x = data.stack(x=['lat', 'lon']).std('time') > minimum_std_dev
    #data = data.stack(x=['lat', 'lon']).sel(x=valid_x).unstack()
    
   

    

    # Compute eofs and varimax rotated eofs
    cov_pcs, cov_eofs, rot_cov_eofs, cov_exp_var, rot_cov_exp_var = xeofs.compute_pca(data)
    
    #cov_eofs, rot_cov_eofs, x = eof_man.compute_pca(data)
    plt.plot(cov_eofs, rot_cov_eofs, title)
    #plt_np.plot_eofs(cov_eofs)



if __name__== '__main__':
    
    #random_cor_noise = cnd.rand_cor_noise()

    #data_xr = construct_xarray(random_cor_noise, 39, 80)
    #print(data_xr)

    #main(data_xr, ' random')


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

    main(data_pacific, 'whole')
    
    
    
    
    
