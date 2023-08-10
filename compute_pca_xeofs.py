import numpy as np
from xeofs.xarray import EOF
import varimax_xeofs as rot
import xarray as xr
# input: a data set (n x 36(=p)), (number of components computed))
#
# returns: PC loadings (nx36)
def compute_pca(data, n_components=6, correlation_mode=False):
    

    
    model = EOF(data, norm=True, dim=['time'])
    model.solve()
    
   
    eofs = model.eofs()
    

    explained_variances = model.explained_variance_ratio()



    #varimax rotation
    rot_eofs, rot_explained_variances = rot.varimax_xeofs(model)
    
    
    return eofs, rot_eofs, explained_variances*100, rot_explained_variances*100
