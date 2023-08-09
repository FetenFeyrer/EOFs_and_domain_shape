from xeofs.xarray import EOF
from xeofs.xarray import Rotator
from matplotlib.gridspec import GridSpec
from cartopy.crs import EqualEarth, PlateCarree, Robinson, Mercator, LambertAzimuthalEqualArea
import matplotlib.pyplot as plt
import numpy as np

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
    def compute_eofs(self):
        eofs, explained_variances = self._compute_eofs_internal()
        self.eofs = eofs
        self.explained_variances = explained_variances
        

    # compute eofs with the xeofs package
    def _compute_eofs_internal(self):
        data = self.data

        minimum_std_dev = 1e-5
        valid_x = data.stack(x=['lat', 'lon']).std('time') > minimum_std_dev
        data = data.stack(x=['lat', 'lon']).sel(x=valid_x).unstack()

        model = EOF(data, norm=True, dim=['time'])
        model.solve()
    
   
        eofs = model.eofs()

        rot_var = Rotator(model, n_rot=50, power=1)

        rot_eofs = rot_var.eofs()
    

        explained_variances = model.explained_variance_ratio()

        
        return rot_eofs, explained_variances
    


    def plotEOFs(self, extent=None, is_subdomain=False, dot_size=20):
        """
        plots the first six eofs with a scatter plot

        Parameters:
        ---------
        extent: TODO
        is_subdomain: set to True, if the plot should only show the eastern hlaf of the map
        dot_size: sets the size of the plotted dots
        
        """
        if(is_subdomain):
            # rectangular projection
            proj = PlateCarree()
            # set extent to the left side of the world map
            extent=[-180,0,-50,50]
            title = str('ROTATED Pacific EOFs 1-6: '+self.title)
            # increase dot size
            dot_size=40
        else:
            # sphere projection
            proj = EqualEarth(central_longitude=180)
            title = str('ROTATED EOFs 1-6: '+self.title)
        #proj = Mercator(central_longitude=180)
        #proj = LambertAzimuthalEqualArea(central_longitude=90, central_latitude=50)

        
        kwargs = {
            'cmap' : 'RdBu', 'vmin' : -0.04, 'vmax': 0.04, 'transform': PlateCarree()
        }
        ### intitlialize plot layout ###
        fig = plt.figure(figsize=(12, 10))
        gs = GridSpec(3, 3, figure=fig, width_ratios=[1, 1, 0.05])
        ax0 = [fig.add_subplot(gs[i, 0], projection=proj) for i in range(3)]
        ax1 = [fig.add_subplot(gs[i, 1], projection=proj) for i in range(3)]
        # add colorbar
        ax_colorbar = fig.add_subplot(gs[:, 2]) 

        scatter_plots = []


        ### fill plots with the first six EOFs ###
        for i, (a0, a1) in enumerate(zip(ax0, ax1)):

            if extent is not None:
                a0.set_extent(extent, crs=proj)
                a1.set_extent(extent, crs=proj)
            
            mode_range = i
            scatter0 = a0.scatter(self.lon, self.lat, c=self.eofs.isel(mode=mode_range), s=dot_size, **kwargs)
            a0.coastlines(color='.5')
            scatter1 = a1.scatter(self.lon, self.lat, c=self.eofs.isel(mode=mode_range+3), s=dot_size, **kwargs)
            a1.coastlines(color='.5')

            scatter_plots.append(scatter0)
            scatter_plots.append(scatter1)

            # Add titles to each subplot
            a0.set_title(f'EOF {mode_range + 1}', fontsize=14)
            a1.set_title(f'EOF {mode_range + 4}', fontsize=14)


        
        # Add a title for the whole plot
        fig.suptitle(title, fontsize=16)



        cbar = fig.colorbar(scatter_plots[0], cax=ax_colorbar, shrink=0.6)  

        plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, wspace=0.1, hspace=0.1)

        plt.tight_layout()
        ## save plot as jpg in the current directory ##
        plt.savefig(str(title)+'.jpg')
        plt.close()


    def plotEigenvalueErrorBars(explained_variances_list):
        """
        Plots error bars for the first ten eigenvalues of different datasets.

        Parameters:
        ---------
        explained_variances_list : list of lists
            List of lists containing the explained variances for different datasets.
            Each inner list corresponds to the explained variances of different modes.

        """
        num_modes = len(explained_variances_list[0])

        # Consider only the first ten modes
        num_modes_to_plot = min(num_modes, 10)
        explained_variances_list = [ev[:num_modes_to_plot] for ev in explained_variances_list]


        # Calculate mean and standard deviation for each mode across datasets
        mean_variances = np.mean(explained_variances_list, axis=0)
        std_dev_variances = np.std(explained_variances_list, axis=0)

        estimated_std_error = mean_variances * ((2/624)**0.5)

        # Convert explained variances to percentages
        mean_variances_percent = mean_variances * 100
        std_dev_variances_percent = std_dev_variances * 100
        estimated_std_error_percent = estimated_std_error * 100


        # Plot error bars for each mode as horizontal lines
        plt.figure(figsize=(10, 6))
        modes = np.arange(1, num_modes_to_plot + 1)
        plt.errorbar(modes+0.1, mean_variances_percent, yerr=std_dev_variances_percent, fmt='o', capsize=5, label='Actual Standard Deviation')

        # Plot error bars with offsets for the first ten modes as horizontal lines
        plt.errorbar(modes-0.1, mean_variances_percent, yerr=estimated_std_error_percent, fmt='o', capsize=5, label='North Standard Deviation Estimation')

        # Set x-axis labels to show the first ten modes
        plt.xticks(modes, modes)

        plt.grid(True)

        plt.xlim(1,11)
        plt.ylim(0,10)

        # Show the legend
        plt.legend()

        # Set plot labels and title
        plt.xlabel('Mode')
        plt.ylabel('Eigenvalue')
        plt.title('SST Eigenvalue Error Bars (First 10 Modes)')

        # Show the plot
        plt.tight_layout()
        plt.savefig(str('SSTErrorBars10k_xlim.jpg'))
        plt.close()


    def plotEigenvalueErrorBarsWithOffsets(eigenvalues):
        """
        Plots error bars for eigenvalues using the specified offsets.

        Parameters:
        ---------
        offsets : list
            List of offset values for each mode to plot error bars.

        """
        num_modes = min(len(eigenvalues), 10)
        eigenvalues = [ev[:num_modes] for ev in eigenvalues]

        mean_variances = np.mean(eigenvalues, axis=0)
        estimated_std_error = mean_variances * ((2/10000)**0.5)

        # Plot error bars for each mode as horizontal lines
        plt.figure(figsize=(10, 6))
        modes = np.arange(1, num_modes + 1)
        plt.errorbar(modes, mean_variances*100, yerr=estimated_std_error*100, fmt='o', capsize=5)

        # Set x-axis labels
        plt.xticks(modes, modes)

        plt.grid(True)

        plt.xlim(2,10)

        # Set plot labels and title
        plt.xlabel('Mode')
        plt.ylabel('Eigenvalue')
        plt.title('Eigenvalue Error Bars (North standard deviation estimation)')

        # Show the plot
        plt.tight_layout()
        plt.savefig('ErrorBarsNorthEstimation.jpg')
        plt.close()

    
