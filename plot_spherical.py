import matplotlib.pyplot as plt
import cartopy.crs as ccrs
import numpy as np

def plot_isolines(dataset):
    # Create a plot figure
    fig = plt.figure(figsize=(10, 6))
    ax = fig.add_subplot(1, 1, 1, projection=ccrs.PlateCarree())

    # Plot isolines of pressure patterns
    levels = np.arange(1008, 1033, 2)
    contour = ax.contour(dataset.lon, dataset.lat, dataset, levels=levels, colors='black')

    # Add contour labels
    ax.clabel(contour, inline=True, fontsize=8, fmt='%1.0f')

    # Set plot title and axis labels
    ax.set_title("Pressure Isolines")
    ax.set_xlabel("Longitude")
    ax.set_ylabel("Latitude")

    # Set gridlines
    ax.gridlines()

    # Show the plot
    plt.show()

