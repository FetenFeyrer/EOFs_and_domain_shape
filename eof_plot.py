from matplotlib.gridspec import GridSpec
from cartopy.crs import EqualEarth, PlateCarree, Robinson, Mercator
import matplotlib.pyplot as plt

def plot(eofs, rot_eofs, title):
    #proj = EqualEarth(central_longitude=180)
    #proj = PlateCarree(central_longitude=180)
    proj = Mercator(central_longitude=180)

    kwargs = {
        'cmap' : 'RdBu', 'vmin' : -.05, 'vmax': .05, 'transform': PlateCarree()
    }
    fig = plt.figure(figsize=(10, 8))
    gs = GridSpec(3, 2)
    ax0 = [fig.add_subplot(gs[i, 0], projection=proj) for i in range(3)]
    ax1 = [fig.add_subplot(gs[i, 1], projection=proj) for i in range(3)]


    for i, (a0, a1) in enumerate(zip(ax0, ax1)):
        mode_range = i+1
        eofs.sel(mode=mode_range).plot(ax=a0, **kwargs)
        a0.coastlines(color='.5')
        rot_eofs.sel(mode=mode_range).plot(ax=a1, **kwargs)
        a1.coastlines(color='.5')

    plt.tight_layout()
    plt.savefig('Unweighted eof-smode'+str(title)+'modes: '+str(mode_range-2)+'-'+str(mode_range)+'.jpg')

