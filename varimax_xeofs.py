from xeofs.xarray import Rotator
import numpy as np


def varimax_xeofs(model):

    rot_var = Rotator(model, n_rot=50, power=1)

    return rot_var.eofs(), rot_var.explained_variance_ratio()
