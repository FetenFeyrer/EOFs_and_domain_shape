import plot_flows as p
import compute_pca as pca
import plot_unrot_pc as pup
import reflect_by_x as refl
import add_noise as ns
import center_matrix as c

import numpy as np
import matplotlib.pyplot as plt


def plot_FlowTypes(sample_MeridionalFlow, sample_ZonalFlow, sample_CyclonicFlow):
    
    # Create a figure and axes for the plots
    fig, axs = plt.subplots(1, 3, figsize=(11, 3.5))
    fig.suptitle("Flow Type Plots")


    # Set a common color range for isolines
    vmin = np.min([sample_MeridionalFlow, sample_ZonalFlow, sample_CyclonicFlow])
    vmax = np.max([sample_MeridionalFlow, sample_ZonalFlow, sample_CyclonicFlow])

    # Plot the isolines for each flow sample dataset 
    p.plot_isoLines(sample_MeridionalFlow, axs[0], 'Meridional Flow')
    p.plot_isoLines(sample_ZonalFlow, axs[1], 'Zonal Flow')
    p.plot_isoLines(sample_CyclonicFlow, axs[2], 'Cyclonic Flow')

    plt.subplots_adjust(hspace=0.4, wspace=0.4)

    #plt.title('Isolines of Flow Data')
    plt.tight_layout()

    plt.show()


if __name__== '__main__':
    # Meridional Flow sample data
    sample_inverse_MeridionalFlow = np.array([1032, 1028, 1024, 1020, 1016, 1012,
                                            1032, 1028, 1024, 1020, 1016, 1012,
                                            1032, 1028, 1024, 1020, 1016, 1012,
                                            1032, 1028, 1024, 1020, 1016, 1012,
                                            1032, 1028, 1024, 1020, 1016, 1012,
                                            1032, 1028, 1024, 1020, 1016, 1012])

    sample_direct_MeridionalFlow = refl.reflect_by_x(sample_inverse_MeridionalFlow, 1012)
    
    # Zonal flow sample data
    sample_direct_ZonalFlow = np.array([1012,1012,1012,1012,1012,1012,
                                        1016,1016,1016,1016,1016,1016,
                                        1020,1020,1020,1020,1020,1020,
                                        1024,1024,1024,1024,1024,1024,
                                        1028,1028,1028,1028,1028,1028,
                                        1032,1032,1032,1032,1032,1032])
    
    
    sample_inverse_ZonalFlow = refl.reflect_by_x(sample_direct_ZonalFlow, 1012)

    sample_inverse_ZonalFlow_flip = np.array([1032,1032,1032,1032,1032,1032,
                                        1028,1028,1028,1028,1028,1028,
                                        1024,1024,1024,1024,1024,1024,
                                        1020,1020,1020,1020,1020,1020,
                                        1016,1016,1016,1016,1016,1016,
                                        1012,1012,1012,1012,1012,1012])
    
    
    sample_direct_ZonalFlow_flip = refl.reflect_by_x(sample_inverse_ZonalFlow_flip, 1012)

    # Cyclonic flow sample data
    sample_inverse_CyclonicFlow = np.array([1016, 1020, 1024, 1024, 1020, 1016,
                                    1020, 1024, 1028, 1028, 1024, 1020,
                                    1024, 1028, 1032, 1032, 1028, 1024,
                                    1024, 1028, 1032, 1032, 1028, 1024,
                                    1020, 1024, 1028, 1028, 1024, 1020,
                                    1016, 1020, 1024, 1024, 1020, 1016])
    
    sample_direct_CyclonicFlow = refl.reflect_by_x(sample_inverse_CyclonicFlow, 1012)

    sample_direct_CyclonicFlow_flip = np.array([1032, 1028, 1024, 1024, 1028, 1032,
                                                1028, 1024, 1020, 1020, 1024, 1028,
                                                1024, 1020, 1016, 1016, 1020, 1024,
                                                1024, 1020, 1016, 1016, 1020, 1024,
                                                1028, 1024, 1020, 1020, 1024, 1028,
                                                1032, 1028, 1024, 1024, 1028, 1032])
    

    sample_inverse_CyclonicFlow_flip = refl.reflect_by_x(sample_direct_CyclonicFlow_flip, 1012)
   

   

    # building the input data matrix for the artificial flow behaviour in S-Mode
    # A = meridional, B = inverse meridional, C = zonal, D = inverse Zonal, E = cyclonic, F = inverse cyclonic
    # sequence composition: AAAAAA BBBBBB CCCCCC DDDDDD EEEEEE FFFFFF
    
    
    ####### PLASMODE 1 ########

    AAAAAA = np.tile(sample_direct_MeridionalFlow, (6,1))
    BBBBBB = np.tile(sample_inverse_MeridionalFlow, (6,1))
    CCCCCC = np.tile(sample_direct_ZonalFlow, (6,1))
    DDDDDD = np.tile(sample_inverse_ZonalFlow, (6,1))
    
    EEEEEE = np.tile(sample_direct_CyclonicFlow, (6,1))
    FFFFFF = np.tile(sample_inverse_CyclonicFlow, (6,1))
    

    input_matrix_mode1 = np.vstack((AAAAAA,BBBBBB,CCCCCC,DDDDDD,EEEEEE,FFFFFF))
    input_matrix_mode1 = ns.add_gaussian_noise(input_matrix_mode1, 0, 1)
    
    input_matrix_mode1 = c.center_matrix(input_matrix_mode1)
    cov_loadings_mode1= pca.compute_pca(input_matrix_mode1)
    cor_loadings_mode1= pca.compute_pca(input_matrix_mode1, correlation_mode=True)




    
    
    ####### PLASMODE 2 ########
    
    
    GGGGGG = np.tile(sample_direct_ZonalFlow_flip, (6,1))
    HHHHHH = np.tile(sample_inverse_ZonalFlow_flip, (6,1))
    KKKKKK = np.tile(sample_direct_CyclonicFlow_flip, (6,1))
    LLLLLL = np.tile(sample_inverse_CyclonicFlow_flip, (6,1))


    input_matrix_mode2 = np.vstack((GGGGGG,HHHHHH,AAAAAA,BBBBBB,KKKKKK,LLLLLL))
    input_matrix_mode2 = ns.add_gaussian_noise(input_matrix_mode2, 0, 3)
    
    input_matrix_mode2 = c.center_matrix(input_matrix_mode2)
    
    cov_loadings_mode2= pca.compute_pca(input_matrix_mode2)
    cor_loadings_mode2= pca.compute_pca(input_matrix_mode2, correlation_mode=True)


    ####### PLASMODE 4 ########

    GGGx10 = np.tile(sample_direct_ZonalFlow_flip, (10,1))
    HHHx10 = np.tile(sample_inverse_ZonalFlow_flip, (10,1))
    IIIx5 = np.tile(sample_direct_MeridionalFlow, (5,1))
    JJJx5 = np.tile(sample_inverse_MeridionalFlow, (5,1))
    KKKx3 = np.tile(sample_direct_CyclonicFlow_flip, (3,1))
    LLLx3 = np.tile(sample_inverse_CyclonicFlow_flip, (3,1))


    input_matrix_mode4 = np.vstack((GGGx10,HHHx10,IIIx5,JJJx5,KKKx3,LLLx3))
    input_matrix_mode4 = ns.add_gaussian_noise(input_matrix_mode4, 0, 3)

    cov_loadings_mode4= pca.compute_pca(input_matrix_mode4)
    cor_loadings_mode4= pca.compute_pca(input_matrix_mode4, correlation_mode=True)
    
    
    ##########################
    #          PLOT         #
    ##########################

    #plot_FlowTypes(sample_direct_MeridionalFlow, sample_direct_ZonalFlow, sample_direct_CyclonicFlow)
    pup.plot_PCA_loadings(cov_loadings_mode1, 'Covariance PCA Plasmode 1 (Meridional-Zonal-Cyclonic) low noise')
    pup.plot_PCA_loadings(cor_loadings_mode1, 'Correlation PCA Plasmode 1 (Meridional-Zonal-Cyclonic) low noise', 20)

    pup.plot_PCA_loadings(cov_loadings_mode2, 'Covariance PCA Plasmode 2 (Zonal-Meridional-Cyclonic) high noise')
    pup.plot_PCA_loadings(cor_loadings_mode2, 'Correlation PCA Plasmode 2 (Zonal-Meridional-Cyclonic) high noise', 20)

    pup.plot_PCA_loadings(cov_loadings_mode4, 'Covariance PCA Plasmode 4 (Zonal-Meridional-Cyclonic) high noise')
    pup.plot_PCA_loadings(cor_loadings_mode4, 'Correlation PCA Plasmode 4 (Zonal-Meridional-Cyclonic) high noise', 20)

  