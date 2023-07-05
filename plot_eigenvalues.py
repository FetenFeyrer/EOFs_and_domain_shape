import numpy as np
import matplotlib.pyplot as plt

def plot_eigenvalue_sequences(sequences):
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'black', 'yellow', 'magenta']  # Define a list of colors

    plt.figure(figsize=(10, 6))  # Set the figure size

    for i, sequence in enumerate(sequences):
        color = colors[i % len(colors)]  # Get a color from the list based on the index
        indices = np.arange(1, 21)  # Generate integer indices from 1 to 40
        plt.plot(indices, sequence[:20], color=color, label=f'length-scale {(i+1)/10.0}')  # Plot only the first 40 eigenvalues with integer indices

    plt.xlabel('Index')  # Set the x-axis label
    plt.xticks(np.arange(1, 21, 1)) 
    plt.yticks(np.arange(1, 30, 1)) 
    plt.ylabel('Eigenvalue')  # Set the y-axis label
    plt.title('Eigenvalue Sequences')  # Set the title
    plt.legend()  # Show the legend
    plt.grid(True)  # Show the grid
    plt.savefig('/Users/julianfeyrer/Documents/GitHub/EOFs_and_domain_shape/Eigenvalue Plot.jpg')  # Display the plot

