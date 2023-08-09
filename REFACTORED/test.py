from ComputeEOFs import *
from Data import *
import gridExpansion as ex
import random
import eof_plot

dataset = CorrelatedNoise(1500,10000)

dataset.create_correlated_noise_data()

dataset.plot_samples()

eofs = myEOF(dataset.data, dataset.lon, dataset.lat, dataset.title)

eofs.compute_eofs()

eofs.plotEOFs()

dataset_pacific = CorrelatedNoise(1500,10000)

dataset_pacific.create_correlated_noise_data(use_subdomain_pacific=True)

dataset_pacific.plot_samples(is_subdomain=True)

eofs = myEOF(dataset_pacific.data, dataset_pacific.lon, dataset_pacific.lat, dataset_pacific.title)

eofs.compute_eofs()

eofs.plotEOFs(is_subdomain=True)

eigenvalue_list = []
eof_list = []

'''for i in range(31):
    dataset = CorrelatedNoise(1500, 10000)

    dataset.create_correlated_noise_data(i)

    eofs = myEOF(dataset.data, dataset.lon, dataset.lat, dataset.title)

    eofs.compute_eofs()

    eof_list.append(eofs.eofs)

    eigenvalues = eofs.explained_variances.values

    eigenvalue_list.append(eigenvalues)
    print("Done: Iteration: "+ str(i))'''

'''data = xr.tutorial.open_dataset('ersstv5')['sst']

for j in range(31):

    rnd_data = []

    for i in range(52):
        
        rnd_start = random.randint(0, 612)

        data_slice = data.isel(time=slice(rnd_start, rnd_start+12))

        rnd_data.append(data_slice)    
        
        
    rnd_new_dataset = xr.concat(rnd_data, dim='time')

    #print(rnd_new_dataset)

    sst_eof = myEOF(rnd_new_dataset, rnd_new_dataset['lon'], rnd_new_dataset['lat'], ' SST EOF ')

    sst_eof.compute_eofs()

    eofs = sst_eof.eofs

    print(eofs)
    
    eof_plot.plot(eofs, eofs, 'SST EOFs - Iteration: ' + str(j))



    eigenvalues = sst_eof.explained_variances

    eigenvalue_list.append(eigenvalues)
    print('Done Iteration: ' + str(j))'''


    


'''concat_eofs = xr.concat(eof_list, dim='instances')

eof_mean = concat_eofs.mean(dim='instances')

print(eof_mean)

eofs.eofs = eof_mean
eofs.title = ' Average EOFs 1000 points'

eofs.plotEOFs()'''






#print(exp_variances_list)

#myEOF.plotEigenvalueErrorBars(explained_variances_list=eigenvalue_list)

#myEOF.plotEigenvalueErrorBarsWithOffsets(eigenvalue_list)





    






