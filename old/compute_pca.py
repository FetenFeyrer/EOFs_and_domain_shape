import numpy as np
import sklearn as s
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# input: a data set (n x 36(=p)), (number of components computed))
#
# returns: PC loadings (nx36)
def compute_pca(data, n_components=3, correlation_mode=False):
    
    
    if correlation_mode:
        scaler = StandardScaler()
        data = scaler.fit_transform(data)
    
    
    
    pca = PCA(n_components=n_components, whiten=False)
    #pca.fit(data)
    
    pc_scores = pca.fit_transform(data)

    explained_variances = pca.explained_variance_ratio_

    loadings = pca.components_
    #print(loadings.shape)
    

    return loadings, pc_scores, explained_variances
