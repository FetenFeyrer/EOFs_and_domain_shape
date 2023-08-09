import numpy as np
from scipy.special import sph_harm

def subtract_domain_shape(eof_patterns, max_degree, max_order, longitude, latitude):
    """
    Subtract the domain shape effect from EOF patterns using spherical harmonics.

    Args:
        eof_patterns (ndarray): Array of shape (K, M, N) containing K EOF patterns.
        max_degree (int): Maximum degree of the spherical harmonics.
        max_order (int): Maximum order of the spherical harmonics.
        longitude (ndarray): 1-D array of longitude values.
        latitude (ndarray): 1-D array of latitude values.

    Returns:
        ndarray: Array of shape (K, M, N) with the domain shape effect subtracted from the EOF patterns.
    """
    theta = (90 - latitude.reshape(eof_patterns.shape[1:])) * (np.pi / 180)
    phi = longitude.reshape(eof_patterns.shape[1:]) * (np.pi / 180)

    n_points = np.prod(eof_patterns.shape[1:])

    # Compute the spherical harmonic coefficients for each EOF pattern
    coeffs = np.zeros((len(eof_patterns), max_degree + 1, 2 * max_order + 1), dtype=np.complex128)
    for k in range(len(eof_patterns)):
        for n in range(max_degree + 1):
            for m in range(-min(n, max_order), min(n, max_order) + 1):
                coeffs[k, n, m] = np.sum(eof_patterns[k] * sph_harm(m, n, phi, theta)) / n_points

    # Generate new EOF patterns by subtracting the domain shape effect
    modified_eof_patterns = np.zeros_like(eof_patterns)
    for k in range(len(eof_patterns)):
        for n in range(max_degree + 1):
            for m in range(-min(n, max_order), min(n, max_order) + 1):
                harmonics = sph_harm(m, n, phi, theta)
                if m < 0:
                    harmonics = np.conj(harmonics)
                modified_eof_patterns[k] += np.real(coeffs[k, n, m] * harmonics)

    return modified_eof_patterns
