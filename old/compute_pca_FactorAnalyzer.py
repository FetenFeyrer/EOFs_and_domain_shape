import numpy as np
import sklearn as s
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

from factor_analyzer import FactorAnalyzer

# input: a data set (n x 36(=p)), (number of components computed))
#
# returns: PC loadings (nx36)
def compute_pca(data, n_components=36, correlation_mode=False):
    
    
    
    fa = FactorAnalyzer(rotation='varimax', method='principal', n_factors=3)
    fa.fit(data)

    loadings = fa.loadings_
    
    #pca = PCA(n_components=n_components)
    #pca.fit(data)
    
    #pc_scores = pca.fit_transform(data)

    #explained_variances = pca.explained_variance_ratio_

    #loadings = pca.components_
    #print(loadings.shape)
    

    return loadings.T, [], [1,1,1]
