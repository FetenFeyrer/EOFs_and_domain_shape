from climnet.myutils import *
from climnet.grid import FeketeGrid
from sklearn.gaussian_process.kernels import Matern
import numpy as np
from matplotlib.gridspec import GridSpec
from cartopy.crs import EqualEarth, PlateCarree
import matplotlib.pyplot as plt

"""
class to create a time series dataset with correlated noise on an isotropic random field using the climent package
https://github.com/moritzhaas/climate_nets_from_random_fields/tree/main

"""

class CorrelatedNoise:


    ## constructor ## 
    def __init__(self, num_points, num_timepoints):
        self.data = None
        self.num_points = num_points
        self.num_timepoints = num_timepoints
        self.lon = None
        self.lat = None
        self.title = None


        
    def create_correlated_noise_data(self, l=0.2, v=1.5, seed_offset=0, is_uncorrelated=False, is_autocorrelated=False, use_subdomain_pacific=False):
        """ 
        create a dataset with correlated noise

        Parameters:
        ----------
        :param seed_offset: offset to create different instances of correlated noise on a grid -- change offset to get a new random instance of correlated noise on a grid
        :type seed_offset: int64
        :param is_uncorrated: set to True to obtain completely uncorrelated noise
        :type is_uncorrelated: bool
        :param is_autocorrelated: set to True to add autocorrelation to the dataset  
        :type isautocorrelated: bool   
        :return: data: the created dataset of correlated noise, lon, lat: the corrdinates of the grid for plotting 
        """
        
        # initialise the grid
        grid = FeketeGrid(num_points=self.num_points, num_iter=1000)

        # if set to 'True', the grid is cut to the eastern region of the world map
        if(use_subdomain_pacific):
            lat_range = [-50,49]  # Specify the desired latitude range (-30 to 30 degrees)
            lon_range = [-366,1] # Specify the desired longitude range (120 to 280 degrees)

            cutted_grid = grid.cut_grid(lat_range, lon_range)
        
            lon, lat = cutted_grid['lon'], cutted_grid['lat']

            ## TODO: remove hardcoding
            self.num_points = 575
        else:
            lon, lat = grid.grid['lon'], grid.grid['lat']


    
        # convert spherical coordinated to cartesian coordinates
        cartesian_grid = spherical2cartesian(lon,lat)

        # if set to 'True' there is autocorrelation infused into the data, else theres no autocorrelation
        if (is_autocorrelated):
            ar_coeff = 0.9 * np.ones(self.num_points)
        else:
            ar_coeff = np.zeros(self.num_points)

        # initialise the Kernel for inducing spatial correlation
        kernel = 1.0 * Matern(length_scale=l, nu=v, )
        cov = kernel(cartesian_grid)
        # if the data should be completely uncorrelated, the cov-matrix is a identity matrix
        if(is_uncorrelated):
            cov = np.eye(self.num_points)

        np.random.seed(18360-seed_offset)
        data = diag_var_process(ar_coeff, cov, n_time=self.num_timepoints)


        ## set titles for different modes
        if(is_uncorrelated):
            title= 'Uncorrelated noise \n(points: '+str(self.num_points)+', timepoints: '+str(self.num_timepoints)+')'
            np.savetxt(title+'.txt', data)
        elif(is_autocorrelated):
            title= 'Auto- and spatial correlated noise \n(points: '+str(self.num_points)+', timepoints: '+str(self.num_timepoints)+', length-scale='+str(l)+', smoothness-scale='+str(v)+')'
            np.savetxt(title+'.txt', data)
        else:
            title= 'Spatial correlated noise \n(points: '+str(self.num_points)+', timepoints: '+str(self.num_timepoints)+', length-scale='+str(l)+', smoothness-scale='+str(v)+')'
            np.savetxt(title+'.txt', data)


        # convert data back to a xarray data-array for further processing
        data_xr = self.construct_xarray(data, title)

        self.data = data_xr
        self.lon = lon
        self.lat = lat
        self.title = title
    


    def find_integers_within_ratio_range(self, input_number, target_ratio= 3/5, tolerance=0.1):
        """
        compute two numbers that result in the input number when multiplied, having a estimated ratio of 3/5
        
        Parameters:
        --------
        input_number: the input number to calculate the factors for
        target_ratio: the ratio the factors should have
        toleance: the tolerance for the ratio
        
        return: [x,y] the factors or Exception if no numbers within the tolerance are found
        """
        for x in range(1, input_number + 1):
            for y in range(1, input_number + 1):
                if abs(x / y - target_ratio) <= tolerance and x * y == input_number:
                    return x, y
        raise Exception('number of gridpoints cannot be properly calculated: possible numbers e.g. 1500, 570,...')


    def construct_xarray(self, data, title='data'):
        """
        construct an xarray data array of the given input np.array

        Parameters:
        --------
        data: np.array (eofs) to convert: (features, eofs)
        lats: number of lat points
        lons: number of lon points
        title: title for the created xarray

        return: the created xarray data-array containing the input data
        """
        lats,lons = self.find_integers_within_ratio_range(self.num_points)
        
        data = data.reshape(self.num_timepoints,lats,lons)
        
        n_time_samples = data.shape[0]
        

        lat = np.linspace(87, -87, lats)
        lon = np.linspace(0, 357, lons)
        time = np.arange(1, n_time_samples+1, dtype=np.int64)

        # Create the attributes for the new Xarray data array
        attributes = {
            'long_name': title,
            'units': 'int64',
            'description': ' input_dataset'
        }

        # Create the new Xarray data array
        data_xr = xr.DataArray(
            data,
            dims=('time', 'lat', 'lon'),
            coords={'lat': lat, 'lon': lon, 'time': time},
            attrs=attributes,
        )

        data_xr['lat'] = data_xr['lat'].astype(np.float32)
        data_xr['lon'] = data_xr['lon'].astype(np.float32)
        
        return data_xr
   
    def plot_samples(self, is_subdomain=False, extent=None, dot_size=20):
        """
        plot fixed time point samples of a dataset

        Parameters:
        --------
        is_subdomain: set to True if the dataset is the pacific subdomain
        dot_size: set the size of the plotted dots
        
        """
        if (is_subdomain):
            proj = PlateCarree()
            extent=[-180,0,-50,50]
            title = 'Pacific '+str(self.title)
            dot_size=40
        else:
            proj = EqualEarth(central_longitude=180)
            title = self.title
        #proj = Mercator(central_longitude=180)
        #proj = LambertAzimuthalEqualArea(central_longitude=90, central_latitude=50)

        
        kwargs = {
            'cmap' : 'RdBu', 'vmin' : -3, 'vmax': 3, 'transform': PlateCarree()
        }
        fig = plt.figure(figsize=(12, 10))
        gs = GridSpec(3, 3, figure=fig, width_ratios=[1, 1, 0.05])
        ax0 = [fig.add_subplot(gs[i, 0], projection=proj) for i in range(3)]
        ax1 = [fig.add_subplot(gs[i, 1], projection=proj) for i in range(3)]
        ax_colorbar = fig.add_subplot(gs[:, 2]) 

        scatter_plots = []

        for i, (a0, a1) in enumerate(zip(ax0, ax1)):

            if extent is not None:
                a0.set_extent(extent, crs=proj)
                a1.set_extent(extent, crs=proj)
            
            mode_range = i
            scatter0 = a0.scatter(self.lon, self.lat, c=self.data.isel(time=mode_range), s=dot_size, **kwargs)
            a0.coastlines(color='.5')
            scatter1 = a1.scatter(self.lon, self.lat, c=self.data.isel(time=mode_range+3), s=dot_size, **kwargs)
            a1.coastlines(color='.5')

            scatter_plots.append(scatter0)
            scatter_plots.append(scatter1)

            # Add titles to each subplot
            a0.set_title(f'Time sample {mode_range + 1}', fontsize=14)
            a1.set_title(f'Time sample {mode_range + 4}', fontsize=14)

        # Add a title for the whole plot
        fig.suptitle(title, fontsize=16)



        cbar = fig.colorbar(scatter_plots[0], cax=ax_colorbar, shrink=0.6)  

        plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, wspace=0.1, hspace=0.1)

        plt.tight_layout()
        plt.savefig(str(title)+'.jpg')
        plt.close()
    




    