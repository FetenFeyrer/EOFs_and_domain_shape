import numpy as np
import matplotlib.pyplot as plt

def plot_eigenvalue_sequences(sequences, title):
    colors = ['red', 'blue', 'green', 'orange', 'purple', 'black', 'yellow', 'magenta']  # Define a list of colors

    plt.figure(figsize=(10, 6))  # Set the figure size

    for i, sequence in enumerate(sequences):
        color = colors[i % len(colors)]  # Get a color from the list based on the index
        indices = np.arange(0, 21)  # Generate integer indices from 1 to 40
        plt.plot(indices, sequence[:21], color=color, label=f'Set: '+ str(i+1))  # Plot only the first 40 eigenvalues with integer indices


    min_var = np.min([seq[:20] for seq in sequences])
    max_var = np.max(sequences)

    plt.xlabel('Eigenvalue Index')  # Set the x-axis label
    plt.xticks(np.arange(1, 21, 1)) 
    plt.yticks(np.arange(np.round(min_var-0.1,2), np.round(max_var+0.1,2), np.round((max_var-min_var)/20,2))) 
    plt.ylabel('Explained Variance [in %]')  # Set the y-axis label
    plt.title('Eigenvalue Sequences - '+ str(title))  # Set the title
    plt.xlim(0, 20)  # Set the x-axis limits
    #plt.legend()  # Show the legend
    plt.grid(True)  # Show the grid
    plt.savefig('/Users/julianfeyrer/Documents/GitHub/EOFs_and_domain_shape/Eigenvalue Plot -  '+str(title)+'.jpg')  # Display the plot

