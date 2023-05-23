import numpy as np
import sklearn as s
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# input: a data set (n x 36(=p)), (number of components computed))
#
# returns: PC loadings (3x36)
def compute_pca(data, n_components=36, correlation_mode=False):
    
    
    if correlation_mode:
        scaler = StandardScaler()
        data = scaler.fit_transform(data)

    
    # Perform PCA on the correlation matrix
    pca = PCA(n_components=n_components)
    pca.fit(data)
    
    pc_scores = pca.transform(data)


    loadings = pca.components_
    
    #print(loadings.shape)
    

    return loadings, pc_scores.T
