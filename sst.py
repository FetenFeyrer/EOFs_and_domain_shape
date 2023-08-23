import xarray as xr
from Data import *
from ComputeEOFs import *
import random
import warnings

warnings.filterwarnings("ignore", category=RuntimeWarning)

# load SST data
data = xr.tutorial.open_dataset('ersstv5')['sst']

# assert that std deviation is not zero for normalisation
minimum_std_dev = 1e-5
valid_x = data.stack(x=['lat', 'lon']).std('time') > minimum_std_dev
data = data.stack(x=['lat', 'lon']).sel(x=valid_x).unstack()

# Define the latitude and longitude range for the Pacific region
lat_range = slice(-70, 70) 
lon_range = slice(100, 300)  


# Crop the dataset to the specified window
data_pacific = data.where(
    (data.lat >= lat_range.start) & (data.lat <= lat_range.stop) &
    (data.lon >= lon_range.start) & (data.lon <= lon_range.stop),
    drop=True
)

# Define the latitude and longitude range for the northern pacific region
lat_range = slice(-70, -30)  
lon_range = slice(120, 280)  

data_pacific_top = data.where(
    (data.lat >= lat_range.start) & (data.lat <= lat_range.stop) &
    (data.lon >= lon_range.start) & (data.lon <= lon_range.stop),
    drop=True
)


# Define the latitude and longitude range for the central pacific region
lat_range = slice(-30, 30)
lon_range = slice(120, 280) 

data_pacific_middle = data.where(
    (data.lat >= lat_range.start) & (data.lat <= lat_range.stop) &
    (data.lon >= lon_range.start) & (data.lon <= lon_range.stop),
    drop=True
)


# Define the latitude and longitude range for the southern pacific region
lat_range = slice(30, 70) 
lon_range = slice(120, 280)  

data_pacific_bottom = data.where(
    (data.lat >= lat_range.start) & (data.lat <= lat_range.stop) &
    (data.lon >= lon_range.start) & (data.lon <= lon_range.stop),
    drop=True
)


# Define the latitude and longitude range for a pacific region, only ocean
lat_range = slice(-70, -30) 
lon_range = slice(200, 260) 

data_pacific_ocean = data.where(
    (data.lat >= lat_range.start) & (data.lat <= lat_range.stop) &
    (data.lon >= lon_range.start) & (data.lon <= lon_range.stop),
    drop=True
)

# Define the latitude and longitude range for a middle-american region
lat_range = slice(30, 70)  
lon_range = slice(190, 280)  

data_pacific_midAmerica = data.where(
    (data.lat >= lat_range.start) & (data.lat <= lat_range.stop) &
    (data.lon >= lon_range.start) & (data.lon <= lon_range.stop),
    drop=True
)


#compute EOFs and rotated EOFs
eofs, rot_eofs, exp_var, rot_exp_var = myEOF.compute_eofs_sst(data)

def random_sample_data(data):
    eigenvalue_list = []
    # create eigenvalue error bar plots
    for j in range(31):

        rnd_data = []

        for i in range(52):
            
            rnd_start = random.randint(0, 612)

            data_slice = data.isel(time=slice(rnd_start, rnd_start+12))

            rnd_data.append(data_slice)    
            
            
        rnd_new_dataset = xr.concat(rnd_data, dim='time')


        sst_eof = myEOF(rnd_new_dataset, rnd_new_dataset['lon'], rnd_new_dataset['lat'], ' SST EOF ')

        try:
            sst_eof.compute_eofs()
        except Exception as e:
            print('SVD did not converge, continuing with generation of next subset. Error: ', e)
            continue
            
        
        eigenvalues = sst_eof.explained_variances

        eigenvalue_list.append(eigenvalues)
        print('SST sampling Iteration: '+str(j))
    return eigenvalue_list
        #print('SST random sampling eigenvalue error bar plot computation - Done Iteration: ' + str(j))
    
eigenvalue_list = random_sample_data(data)
myEOF.plotEigenvalueErrorBars(eigenvalue_list, N=624, title='Global SST_sampling_eigenvalue_errorbars_ev:2-10', ignore_first_ev=True)
myEOF.plotEigenvalueErrorBars(eigenvalue_list, N=624, title='Global SST_sampling_eigenvalue_errorbars_ev:1-10')
myEOF.plot_eigenvalue_sequences(eigenvalue_list, 'Global SST sampling eigenvalue plot', ignore_first_ev=True)
print('Eigenvalue plot + error bar plot done: Global SST')
eigenvalue_list = random_sample_data(data_pacific)
myEOF.plot_eigenvalue_sequences(eigenvalue_list, 'Pacific SST sampling eigenvalue plot', ignore_first_ev=True)
myEOF.plotEigenvalueErrorBars(eigenvalue_list, N=624, title='Pacific SST_sampling_eigenvalue_errorbars_ev:2-10', ignore_first_ev=True)
print('Eigenvalue plot + error bar plot done: Pacific SST')
eigenvalue_list = random_sample_data(data_pacific_bottom)
myEOF.plot_eigenvalue_sequences(eigenvalue_list, 'Northern pacific SST sampling eigenvalue plot', ignore_first_ev=True)
myEOF.plotEigenvalueErrorBars(eigenvalue_list, N=624, title='Northern Pacific SST_sampling_eigenvalue_errorbars_ev:2-10', ignore_first_ev=True)
print('Eigenvalue plot + error bar plot done: Northern Pacific SST')
eigenvalue_list = random_sample_data(data_pacific_middle)
myEOF.plot_eigenvalue_sequences(eigenvalue_list, 'Central pacific SST sampling eigenvalue plot', ignore_first_ev=True)
myEOF.plotEigenvalueErrorBars(eigenvalue_list, N=624, title='Tropical Pacific SST_sampling_eigenvalue_errorbars_ev:2-10', ignore_first_ev=True)
print('Eigenvalue plot + error bar plot done: central Pacific SST')
eigenvalue_list = random_sample_data(data_pacific_top)
myEOF.plot_eigenvalue_sequences(eigenvalue_list, 'Southern pacific SST sampling eigenvalue plot', ignore_first_ev=True)
myEOF.plotEigenvalueErrorBars(eigenvalue_list, N=624, title='Southern Pacific SST_sampling_eigenvalue_errorbars_ev:2-10', ignore_first_ev=True)
print('Eigenvalue plot + error bar plot done: Southern Pacific SST')



# plot first 3 global EOFs and rotated EOFs
myEOF.sst_plot(eofs, rot_eofs, exp_var, rot_exp_var, 'SST EOFs 1-3 global')
myEOF.sst_plot(eofs, rot_eofs, exp_var, rot_exp_var, 'SST EOFs global 4-6', plot_offset=3)

print('SST global EOF plot done.')

#compute EOFs and rotated EOFs
eofs, rot_eofs, exp_var, rot_exp_var = myEOF.compute_eofs_sst(data_pacific)

# plot first 3 global EOFs and rotated EOFs
myEOF.sst_plot(eofs, rot_eofs, exp_var, rot_exp_var, 'SST EOFs 1-3 pacific', True)
myEOF.sst_plot(eofs, rot_eofs, exp_var, rot_exp_var, 'SST EOFs 4-6 pacific', True, plot_offset=3)

print('SST pacific EOF plot done.')

#compute EOFs and rotated EOFs
eofs, rot_eofs, exp_var, rot_exp_var = myEOF.compute_eofs_sst(data_pacific_bottom)

# plot first 3 global EOFs and rotated EOFs
myEOF.sst_plot(eofs, rot_eofs, exp_var, rot_exp_var, 'SST EOFs 1-3 northern pacific', True)
myEOF.sst_plot(eofs, rot_eofs, exp_var, rot_exp_var, 'SST EOFs 4-6 northern pacific', True, plot_offset=3)

print('SST northern pacific EOF plot done.')

#compute EOFs and rotated EOFs
eofs, rot_eofs, exp_var, rot_exp_var = myEOF.compute_eofs_sst(data_pacific_middle)

# plot first 3 global EOFs and rotated EOFs
myEOF.sst_plot(eofs, rot_eofs, exp_var, rot_exp_var, 'SST EOFs 1-3 central pacific', True)
myEOF.sst_plot(eofs, rot_eofs, exp_var, rot_exp_var, 'SST EOFs 4-6 central pacific', True, plot_offset=3)

print('SST central pacific EOF plot done.')

#compute EOFs and rotated EOFs
eofs, rot_eofs, exp_var, rot_exp_var = myEOF.compute_eofs_sst(data_pacific_top)

# plot first 3 global EOFs and rotated EOFs
myEOF.sst_plot(eofs, rot_eofs, exp_var, rot_exp_var, 'SST EOFs 1-3 southern pacific', True)
myEOF.sst_plot(eofs, rot_eofs, exp_var, rot_exp_var, 'SST EOFs 4-6 southern pacific', True, plot_offset=3)

print('SST southern pacific EOF plot done.')

#compute EOFs and rotated EOFs
eofs, rot_eofs, exp_var, rot_exp_var = myEOF.compute_eofs_sst(data_pacific_ocean)

# plot first 3 global EOFs and rotated EOFs
myEOF.sst_plot(eofs, rot_eofs, exp_var, rot_exp_var, 'SST EOFs 1-3 pacific ocean', True)
myEOF.sst_plot(eofs, rot_eofs, exp_var, rot_exp_var, 'SST EOFs 4-6 pacific ocean', True, plot_offset=3)

print('SST ocean EOF plot done.')

#compute EOFs and rotated EOFs
eofs, rot_eofs, exp_var, rot_exp_var = myEOF.compute_eofs_sst(data_pacific_midAmerica)

# plot first 3 global EOFs and rotated EOFs
myEOF.sst_plot(eofs, rot_eofs, exp_var, rot_exp_var, 'SST EOFs 1-3 middle america', True)
myEOF.sst_plot(eofs, rot_eofs, exp_var, rot_exp_var, 'SST EOFs 4-6 middle america', True, plot_offset=3)

print('SST middle american EOF plot done.')


