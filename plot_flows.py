import numpy as np
import matplotlib.pyplot as plt

# Input: 6x6 data matrix (np.array), the position in the subplot, and a subplot title
def plot_isoLines(dataset, ax, title):
    # reshape input sample dataset to 6x6 matrix
    dataset = dataset.reshape(6,6)
    # Create X and Y coordinates for the data points
    x = np.arange(dataset.shape[1])
    y = np.arange(dataset.shape[0])

    # Create a meshgrid of X and Y coordinates
    X, Y = np.meshgrid(x, y)

    # Set the common color range based on the minimum and maximum values
    vmin = np.min(dataset)
    vmax = np.max(dataset)
    # Plot the isolines
    contour = ax.contourf(X, Y, dataset, levels=6, extend='both', vmin=vmin, vmax=vmax)

    # Customize the plot
    ax.set_xlabel('hP')
    ax.set_title(title)
    ax.grid(True)

    # Create a separate legend with isoline colors and values
    cbar = plt.colorbar(contour, ax=ax)
    cbar.set_label('hP Value')

    # Remove tick labels from the Axes
    ax.set_xticklabels([])
    ax.set_yticklabels([])

    # Remove ticks from the Axes
    ax.tick_params(axis='both', which='both', length=0)


# Input: List of datasets to merge (same sized numpy matrices)
# 
# returns: a merged matrix of same size as input matrices with compoment wise means
def merge_Datasets(list_of_datasets):
    merged_Dataset = np.mean(list_of_datasets, axis=0)
    return merged_Dataset
