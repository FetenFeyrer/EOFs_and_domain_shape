
import plot_pc as pup
import reflect_by_x as refl
import add_noise as ns
import center_matrix as c
import compute_pca_xeofs as xeofs
import numpy as np

def main(data_matrix, title, noise_level):

    # Add gaussian noise
    data_matrix = ns.add_gaussian_noise(data_matrix, 0, noise_level)
    data_matrix = c.center_matrix(data_matrix)

    # Compute eofs and varimax rotated eofs
    cov_pcs, cov_eofs, rot_cov_eofs, cov_exp_var, rot_cov_exp_var = xeofs.compute_pca(data_matrix)
    cor_pcs, cor_eofs, rot_cor_eofs, cor_exp_var, rot_cor_exp_var = xeofs.compute_pca(data_matrix, correlation_mode=True)


    ##### PLOT #####
    pup.plot_PCA_loadings(cov_eofs, cov_exp_var, 'Covariance PCA ' + str(title) + ' noise-level: ' + str(noise_level))
    pup.plot_PCA_loadings(rot_cov_eofs, rot_cov_exp_var, 'Covariance rotated PCA ' + str(title) + ' noise-level: ' + str(noise_level), 20)
    pup.plot_PCA_loadings(cor_eofs, cor_exp_var, 'Correlation PCA ' + str(title) + ' noise-level: ' + str(noise_level), 20)
    pup.plot_PCA_loadings(rot_cor_eofs, rot_cor_exp_var, 'Correlation rotated PCA ' + str(title) + ' noise-level: ' + str(noise_level), 20)


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


    ####### PLASMODE 5 #########

    GGGx6 = np.tile(sample_direct_ZonalFlow_flip, (6,1))
    HHHx6 = np.tile(sample_inverse_ZonalFlow_flip, (6,1))
    IIIx3 = np.tile(sample_direct_MeridionalFlow, (3,1))
    JJJx3 = np.tile(sample_inverse_MeridionalFlow, (3,1))
    KKKx9 = np.tile(sample_direct_CyclonicFlow_flip, (9,1))
    LLLx9 = np.tile(sample_inverse_CyclonicFlow_flip, (9,1))

    input_matrix_mode5 = np.vstack((GGGx6, HHHx6, IIIx3, JJJx3, KKKx9, LLLx9))
    
    
    #plot_FlowTypes(sample_direct_MeridionalFlow, sample_direct_ZonalFlow, sample_direct_CyclonicFlow)
    
    
    #for i in np.arange(0.093,0.100,0.001):
        #i = i/10.0
    main(input_matrix_mode1, 'Plasmode 1', 1)
    main(input_matrix_mode2, 'Plasmode 2', 1)
    main(input_matrix_mode4, 'Plasmode 4', 1)
    main(input_matrix_mode5, 'Plasmode 5', 1)
    
    
    
    
    
