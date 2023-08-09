from matplotlib.gridspec import GridSpec
from cartopy.crs import EqualEarth, PlateCarree, Robinson, Mercator
import matplotlib.pyplot as plt

def plot(eofs, rot_eofs, title):
    #proj = EqualEarth(central_longitude=180)
    #proj = PlateCarree(central_longitude=180)
    proj = EqualEarth(central_longitude=180)

    kwargs = {
        'levels' : 10, 'cmap' : 'RdBu', 'vmin' : -0.04, 'vmax': 0.04, 'transform': PlateCarree(), 'shading' : 'auto'
    }
    fig = plt.figure(figsize=(10, 8))
    gs = GridSpec(3, 2)
    ax0 = [fig.add_subplot(gs[i, 0], projection=proj) for i in range(3)]
    ax1 = [fig.add_subplot(gs[i, 1], projection=proj) for i in range(3)]


    for i, (a0, a1) in enumerate(zip(ax0, ax1)):
        mode_range = i+1
        eofs.sel(mode=mode_range).plot.pcolormesh(ax=a0, **kwargs)
        a0.coastlines(color='.5')
        eofs.sel(mode=mode_range+3).plot.pcolormesh(ax=a1, **kwargs)
        a1.coastlines(color='.5')

    plt.tight_layout()
    plt.savefig(str(title)+str(mode_range-2)+'-'+str(mode_range)+'.jpg')

