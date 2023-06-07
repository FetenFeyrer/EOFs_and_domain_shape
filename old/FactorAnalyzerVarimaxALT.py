from factor_analyzer import FactorAnalyzer

def varimax_rotation(loadings):
    rotator = Rotator(method='varimax', normalize=False)
    rotated_loadings = rotator.fit_transform(loadings)


    return rotated_loadings
