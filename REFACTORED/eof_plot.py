import matplotlib.pyplot as plt
from matplotlib.gridspec import GridSpec
from matplotlib.colors import Normalize
from matplotlib.colorbar import ColorbarBase
from cartopy.crs import EqualEarth, PlateCarree, Mercator
import numpy as np

def plot(eofs, rot_eofs, title, is_cropped=False):
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

    # Iterate through the subplots and add content
    for i, (a0, a1) in enumerate(zip(ax0, ax1)):
        mode_range = i + 1
        if is_cropped:
            eofs.sel(mode=mode_range).plot.contourf(ax=a0, **kwargs, add_colorbar=False)
        else:
            eofs.sel(mode=mode_range+1).plot.contourf(ax=a0, **kwargs, add_colorbar=False)
        a0.coastlines(color='.5')
        if is_cropped:
            rot_eofs.sel(mode=mode_range).plot.contourf(ax=a1, **kwargs, add_colorbar=False)
        else:
            rot_eofs.sel(mode=mode_range+1).plot.contourf(ax=a1, **kwargs, add_colorbar=False)
        a1.coastlines(color='.5')

        a0.set_title(f'EOF {mode_range+1}')
        a1.set_title(f'Rotated EOF {mode_range+1}')
        

    # Create a shared colorbar
    norm = Normalize(vmin=kwargs['vmin'], vmax=kwargs['vmax'])
    cax = fig.add_subplot(gs[:, 2])
    cb = ColorbarBase(cax, cmap=kwargs['cmap'], norm=norm, orientation='vertical')
    cb.set_label('EOF coefficients')  # Set your desired label

    plt.tight_layout(rect=[0, 0, 0.92, 1])
    plt.savefig(f'{title}.jpg')


