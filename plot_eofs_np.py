from matplotlib.gridspec import GridSpec
from cartopy.crs import EqualEarth, PlateCarree
import matplotlib.pyplot as plt

def plot_eofs(eofs):
    proj = EqualEarth(central_longitude=180)

    fig = plt.figure(figsize=(10, 8))
    gs = GridSpec(1, 3)
    ax = [fig.add_subplot(gs[0, i], projection=proj) for i in range(3)]

    for i, a in enumerate(ax):
        pc = eofs[:, i]
        a.scatter(pc, pc, transform=PlateCarree(), s=20)
        a.set_xlabel('PC{}'.format(i+1))
        a.set_ylabel('PC{}'.format(i+1))
        a.coastlines(color='.5')

    plt.tight_layout()
    plt.show()