from xeofs.models import Rotator
import numpy as np


def varimax_xeofs(model):

    rot_var = Rotator(model, n_rot=3, power=1)

    return rot_var.eofs(), rot_var.explained_variance_ratio()
