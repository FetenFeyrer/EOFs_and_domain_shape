
import compute_pca_xeofs as xeofs
import xarray as xr
import eof_plot as plt
import eof_plot_scatter as plt_sct
import numpy as np
import create_cor_noise_data as cnd
import generate_uncor_noise as uncor
import plot_eofs_np as plt_np
from construct_xarray_data import construct_xarray
import construct_xarray_eofs as construct_np
from plot_eigenvalues import plot_eigenvalue_sequences

from climnet.myutils import plot_map_lonlat


def main(data,title, lon=[], lat=[]):

    minimum_std_dev = 1e-5
    valid_x = data.stack(x=['lat', 'lon']).std('time') > minimum_std_dev
    data = data.stack(x=['lat', 'lon']).sel(x=valid_x).unstack()
    
   

    fixed_time_point = data.values[:6]
    fixed_time_point = fixed_time_point.reshape(6,1500)

    print('finished: ' + title)

    fixed_xr = construct_np.construct_xarray(fixed_time_point.T, 30, 50)
    #print(fixed_xr)

    # Compute eofs and varimax rotated eofs
    cov_pcs, cov_eofs, rot_cov_eofs, cov_exp_var, rot_cov_exp_var = xeofs.compute_pca(data)
    #print(fixed_xr)
    #print(rot_cov_exp_var)
    
    #cov_eofs, rot_cov_eofs, x = eof_man.compute_pca(data)
    #plt.plot(fixed_xr, fixed_xr, title)
    plt_sct.plot(fixed_xr, lon, lat, title)

    #lon = data['lon']
    #lat = data['lat'].values

    #plot_map_lonlat(lon,lon,data)

    #plt_np.plot_eofs(cov_eofs)
    print('finished: ' + title)
    #return cov_exp_var.values



if __name__== '__main__':
    
    #random_cor_noise = cnd.rand_cor_noise(is_uncorrelated=False)
    #np.savetxt('/Users/julianfeyrer/Documents/GitHub/EOFs_and_domain_shape/datasets/random_uncorrelated_noise.txt', random_cor_noise)

    
    

    '''list_exp_vars = []
    for i in range(1, 9):
        i /= 10.0
        random_corr_file = '/Users/julianfeyrer/Documents/GitHub/EOFs_and_domain_shape/datasets/random_correlated_noise_0d'+str(int(i*100))+'.txt'
        random_cor_noise = np.loadtxt(random_corr_file)

        #random_cor_noise = cnd.rand_cor_noise(length_scale=i, is_uncorrelated=False)


        data = construct_xarray(random_cor_noise, 59, 120)
        exp_var = main(data, ' - EOFs Random correlated noise l='+str(i)+'0'+' - ISOLINES ')
        
        
        list_exp_vars.append(exp_var)
        
    print(list_exp_vars)
    plot_eigenvalue_sequences(list_exp_vars)'''

    

    '''for i in range(1, 9):
        i /= 10.0
        #random_corr_file = '/Users/julianfeyrer/Documents/GitHub/EOFs_and_domain_shape/datasets/random_correlated_noise_0d'+str(int(i*100))+'.txt'
        random_cor_noise = cnd.rand_cor_noise(length_scale=i, is_uncorrelated=False)
        #random_cor_noise = np.loadtxt(random_corr_file)

        data = construct_xarray(random_cor_noise, 19, 40)
        #data = xr.tutorial.open_dataset('ersstv5')['sst']
        #main(data, ' - EOFs Random correlated noise l=0')


        # Define the latitude and longitude range for the Pacific region
        lat_range = slice(-70, 70)  # Specify the desired latitude range (-88.0 to -30.0 degrees)
        lon_range = slice(100, 300)  # Specify the desired longitude range (120.0 to 280.0 degrees)


        # Crop the dataset to the specified window
        data_pacific = data.where(
            (data.lat >= lat_range.start) & (data.lat <= lat_range.stop) &
            (data.lon >= lon_range.start) & (data.lon <= lon_range.stop),
            drop=True
        )
        #print(data_pacific)

        main(data_pacific, 'Small EOFS Pacific cropped random noise - l='+str(i)+'0 - TEST')'''








    random_cor_noise, lon, lat = cnd.rand_cor_noise(length_scale=0.2)
    #np.savetxt('/Users/julianfeyrer/Documents/GitHub/EOFs_and_domain_shape/datasets/random_correlated_noise_0d50.txt', random_cor_noise)
    data = construct_xarray(random_cor_noise, 30, 50)
    main(data, 'Scatter test', lon, lat)























    #data = xr.tutorial.open_dataset('ersstv5')['sst']
    #print(data)
    # Define the latitude and longitude range for the Pacific region
    #lat_range = slice(-70, 70)  # Specify the desired latitude range (-30 to 30 degrees)
    #lon_range = slice(220, 320)  # Specify the desired longitude range (120 to 280 degrees)

    # Crop the dataset to the specified region
    #data = data.sel(lat=lat_range, lon=lon_range)

    # Crop the dataset to the specified window
    #data_pacific = data.where(
    #    (data.lat >= lat_range.start) & (data.lat <= lat_range.stop) &
    #    (data.lon >= lon_range.start) & (data.lon <= lon_range.stop),
    #    drop=True
    #)
    #print(data_pacific.shape)

    #main(data_pacific, 'whole')
    
    
    
    
    
