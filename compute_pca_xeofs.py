import numpy as np
from xeofs.xarray import EOF
import varimax_xeofs as rot
import xarray as xr
# input: a data set (n x 36(=p)), (number of components computed))
#
# returns: PC loadings (nx36)
def compute_pca(data, n_components=6, correlation_mode=False, custom_weights=None):
    

    
    model = EOF(data, norm=False, dim=['time'], weights=custom_weights)
    model.solve()
    
    #pca.fit(data)
    
    #pc_scores = pca.fit_transform(data)
    eofs = model.eofs()
    

    explained_variances = model.explained_variance_ratio()

    pcs = model.pcs()
    #print(loadings.shape)

    #varimax rotation
    rot_eofs, rot_explained_variances = rot.varimax_xeofs(model)
    
    
    return pcs, eofs, rot_eofs, explained_variances*100, rot_explained_variances*100
