import numpy as np

def add_gaussian_noise(matrix, mean, std_dev):
    # Get the shape of the matrix
    rows, cols = matrix.shape
    
    # Generate Gaussian noise with the same shape as the matrix
    noise = np.random.normal(mean, std_dev, size=(rows, cols))

    # Add the noise to each row vector
    matrix_with_noise = matrix + noise
    
    return matrix_with_noise
