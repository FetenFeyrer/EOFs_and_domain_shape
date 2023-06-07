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
    
    
    
    cov = np.cov(data.T)
    ev , eig = np.linalg.eig(cov)
    a = eig.dot(data.T)
    

    return eig.T[:3], a.T, [1,1,1]
