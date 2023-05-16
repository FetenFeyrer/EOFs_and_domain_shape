import matplotlib.pyplot as plt
import numpy as np
import plot_flows as p

def plot_PCA_loadings(loadings, covariance):
    
    # Create a figure and axes for the plots
    fig, axs = plt.subplots(1, 4, figsize=(14, 3.5))
    fig.suptitle("PCA loadings Plots")


    loadings_matrix_pc1 = loadings[0].reshape(6,6)
    loadings_matrix_pc2 = loadings[1].reshape(6,6)
    loadings_matrix_pc3 = loadings[2].reshape(6,6)


    # Plot the isolines for each flow dataset
    #p.plot_isoLines(covariance, axs[0], 'Covariance Matrix')
    p.plot_isoLines(loadings_matrix_pc1, axs[0], 'PC1')
    p.plot_isoLines(loadings_matrix_pc2, axs[1], 'PC2')
    p.plot_isoLines(loadings_matrix_pc3, axs[2], 'PC3')

    plt.subplots_adjust(hspace=0.4, wspace=0.4)

    #plt.title('Isolines of Flow Data')
    plt.tight_layout()

    plt.show()