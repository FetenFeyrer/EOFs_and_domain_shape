import plot_flows as p
import compute_pca as pca
import plot_unrot_pc as pup
import numpy as np
import matplotlib.pyplot as plt


def plot_FlowTypes(sample_MeridionalFlow, sample_ZonalFlow, sample_CyclonicFlow, merged_FlowTypes):
    
    # Create a figure and axes for the plots
    fig, axs = plt.subplots(1, 4, figsize=(14, 3.5))
    fig.suptitle("Flow Type Plots")


    # Set a common color range for isolines
    vmin = np.min([sample_ZonalFlow, sample_MeridionalFlow, sample_CyclonicFlow])
    vmax = np.max([sample_ZonalFlow, sample_MeridionalFlow, sample_CyclonicFlow])

    # Plot the isolines for each flow sample dataset 
    p.plot_isoLines(sample_MeridionalFlow, axs[0], 'Meridional Flow')
    p.plot_isoLines(sample_ZonalFlow, axs[1], 'Zonal Flow')
    p.plot_isoLines(sample_CyclonicFlow, axs[2], 'Anticyclonic Flow')
    p.plot_isoLines(merged_FlowTypes, axs[3], 'Flows merged')

    plt.subplots_adjust(hspace=0.4, wspace=0.4)

    #plt.title('Isolines of Flow Data')
    plt.tight_layout()

    plt.show()


if __name__== '__main__':
    # Zonal Flow sample data
    sample_MeridionalFlow = np.array([1032, 1028, 1024, 1020, 1016, 1012,
                                1032, 1028, 1024, 1020, 1016, 1012,
                                1032, 1028, 1024, 1020, 1016, 1012,
                                1032, 1028, 1024, 1020, 1016, 1012,
                                1032, 1028, 1024, 1020, 1016, 1012,
                                1032, 1028, 1024, 1020, 1016, 1012])

    # Meridional flow sample data
    sample_ZonalFlow = np.array([1032,1032,1032,1032,1032,1032,
                                      1028,1028,1028,1028,1028,1028,
                                      1024,1024,1024,1024,1024,1024,
                                      1020,1020,1020,1020,1020,1020,
                                      1016,1016,1016,1016,1016,1016,
                                      1012,1012,1012,1012,1012,1012])

    # Cyclonic flow sample data
    sample_CyclonicFlow = np.array([1016, 1020, 1024, 1024, 1020, 1016,
                                    1020, 1024, 1028, 1028, 1024, 1020,
                                    1024, 1028, 1032, 1032, 1028, 1024,
                                    1024, 1028, 1032, 1032, 1028, 1024,
                                    1020, 1024, 1028, 1028, 1024, 1020,
                                    1016, 1020, 1024, 1024, 1020, 1016])
    
    # create a 3x36 input data matrix with the three samples
    input_matrix = np.vstack((sample_MeridionalFlow, sample_ZonalFlow, sample_CyclonicFlow))
    #print(input_matrix)
    # merge input flow types 
    merged_FlowTypes = p.merge_Datasets([sample_ZonalFlow, sample_MeridionalFlow, sample_CyclonicFlow])

    plot_FlowTypes(sample_MeridionalFlow, sample_ZonalFlow, sample_CyclonicFlow, merged_FlowTypes)

    loadings, covariance  = pca.compute_pca(input_matrix)
    
    pup.plot_PCA_loadings(loadings, covariance)
    #print(pca_result)
    