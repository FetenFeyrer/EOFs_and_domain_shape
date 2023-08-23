from xeofs.xarray import EOF
from xeofs.xarray import Rotator
from matplotlib.gridspec import GridSpec
from cartopy.crs import EqualEarth, PlateCarree
import matplotlib.pyplot as plt
import numpy as np
import os
import string
from matplotlib.colors import Normalize
from matplotlib.colorbar import ColorbarBase
from cartopy.crs import EqualEarth, PlateCarree, Mercator

"""
class for EOF computation with the 'xeofs' package
https://xeofs.readthedocs.io/en/latest/
"""

class myEOF:

    # self.data is a xarray data-array with dimensions 'time', 'lat', 'lon' where 'time' is the number of time samples,
    # 'lat' and 'lon' are the 2d coordinates of the measurements 
    def __init__(self, data, lon, lat, title):
        self.data = data
        self.lon = lon
        self.lat = lat
        self.title = title
        self.eofs = None
        self.explained_variances = None

    # computes the eofs of a given dataset
    # returns: eofs as xarray data-array of with dimensions 'lon', 'lat' and 'mode',
    # where 'lon' and 'lat are of same shape as data['lon'] and data['lat'] '
    # and 'mode' is the number of eofs calculated, default is the number of gridpoints in 'data' (#'lon'*#'lat')
    def compute_eofs(self, rotate=False):
        eofs, explained_variances = self._compute_eofs_internal(rotate=rotate)
        self.eofs = eofs
        self.explained_variances = explained_variances
        

    # compute eofs with the xeofs package
    def _compute_eofs_internal(self, rotate=False):
        data = self.data

        minimum_std_dev = 1e-5
        valid_x = data.stack(x=['lat', 'lon']).std('time') > minimum_std_dev
        data = data.stack(x=['lat', 'lon']).sel(x=valid_x).unstack()

        model = EOF(data, norm=True, dim=['time'])
        model.solve()
    
   
        eofs = model.eofs()
        explained_variances = model.explained_variance_ratio().values
        if rotate:
            rot_var = Rotator(model, n_rot=50, power=1)
            eofs = rot_var.eofs()
            explained_variances = rot_var.explained_variance_ratio().values
    

        self.explained_variances = np.round(explained_variances*100,4)

        
        return eofs, np.round(explained_variances*100,4)
    


    def plotEOFs(self, plot_offset=0, extent=None, is_subdomain=False, dot_size=20, is_rotated=False):
        """
        plots the first six eofs with a scatter plot

        Parameters:
        ---------
        plot_offset: int, from which EOF to start plotting
        extent: TODO
        is_subdomain: set to True, if the plot should only show the eastern hlaf of the map
        dot_size: sets the size of the plotted dots
        
        """
        directory_path = './MIGRF_EOF_plots/'

        # Check if the directory already exists
        if not os.path.exists(directory_path):
            # Create the directory
            os.makedirs(directory_path)
            print(f"Directory '{directory_path}' created.")
        else:
            print(f"Directory '{directory_path}' already exists.")

        eof_range = str(plot_offset+1)+'-'+str(plot_offset+6)


        if(is_subdomain):
            # rectangular projection
            proj = PlateCarree()
            # set extent to the left side of the world map
            extent=[-180,0,-50,50]
            if is_rotated:
                title = str('Rotated subdomain EOFs '+eof_range+': '+self.title)
            else:
                title = str('Subdomain EOFs '+eof_range+': '+self.title)
            # increase dot size
            dot_size=40
        else:
            # sphere projection
            proj = EqualEarth(central_longitude=180)
            if is_rotated:
                title = str('Rotated EOFs '+eof_range+': '+self.title)
            else:
                title = str('EOFs '+eof_range+': '+self.title)
        #proj = Mercator(central_longitude=180)
        #proj = LambertAzimuthalEqualArea(central_longitude=90, central_latitude=50)

        
        kwargs = {
            'cmap' : 'coolwarm', 'vmin' : -0.04, 'vmax': 0.04, 'transform': PlateCarree()
        }
        ### intitlialize plot layout ###
        fig = plt.figure(figsize=(12, 10))
        gs = GridSpec(3, 3, figure=fig, width_ratios=[1, 1, 0.05])
        ax0 = [fig.add_subplot(gs[i, 0], projection=proj) for i in range(3)]
        ax1 = [fig.add_subplot(gs[i, 1], projection=proj) for i in range(3)]
        # add colorbar
        ax_colorbar = fig.add_subplot(gs[:, 2]) 

        scatter_plots = []

        # Get the lowercase letters from 'a' to 'z'
        subplot_labels = list(string.ascii_lowercase)

        ### fill plots with the first six EOFs ###
        for i, (a0, a1) in enumerate(zip(ax0, ax1)):

            if extent is not None:
                a0.set_extent(extent, crs=proj)
                a1.set_extent(extent, crs=proj)
            
            mode_range = i
            scatter0 = a0.scatter(self.lon, self.lat, c=self.eofs.isel(mode=mode_range+plot_offset), s=dot_size, **kwargs)
            a0.coastlines(color='.5')
            scatter1 = a1.scatter(self.lon, self.lat, c=self.eofs.isel(mode=mode_range+3+plot_offset), s=dot_size, **kwargs)
            a1.coastlines(color='.5')

            scatter_plots.append(scatter0)
            scatter_plots.append(scatter1)

            # Add titles to each subplot
            a0.set_title('('+str(subplot_labels[i+plot_offset])+') '+f'EOF {mode_range + 1+plot_offset} - Explained variance: ~'+str(np.round(self.explained_variances[i+plot_offset],2)), fontsize=14)
            a1.set_title('('+str(subplot_labels[i+3+plot_offset])+') '+f'EOF {mode_range + 4+plot_offset} - Explained variance: ~'+str(np.round(self.explained_variances[i+3+plot_offset],2)), fontsize=14)


        
        # Add a title for the whole plot
        fig.suptitle(title, fontsize=16)



        cbar = fig.colorbar(scatter_plots[0], cax=ax_colorbar, shrink=0.6)  
        cbar.set_label('EOF coefficients')

        plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, wspace=0.1, hspace=0.1)

        plt.tight_layout()
        ## save plot as jpg in the current directory ##
        plt.savefig(f'{directory_path}{title}.jpg')
        plt.close()


    def plotEigenvalueErrorBars(explained_variances_list, N, title, ignore_first_ev=False):
        """
        Plots error bars for the first ten eigenvalues of different datasets.

        Parameters:
        ---------
        explained_variances_list : list of lists
            List of lists containing the explained variances for different datasets.
            Each inner list corresponds to the explained variances of different modes.

        """
        directory_path = './eigenvalue_error_bars/'

        # Check if the directory already exists
        if not os.path.exists(directory_path):
            # Create the directory
            os.makedirs(directory_path)
            print(f"Directory '{directory_path}' created.")
        else:
            print(f"Directory '{directory_path}' already exists.")
        num_modes = len(explained_variances_list[0])

        # Consider only the first ten modes
        num_modes_to_plot = min(num_modes, 10)
        explained_variances_list = [ev[:num_modes_to_plot] for ev in explained_variances_list]


        # Calculate mean and standard deviation for each mode across datasets
        mean_variances = np.mean(explained_variances_list, axis=0)
        std_dev_variances = np.std(explained_variances_list, axis=0)

        estimated_std_error = mean_variances * ((2/N)**0.5)

        # Convert explained variances to percentages
        mean_variances_percent = mean_variances
        std_dev_variances_percent = std_dev_variances
        estimated_std_error_percent = estimated_std_error


        # Plot error bars for each mode as horizontal lines
        plt.figure(figsize=(10, 6))
        modes = np.arange(1, num_modes_to_plot + 1)
        plt.errorbar(modes+0.1, mean_variances_percent, yerr=std_dev_variances_percent, fmt='o', capsize=5, label='Sampled Standard Deviation')

        # Plot error bars with offsets for the first ten modes as horizontal lines
        plt.errorbar(modes-0.1, mean_variances_percent, yerr=estimated_std_error_percent, fmt='o', capsize=5, label='North Standard Deviation Estimation')

        # Set x-axis labels to show the first ten modes
        plt.xticks(modes, modes)

        plt.grid(True)

        #plt.title(str(title))


    

        if ignore_first_ev:
            ylim = np.max([exp[1:] for exp in explained_variances_list])
            plt.xlim(1,11)
            plt.ylim(0,ylim+1)
            #plt.title(str(title)+' - First eigenvalue not shown')
        

        # Show the legend
        plt.legend()

        # Set plot labels and title
        plt.xlabel('Mode')
        plt.ylabel('Eigenvalue [in %]')
        

        # Show the plot
        plt.tight_layout()
        plt.savefig(f'{directory_path}{title}.jpg')
        plt.close()

    def plot_eigenvalue_sequences(sequences, title, ignore_first_ev=False):
        colors = ['red', 'blue', 'green', 'orange', 'purple', 'black', 'yellow', 'magenta']  # Define a list of colors

        directory_path = './eigenvalue_plots/'

        # Check if the directory already exists
        if not os.path.exists(directory_path):
            # Create the directory
            os.makedirs(directory_path)
            print(f"Directory '{directory_path}' created.")
        else:
            print(f"Directory '{directory_path}' already exists.")


        plt.figure(figsize=(10, 6))  # Set the figure size

        for i, sequence in enumerate(sequences):
            color = colors[i % len(colors)]  # Get a color from the list based on the index
            indices = np.arange(0, 20)  # Generate integer indices from 1 to 40
            plt.plot(indices, sequence[:20], color=color, label=f'Set: '+ str(i+1))  # Plot only the first 40 eigenvalues with integer indices

        if ignore_first_ev:
            #min_var = np.min([seq[2:20] for seq in sequences])
            min_var = 0
            max_var = np.max([seq[1:] for seq in sequences])    
        else:
            min_var = np.min([seq[:20] for seq in sequences])
            max_var = np.max(sequences)

        

        plt.xlabel('Eigenvalue Index')  # Set the x-axis label
        plt.xticks(np.arange(1, 21), [str(i+2) for i in range(20)])
        plt.yticks(np.arange(np.round(min_var-(min_var/20),2), np.round(max_var+(min_var/20),2), np.round((max_var-min_var)/20,4))) 
        plt.ylabel('Explained Variance [in %]')  # Set the y-axis label
        #plt.title('Eigenvalue Sequences - '+ str(title))  # Set the title
        if ignore_first_ev:
            plt.xlim(1,9)
            plt.ylim(0,max_var+0.2)
            title = str(title)+' - First eigenvalue not shown'
        else:
            plt.xlim(0, 11)  # Set the x-axis limits
        #plt.legend()  # Show the legend
        plt.grid(True)  # Show the grid
        plt.savefig(f'{directory_path}{title}.jpg')
        plt.close()



    
    def sst_plot(eofs, rot_eofs, exp_var, rot_exp_var, title, is_cropped=False, plot_offset=0):
        directory_path = './sst_plots/'

        # Check if the directory already exists
        if not os.path.exists(directory_path):
            # Create the directory
            os.makedirs(directory_path)
            print(f"Directory '{directory_path}' created.")
        else:
            print(f"Directory '{directory_path}' already exists.")


        if is_cropped:
            proj = Mercator(central_longitude=180)
        else:
            proj = EqualEarth(central_longitude=180)
        kwargs = {
            'levels': 30, 'cmap': 'coolwarm', 'vmin': -0.04, 'vmax': 0.04, 'transform': PlateCarree()
        }
        fig = plt.figure(figsize=(12, 10))
        gs = GridSpec(3, 3, width_ratios=[1, 1, 0.05])

        ax0 = [fig.add_subplot(gs[i, 0], projection=proj) for i in range(3)]
        ax1 = [fig.add_subplot(gs[i, 1], projection=proj) for i in range(3)]

    
        # Get the lowercase letters from 'a' to 'z'
        subplot_labels = list(string.ascii_lowercase)
        # Iterate through the subplots and add content
        for i, (a0, a1) in enumerate(zip(ax0, ax1)):
            mode_range = i + 1

            eofs.sel(mode=mode_range+plot_offset).plot.contourf(ax=a0, **kwargs, add_colorbar=False)
            a0.coastlines(color='.5')
            rot_eofs.sel(mode=mode_range+plot_offset).plot.contourf(ax=a1, **kwargs, add_colorbar=False)
            a1.coastlines(color='.5')

            
            a0.set_title('('+str(subplot_labels[i+plot_offset])+') '+f'EOF {mode_range+plot_offset} - Explained variance: ~'+str(exp_var[i+plot_offset]))
            a1.set_title('('+str(subplot_labels[i+6+plot_offset])+') '+f'Rotated EOF {mode_range+plot_offset} - Explained variance: ~'+str(rot_exp_var[i+plot_offset]))
            


        # Add a title for the whole plot
        fig.suptitle(title, fontsize=16)

        # Create a shared colorbar
        norm = Normalize(vmin=kwargs['vmin'], vmax=kwargs['vmax'])
        cax = fig.add_subplot(gs[:, 2])
        cb = ColorbarBase(cax, cmap=kwargs['cmap'], norm=norm, orientation='vertical')
        cb.set_label('EOF coefficients')  # Set your desired label

        plt.tight_layout(rect=[0, 0, 0.92, 1])
        plt.savefig(f'{directory_path}{title}.jpg')
        plt.close()



    def varimax_xeofs(model):

        rot_var = Rotator(model, n_rot=50, power=1)

        return rot_var.eofs(), rot_var.explained_variance_ratio().values
    
    def compute_eofs_sst(data, n_components=6, correlation_mode=False):


    
        model = EOF(data, norm=True, dim=['time'])
        
        model.solve()
    
        eofs = model.eofs()
        
        explained_variances = model.explained_variance_ratio().values

        pcs = model.pcs()
        #print(loadings.shape)

        #varimax rotation
        rot_eofs, rot_explained_variances = myEOF.varimax_xeofs(model)
        
        
        return eofs, rot_eofs, np.round(explained_variances*100,2), np.round(rot_explained_variances*100,2)


    