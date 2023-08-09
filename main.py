
import compute_pca_xeofs as xeofs
import os
import eof_plot_scatter as plt
import fixed_point_plot_scatter as pt_plt
import numpy as np
import create_cor_noise_data as cnd
from construct_xarray_data import construct_xarray
import construct_xarray_eofs as construct_np
from plot_eigenvalues import plot_eigenvalue_sequences
import xarray as xr

from climnet.grid import spherical2cartesian


def main(data,title, lon=[], lat=[]):

    minimum_std_dev = 1e-5
    valid_x = data.stack(x=['lat', 'lon']).std('time') > minimum_std_dev
    data = data.stack(x=['lat', 'lon']).sel(x=valid_x).unstack()
    
    

    fixed_time_point = data.values[:6]
    #print(fixed_time_point.shape)
    fixed_time_point = fixed_time_point.reshape(6,1500)


    fixed_xr = construct_np.construct_xarray(fixed_time_point, 30, 50)
    #print(fixed_xr)

    # Compute eofs and varimax rotated eofs
    cov_pcs, cov_eofs, rot_cov_eofs, cov_exp_var, rot_cov_exp_var = xeofs.compute_pca(data)
    #print(fixed_xr)
    print(cov_eofs)
    
    #cov_eofs, rot_cov_eofs, x = eof_man.compute_pca(data)
    #plt.plot(fixed_xr, fixed_xr, title)
    pt_plt.plot(fixed_xr, lon, lat, 'Sample fixed Point 10000 points:   '+str(title), extent=[-180,0,-50,50])
    plt.plot(cov_eofs, lon, lat, 'EOFs 1-6 10000 points:     '+str(title), extent=[-180,0,-50,50])

    #lon = data['lon']
    #lat = data['lat'].values

    #plot_map_lonlat(lon,lon,data)

    #plt_np.plot_eofs(cov_eofs)
    print('finished: ' + title)
    return cov_exp_var.values



if __name__== '__main__':
    
    #random_cor_noise = cnd.rand_cor_noise(is_uncorrelated=False)
    #np.savetxt('/Users/julianfeyrer/Documents/GitHub/EOFs_and_domain_shape/datasets/random_uncorrelated_noise.txt', random_cor_noise)

    
    
    def eigenvalue_line_plot(title):
        list_exp_vars = []
        for i in range(0, 30):
            random_corr_file = '/Users/julianfeyrer/Documents/GitHub/EOFs_and_domain_shape/datasets_scatter - ' + str(title) + '/random_correlated_noise_'+str(int(i))+'.txt'
            random_cor_noise = np.loadtxt(random_corr_file)

            #random_cor_noise = cnd.rand_cor_noise(length_scale=i, is_uncorrelated=False)


            data = construct_xarray(random_cor_noise, 30, 50)
            exp_var = main(data, ' - EOFs Random correlated noise l='+str(i))
            
            exp_var_sum = np.sum(exp_var)

            exp_var /= exp_var_sum
            exp_var = exp_var*100

            print(np.sum(exp_var))
            
            list_exp_vars.append(exp_var)
            
        #print(list_exp_vars)
        plot_eigenvalue_sequences(list_exp_vars, 'Correlated Noise - '+str(title))

    '''eigenvalue_line_plot('l=0,05 nu=1,5 NO_AR')
    eigenvalue_line_plot('l=0,10 nu=1,5 NO_AR')
    eigenvalue_line_plot('l=0,20 nu=1,5 NO_AR')
    eigenvalue_line_plot('l=0,20 nu=1,5 0,9 AR')
    eigenvalue_line_plot('l=0,30 nu=1,5 0,9 AR')
    eigenvalue_line_plot('NO SC - 0,7 AR')
    eigenvalue_line_plot('NO SC - 0,9 AR')'''

    





    '''for i in range(1, 31):
        #random_corr_file = '/Users/julianfeyrer/Documents/GitHub/EOFs_and_domain_shape/datasets_scatter UNCORRELATED/random_correlated_noise_'+str(int(i))+'.txt'
        random_cor_noise, lon, lat = cnd.rand_cor_noise(seed_offset=i, is_uncorrelated=False)
        #random_cor_noise = np.loadtxt(random_corr_file)

        data = construct_xarray(random_cor_noise, 30, 50)
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

        main(data_pacific, 'EOFS Pacific cropped random noise - l='+str(i)+'0 - TEST', lon, lat)'''








    '''random_cor_noise, lon, lat = cnd.rand_cor_noise(length_scale=0.2)
    #np.savetxt('/Users/julianfeyrer/Documents/GitHub/EOFs_and_domain_shape/datasets/random_correlated_noise_0d50.txt', random_cor_noise)
    data = construct_xarray(random_cor_noise, 30, 50)
    main(data, 'Scatter test', lon, lat)'''


    ############################ MAIN LOOP #####################
    for i in range(31):
        random_cor_noise, lon, lat = cnd.rand_cor_noise(i, is_uncorrelated=False)
        print(lon.shape)
        np.savetxt('/Users/julianfeyrer/Documents/GitHub/EOFs_and_domain_shape/datasets_scatter/random_correlated_noise_'+str(i)+'.txt', random_cor_noise)
        data = construct_xarray(random_cor_noise, 30, 50)
        main(data, 'Random correlated noise - Iteration: '+str(i), lon, lat)
        ##os.remove('/Users/julianfeyrer/Documents/GitHub/EOFs_and_domain_shape/feketegrid_1500_1000.p')'''


    '''import compute_spherical_harmonics as sph


    random_cor_noise, lon, lat = cnd.rand_cor_noise()
    data = construct_xarray(random_cor_noise, 30, 50)

    

    cov_pcs, cov_eofs, rot_cov_eofs, cov_exp_var, rot_cov_exp_var = xeofs.compute_pca(data)

    cov_eofs_swapped = cov_eofs.transpose('mode', 'lat', 'lon')

    modified_eofs_T = sph.subtract_domain_shape(cov_eofs_swapped,6, 2, lon, lat)

    modified_eofs = modified_eofs_T.transpose(0, 1, 2)
    modified_eofs = modified_eofs[:6]

    

    lat_xr = np.linspace(90, -90, 30)
    lon_xr = np.linspace(0, 360, 50)
    mode = np.arange(1, 7, dtype=np.int64)

    # Create the attributes for the new Xarray data array
    attributes = {
        'long_name': 'SPHERICAL TEST',
        'description': 'Empirical Orthogonal Functions'
    }

    # Create the new Xarray data array
    modified_eofs_xr = xr.DataArray(
        modified_eofs,
        dims=('mode', 'lat', 'lon'),
        coords={'lat': lat_xr, 'lon': lon_xr, 'mode': mode},
        attrs=attributes,
    )
    print(modified_eofs.shape)
    plt.plot(cov_eofs, lon, lat, 'EOFs WITHOUT CORRECTION:')
    plt.plot(modified_eofs_xr, lon, lat, 'EOFs SPHERICAL HARMONICS TEST:')

    cov_eofs_T = cov_eofs.transpose('mode', 'lat', 'lon')
    cov_eofs_T = cov_eofs_T[:6]


    #print(cov_eofs_T.shape)

    alg_cov_eofs, alg_mod_cov_eofs = xr.align(cov_eofs_T, modified_eofs_xr, join='exact')

    corrected_eofs = alg_cov_eofs - alg_mod_cov_eofs
    print(corrected_eofs)
    plt.plot(corrected_eofs, lon, lat, 'CORRECTION')'''

















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
    
    
    
    
    
