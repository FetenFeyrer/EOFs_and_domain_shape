import numpy as np
from xeofs.models import EOF
import varimax_xeofs as rot
import xarray as xr

from construct_xarray_eofs import construct_xarray



# input: a data set (n x 36(=p)), (number of components computed))
#
# returns: PC loadings (nx36)
def compute_pca(data, n_components=6):
    
    
    model = EOF(data, n_modes=n_components, norm=True)
    model.solve()
    
    eofs = model.eofs()

    eofs_xar = construct_xarray(eofs, 39, 80)
    
    explained_variances = model.explained_variance_ratio()

    pcs = model.pcs()

    #varimax rotation
    rot_eofs, rot_explained_variances = rot.varimax_xeofs(model)

    rot_eofs_xar = construct_xarray(rot_eofs, 39, 80)
    
    
    return pcs, eofs_xar, rot_eofs_xar, explained_variances*100, rot_explained_variances*100
