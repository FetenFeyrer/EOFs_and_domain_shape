import numpy as np
from xeofs.xarray import EOF
from xeofs.xarray import Rotator
import xarray as xr
# input: a data set (n x 36(=p)), (number of components computed))
#
# returns: PC loadings (nx36)
def compute_pca(data, n_components=6, correlation_mode=False):
    

    
    model = EOF(data, norm=True, dim=['time'])
    
    model.solve()
   
    eofs = model.eofs()
    
    explained_variances = model.explained_variance_ratio()

    pcs = model.pcs()
    #print(loadings.shape)

    #varimax rotation
    rot_eofs, rot_explained_variances = varimax_xeofs(model)
    
    
    return eofs, rot_eofs, explained_variances*100, rot_explained_variances*100


def varimax_xeofs(model):

    rot_var = Rotator(model, n_rot=50, power=1)

    return rot_var.eofs(), rot_var.explained_variance_ratio()
