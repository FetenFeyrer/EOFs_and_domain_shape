from matplotlib.gridspec import GridSpec
from cartopy.crs import EqualEarth, PlateCarree, Robinson, Mercator
import matplotlib.pyplot as plt

def plot(eofs, lon, lat, title):
    #proj = EqualEarth(central_longitude=180)
    #proj = PlateCarree(central_longitude=180)
    proj = EqualEarth(central_longitude=180)

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
        mode_range = i
        scatter0 = a0.scatter(lon, lat, c=eofs.isel(mode=mode_range), s=20, **kwargs)
        a0.coastlines(color='.5')
        scatter1 = a1.scatter(lon, lat, c=eofs.isel(mode=mode_range+3), s=20, **kwargs)
        a1.coastlines(color='.5')

        scatter_plots.append(scatter0)
        scatter_plots.append(scatter1)



    cbar = fig.colorbar(scatter_plots[0], cax=ax_colorbar, shrink=0.6)  
    cbar.set_label('timepoints')

    plt.subplots_adjust(left=0.05, right=0.95, bottom=0.05, top=0.95, wspace=0.1, hspace=0.1)

    #plt.tight_layout()
    plt.savefig('/Users/julianfeyrer/Documents/GitHub/EOFs_and_domain_shape/scatterImgs/fix_points/'+str(title)+'.jpg')
    plt.close()