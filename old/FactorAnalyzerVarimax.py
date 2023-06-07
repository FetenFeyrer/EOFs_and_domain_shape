from factor_analyzer import Rotator

def varimax_rotation(loadings):

    rotator = Rotator(method='varimax', normalize=True)

    rotated_loadings = rotator.fit_transform(loadings)

    return rotated_loadings
