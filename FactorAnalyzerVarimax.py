from factor_analyzer import FactorAnalyzer
import numpy as np

def compute_rotated_pc_loadings(pc_loadings):
    # Initialize factor analyzer with 1 component
    fa = FactorAnalyzer(n_factors=1, rotation='varimax')

    # Fit the factor analyzer to the principal components
    fa.fit(pc_loadings)

    # Get the rotated loadings
    rotated_loadings = fa.loadings_

    return rotated_loadings
