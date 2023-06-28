
import compute_pca_xeofs as xeofs
import xarray as xr
import eof_plot as plt
import numpy as np
import create_cor_noise_data as cnd
import plot_eofs_np as plt_np


def main(data, title):

    #minimum_std_dev = 1e-5
    #valid_x = data.stack(x=['lat', 'lon']).std('time') > minimum_std_dev
    #data = data.stack(x=['lat', 'lon']).sel(x=valid_x).unstack()
    
   

    

    # Compute eofs and varimax rotated eofs
    cov_pcs, cov_eofs, rot_cov_eofs, cov_exp_var, rot_cov_exp_var = xeofs.compute_pca(data)
    print(cov_eofs.shape)
    #cov_eofs, rot_cov_eofs, x = eof_man.compute_pca(data)
    #plt.plot(cov_eofs, rot_cov_eofs, title)
    plt_np.plot_eofs(cov_eofs)



if __name__== '__main__':
    
    random_cor_noise = cnd.rand_cor_noise()
    
    main(random_cor_noise, 'random Correlated')
    
    
    
    
    
