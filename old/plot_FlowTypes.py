import matplotlib.pyplot as plt
import numpy as np
import plot_isoLines as p



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