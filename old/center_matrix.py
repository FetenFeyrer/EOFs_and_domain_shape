import numpy as np

def center_matrix(matrix):
    # Calculate the mean along each column
    column_means = np.mean(matrix, axis=0)

    # Subtract the column means from the matrix
    centered_matrix = matrix - column_means

    return centered_matrix
