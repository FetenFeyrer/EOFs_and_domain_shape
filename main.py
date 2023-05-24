
import compute_pca as pca
import plot_pc as pup
import reflect_by_x as refl
import add_noise as ns
import center_matrix as c
import varimax_rotation as rot
import FactorAnalyzerVarimax as rot_alt

import numpy as np
import matplotlib.pyplot as plt

def main(data_matrix, title, noise_level):
    data_matrix_T = data_matrix.T

    data_matrix = ns.add_gaussian_noise(data_matrix, 0, noise_level)
    data_matrix = c.center_matrix(data_matrix)

    data_matrix_T = ns.add_gaussian_noise(data_matrix_T, 0, noise_level)
    data_matrix_T = c.center_matrix(data_matrix_T)

    cov_loadings_S, cov_scores_S, cov_exp_var_S = pca.compute_pca(data_matrix)
    cor_loadings_S, cor_scores_S, cor_exp_var_S = pca.compute_pca(data_matrix, correlation_mode=True)

    cov_loadings_T, cov_scores_T, cov_exp_var_T = pca.compute_pca(data_matrix_T)
    cor_loadings_T, cor_scores_T, cor_exp_var_T = pca.compute_pca(data_matrix_T, correlation_mode=True)

    rotated_cov_loadings_S = rot.varimax(cov_loadings_S[:3].T)
    rotated_cor_loadings_S = rot.varimax(cor_loadings_S[:3].T)

    rotated_cov_scores_T = rot.varimax(cov_scores_T[:3].T)
    rotated_cor_scores_T = rot.varimax(cor_scores_T[:3].T)

    a, b, rot_cov_exp_var_S = pca.compute_pca(rotated_cov_loadings_S, 3)
    a, b, rot_cor_exp_var_S = pca.compute_pca(rotated_cor_loadings_S, 3, True)

    a, b, rot_cov_exp_var_T = pca.compute_pca(rotated_cov_scores_T, 3)
    a, b, rot_cor_exp_var_T = pca.compute_pca(rotated_cor_scores_T, 3, True)

    pup.plot_PCA_loadings(cov_loadings_S, cov_exp_var_S, 'S-Mode Covariance PCA ' + str(title) + ' noise-level: ' + str(noise_level))
    pup.plot_PCA_loadings(rotated_cov_loadings_S.T, rot_cov_exp_var_S, 'S-Mode Covariance rotated PCA ' + str(title) + ' noise-level: ' + str(noise_level))

    pup.plot_PCA_loadings(cor_loadings_S, cor_exp_var_S, 'S-Mode Correlation PCA ' + str(title) + ' noise-level: ' + str(noise_level), 20)
    pup.plot_PCA_loadings(rotated_cor_loadings_S.T, rot_cor_exp_var_S, 'S-Mode Correlation rotated PCA ' + str(title) + ' noise-level: ' + str(noise_level), 20)

    pup.plot_PCA_loadings(cov_scores_T, cov_exp_var_T, 'T-Mode Covariance PCA ' + str(title) + ' noise-level: ' + str(noise_level))
    pup.plot_PCA_loadings(rotated_cov_scores_T.T, rot_cov_exp_var_T, 'T-Mode Covariance rotated PCA ' + str(title) + ' noise-level: ' + str(noise_level))

    pup.plot_PCA_loadings(cor_scores_T, cor_exp_var_T, 'T-Mode Correlation PCA ' + str(title) + ' noise-level: ' + str(noise_level), 20)
    pup.plot_PCA_loadings(rotated_cor_scores_T.T, rot_cor_exp_var_T, 'T-Mode Correlation rotated PCA ' + str(title) + ' noise-level: ' + str(noise_level))

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

    
    ####### PLASMODE 2 ########
    
    GGGGGG = np.tile(sample_direct_ZonalFlow_flip, (6,1))
    HHHHHH = np.tile(sample_inverse_ZonalFlow_flip, (6,1))
    KKKKKK = np.tile(sample_direct_CyclonicFlow_flip, (6,1))
    LLLLLL = np.tile(sample_inverse_CyclonicFlow_flip, (6,1))


    input_matrix_mode2 = np.vstack((GGGGGG,HHHHHH,AAAAAA,BBBBBB,KKKKKK,LLLLLL))
   
    ####### PLASMODE 4 ########
    
    GGGx10 = np.tile(sample_direct_ZonalFlow_flip, (10,1))
    HHHx10 = np.tile(sample_inverse_ZonalFlow_flip, (10,1))
    IIIx5 = np.tile(sample_direct_MeridionalFlow, (5,1))
    JJJx5 = np.tile(sample_inverse_MeridionalFlow, (5,1))
    KKKx3 = np.tile(sample_direct_CyclonicFlow_flip, (3,1))
    LLLx3 = np.tile(sample_inverse_CyclonicFlow_flip, (3,1))


    input_matrix_mode4 = np.vstack((GGGx10,HHHx10,IIIx5,JJJx5,KKKx3,LLLx3))
    
    ##########################
    #          PLOT         #
    ##########################
    
    #plot_FlowTypes(sample_direct_MeridionalFlow, sample_direct_ZonalFlow, sample_direct_CyclonicFlow)
    
    main(input_matrix_mode1, 'Plasmode 1', 1)
    main(input_matrix_mode2, 'Plasmode 2', 3)
    main(input_matrix_mode4, 'Plasmode 4', 1)
