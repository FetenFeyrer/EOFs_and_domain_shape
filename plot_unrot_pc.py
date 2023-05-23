import matplotlib.pyplot as plt
import numpy as np
import plot_isoLines as p

def plot_PCA_loadings(loadings, title, levels=6):
    
    # Create a figure and axes for the plots
    fig, axs = plt.subplots(1, 3, figsize=(11, 3.5))
    fig.suptitle(title)


    loadings_matrix_pc1 = loadings[0]
    loadings_matrix_pc2 = loadings[1]
    loadings_matrix_pc3 = loadings[2]
    #covariance_matrix = covariance.reshape(6,6)


    # Plot the isolines for each flow dataset
    #p.plot_isoLines(covariance, axs[0], 'Covariance Matrix')
    p.plot_isoLines(loadings_matrix_pc1, axs[0], levels,  'PC1')
    p.plot_isoLines(loadings_matrix_pc2, axs[1], levels,  'PC2')
    p.plot_isoLines(loadings_matrix_pc3, axs[2], levels, 'PC3')
    #p.plot_isoLines(covariance, axs[4], 'Covariance matrix')

    plt.subplots_adjust(hspace=0.4, wspace=0.4)

    #plt.title('Isolines of Flow Data')
    plt.tight_layout()

    plt.show()