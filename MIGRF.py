from ComputeEOFs import *
from Data import *


######## Uncorrelated noise data set ########
dataset = CorrelatedNoise(1500,10000)

dataset.create_correlated_noise_data(is_uncorrelated=True)

dataset.plot_samples()

eofs = myEOF(dataset.data, dataset.lon, dataset.lat, dataset.title)

eofs.compute_eofs()

eofs.plotEOFs()

print('Uncorrelated noise plot done.')

######## Correlated noise data set l=0.05, v=1.5, 10000 samples ########

dataset = CorrelatedNoise(1500,10000)

dataset.create_correlated_noise_data(l=0.05)

dataset.plot_samples()

eofs = myEOF(dataset.data, dataset.lon, dataset.lat, dataset.title)

eofs.compute_eofs()

eofs.plotEOFs()
eofs.plotEOFs(plot_offset=6)

eofs.compute_eofs(rotate=True)

eofs.plotEOFs(is_rotated=True)

print('Correlated noise data set l=0.05, v=1.5, 100000 samples plot done.')

######## Correlated noise data set l=0.1, v=1.5, 10000 samples ########

dataset = CorrelatedNoise(1500,10000)

dataset.create_correlated_noise_data(l=0.1)

dataset.plot_samples()

eofs = myEOF(dataset.data, dataset.lon, dataset.lat, dataset.title)

eofs.compute_eofs()

eofs.plotEOFs()
eofs.plotEOFs(plot_offset=6)

eofs.compute_eofs(rotate=True)

eofs.plotEOFs(is_rotated=True)

print('Correlated noise data set l=0.1, v=1.5, 10000 samples plot done.')

######## Correlated noise data set l=0.2, v=1.5, 10000 samples ########

dataset = CorrelatedNoise(1500,10000)

dataset.create_correlated_noise_data()

dataset.plot_samples()

eofs = myEOF(dataset.data, dataset.lon, dataset.lat, dataset.title)

eofs.compute_eofs()

eofs.plotEOFs()
eofs.plotEOFs(plot_offset=6)

eofs.compute_eofs(rotate=True)

eofs.plotEOFs(is_rotated=True)

print('Correlated noise data set l=0.2, v=1.5, 10000 samples plot done.')




######## Correlated noise data set ractangular subdomain l=0.05, v=1.5, 10000 samples ########

dataset_pacific = CorrelatedNoise(1500,10000)

dataset_pacific.create_correlated_noise_data(l=0.2, use_subdomain_pacific=True)

dataset_pacific.plot_samples(is_subdomain=True)

eofs = myEOF(dataset_pacific.data, dataset_pacific.lon, dataset_pacific.lat, dataset_pacific.title)

eofs.compute_eofs()

eofs.plotEOFs(is_subdomain=True)
eofs.plotEOFs(is_subdomain=True, plot_offset=6)

eofs.compute_eofs(rotate=True)

eofs.plotEOFs(is_rotated=True, is_subdomain=True)

print('Correlated noise data set subdomain l=0.2, v=1.5, 10000 samples plot done.')

######## Correlated noise data set ractangular subdomain l=0.2, v=1.5, 1000 samples ########

dataset_pacific = CorrelatedNoise(1500,1000)

dataset_pacific.create_correlated_noise_data(use_subdomain_pacific=True)

dataset_pacific.plot_samples(is_subdomain=True)

eofs = myEOF(dataset_pacific.data, dataset_pacific.lon, dataset_pacific.lat, dataset_pacific.title)

eofs.compute_eofs()

eofs.plotEOFs(is_subdomain=True)
eofs.plotEOFs(is_subdomain=True, plot_offset=6)

eofs.compute_eofs(rotate=True)

eofs.plotEOFs(is_rotated=True, is_subdomain=True)

print('Correlated noise data set subdomain l=0.2, v=1.5, 1000 samples plot done.')

   #### plot eigenvalue error bars from 30 ralisations of the MIGRF #####
def plotEigenvalueSequencesAndErrorBars(length_scale=0.2, is_subdomain=False, is_uncorrelated=False):
    eigenvalue_list = []
    eof_list = []


    for i in range(31):
        dataset = CorrelatedNoise(1500, 10000)

        dataset.create_correlated_noise_data(seed_offset=i, l=length_scale, use_subdomain_pacific=is_subdomain, is_uncorrelated=True)

        eofs = myEOF(dataset.data, dataset.lon, dataset.lat, dataset.title)

        eofs.compute_eofs()

        eof_list.append(eofs.eofs)

        eigenvalues = eofs.explained_variances


        eigenvalue_list.append(eigenvalues)
        print("MIGRF eigenvalue error bar computation - Done: Iteration: "+ str(i))

    if is_subdomain:
        title_seq='Subdomain eigenvalue sequences l='+str(length_scale)
        title_err='Subdomain eigenvalue error bars - MIGRF l='+str(length_scale)
    elif is_uncorrelated:
        title_seq='Uncorrelated eigenvalue sequences'
        title_err='Uncorrelated eigenvalue error bars - MIGRF'
    else:
        title_seq='Eigenvalue sequences l='+str(length_scale)
        title_err='Eigenvalue error bars - MIGRF l='+str(length_scale)

    myEOF.plotEigenvalueErrorBars(explained_variances_list=eigenvalue_list, N=10000, title=title_err)
    myEOF.plot_eigenvalue_sequences(eigenvalue_list, title_seq)

    print("MIGRF eigenvalue error bar plot and eigenvalue sequence plot done.")

     ##### average EOFs of 30 realisations of the MIGRF ######

    concat_eofs = xr.concat(eof_list, dim='instances')

    eof_mean = concat_eofs.mean(dim='instances')

    eofs.eofs = eof_mean
    eofs.title = ' Average EOFs l='+str(length_scale)

    eofs.plotEOFs(is_subdomain=is_subdomain)

    print("MIGRF average EOFs plot done.")


plotEigenvalueSequencesAndErrorBars(length_scale=0.05)
plotEigenvalueSequencesAndErrorBars(length_scale=0.1)
plotEigenvalueSequencesAndErrorBars()
plotEigenvalueSequencesAndErrorBars(is_subdomain=True)
plotEigenvalueSequencesAndErrorBars(is_uncorrelated=True)
















    






