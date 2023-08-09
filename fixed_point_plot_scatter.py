from matplotlib.gridspec import GridSpec
from cartopy.crs import EqualEarth, PlateCarree, Robinson, Mercator
import matplotlib.pyplot as plt

def plot(eofs, lon, lat, title, extent=None):
    #proj = EqualEarth(central_longitude=180)
    #proj = Mercator(central_longitude=180)
    #proj = EqualEarth(central_longitude=180)
    proj= PlateCarree()

    kwargs = {
         'cmap' : 'RdBu', 'vmin' : -3, 'vmax': 3, 'transform': PlateCarree()
    }
    fig = plt.figure(figsize=(12, 10))
    gs = GridSpec(3, 3, figure=fig, width_ratios=[1, 1, 0.05])
    ax0 = [fig.add_subplot(gs[i, 0], projection=proj) for i in range(3)]
    ax1 = [fig.add_subplot(gs[i, 1], projection=proj) for i in range(3)]
    ax_colorbar = fig.add_subplot(gs[:, 2]) 

    scatter_plots = []

    #print(eofs[1])
    for i, (a0, a1) in enumerate(zip(ax0, ax1)):

        if extent is not None:
            a0.set_extent(extent, crs=proj)
            a1.set_extent(extent, crs=proj)

        mode_range = i
    
        scatter0 = a0.scatter(lon, lat, c=eofs.isel(mode=mode_range), s=40, **kwargs)
        a0.coastlines(color='.5')
        scatter1 = a1.scatter(lon, lat, c=eofs.isel(mode=mode_range+3), s=40, **kwargs)
        a1.coastlines(color='.5')

        scatter_plots.append(scatter0)
        scatter_plots.append(scatter1)

        # Add titles to each subplot
        a0.set_title(f'Time sample {mode_range + 1}', fontsize=14)
        a1.set_title(f'Time sample {mode_range + 4}', fontsize=14)

    # Add a title for the whole plot
    fig.suptitle(title, fontsize=16)



    cbar = fig.colorbar(scatter_plots[0], cax=ax_colorbar, shrink=0.6)  
    cbar.set_label('anomaly')

    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, wspace=0.1, hspace=0.1)

    plt.tight_layout()
    plt.savefig('/Users/julianfeyrer/Documents/GitHub/EOFs_and_domain_shape/scatterImgs/fix_points/'+str(title)+'.jpg')
    plt.close()