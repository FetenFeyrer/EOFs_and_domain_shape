import numpy as np

#reflect the input_matrix by a value x
#
# input: input_matrix, value of reflection x
def reflect_by_x(input_matrix, x):
    reflected_matrix = input_matrix - x
    reflected_matrix = -reflected_matrix
    reflected_matrix += x
    return reflected_matrix