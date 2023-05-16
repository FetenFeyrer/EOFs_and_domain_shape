import numpy as np
import sklearn as s
from sklearn.decomposition import PCA


# input: a data set (n x 36(=p)), (number of components computed))
#
# returns: PC loadings (1x36), covariance matrix (pxp)
def compute_pca(data, n_components=3):
    # Perform PCA
    pca = PCA(n_components=n_components)
    pca_result = pca.fit_transform(data)
    loadings = pca.components_
    covariance = pca.get_covariance()
    
    #print(loadings)
    

    return loadings, covariance
