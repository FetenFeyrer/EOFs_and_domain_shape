import matplotlib.pyplot as plt
import numpy as np
import os

# Input: 6x6 data matrix (np.array), the position in the subplot, and a subplot title
def plot_isoLines(dataset, ax, levels, title):

    # reshape input sample dataset to 6x6 matrix
    dataset = dataset.reshape(6,6)
    # Create X and Y coordinates for the data points
    x = np.arange(dataset.shape[0])
    y = np.arange(dataset.shape[1])

    # Create a meshgrid of X and Y coordinates
    X, Y = np.meshgrid(x, y)

    # Set the common color range based on the minimum and maximum values
    vmin = np.min(dataset)
    vmax = np.max(dataset)

    # Flip the Y coordinates vertically
    Y = np.max(Y) - Y
    # Plot the isolines
    contour = ax.contourf(X, Y, dataset, levels=levels, extend='both', vmin=vmin, vmax=vmax)

    # Customize the plot
    #ax.set_xlabel('hP')
    ax.set_title(title)
    ax.grid(True)

    # Create a separate legend with isoline colors and values
    cbar = plt.colorbar(contour, ax=ax)
    #cbar.set_label('hP Value')

    # Remove tick labels from the Axes
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    # Remove ticks from the Axes
    ax.tick_params(axis='both', which='both', length=0)


def plot_PCA_loadings(loadings, variances, title, levels=6):
    
    # Create a figure and axes for the plots
    fig, axs = plt.subplots(1, 3, figsize=(11, 3.5))
    fig.suptitle(title)


    loadings_matrix_pc1 = loadings[0]
    loadings_matrix_pc2 = loadings[1]
    loadings_matrix_pc3 = loadings[2]
    #covariance_matrix = covariance.reshape(6,6)


    # Plot the isolines for each flow dataset
    #p.plot_isoLines(covariance, axs[0], 'Covariance Matrix')
    plot_isoLines(loadings_matrix_pc1, axs[0], levels,  'PC1, explained variance: ' + str(round(variances[0], 2)))
    plot_isoLines(loadings_matrix_pc2, axs[1], levels,  'PC2, explained variance: ' + str(round(variances[1], 2)))
    plot_isoLines(loadings_matrix_pc3, axs[2], levels, 'PC3, explained variance: ' + str(round(variances[2], 2)))
    #p.plot_isoLines(covariance, axs[4], 'Covariance matrix')

    plt.subplots_adjust(hspace=0.4, wspace=0.4)

    #plt.title('Isolines of Flow Data')
    plt.tight_layout()

    

    # Specify the directory path and file name
    directory = '~/env/imgs/'
    filename = 'img' + ' ' + title + '.png'

    # Expand the home directory path
    expanded_directory = os.path.expanduser(directory)

    # Create the directory if it does not exist
    os.makedirs(expanded_directory, exist_ok=True)
    plt.savefig(os.path.join(expanded_directory, filename))

    plt.close()
    #plt.show()