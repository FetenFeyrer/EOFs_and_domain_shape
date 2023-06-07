import numpy as np
from xeofs.models import EOF
import varimax_xeofs as rot
import xarray as xr
# input: a data set (n x 36(=p)), (number of components computed))
#
# returns: PC loadings (nx36)
def compute_pca(data, n_components=3, correlation_mode=False):
    
    #xdata = xr.DataArray(data)
    
    #if correlation_mode:
    #    scaler = StandardScaler()
    #    data = scaler.fit_transform(data)
    
    model = EOF(data, n_modes=n_components, norm=correlation_mode)
    model.solve()

    
    #pca.fit(data)
    
    #pc_scores = pca.fit_transform(data)
    eofs = model.eofs()

    explained_variances = model.explained_variance_ratio()

    pcs = model.pcs()
    #print(loadings.shape)

    #varimax rotation
    rot_eofs, rot_explained_variances = rot.varimax_xeofs(model)
    

    return pcs.T, eofs.T, rot_eofs.T, explained_variances*100, rot_explained_variances*100
