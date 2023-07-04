import numpy as np
from xeofs.models import EOF
import varimax_xeofs as rot
import xarray as xr



# input: a data set (n x 36(=p)), (number of components computed))
#
# returns: PC loadings (nx36)
def compute_pca(data, n_components=6, correlation_mode=False, custom_weights=None):
    
    # Define the number of rows and columns
    num_rows = 3120

    # Generate the values for the first and fifth columns (increasing from 0 to 1)
    col1_values = np.linspace(0, 1, num_rows)
    col5_values = np.linspace(0, 1, num_rows)

    # Generate the values for the second and sixth columns (decreasing from 0 to -1)
    col2_values = np.linspace(0, -1, num_rows)
    col6_values = np.linspace(0, -1, num_rows)

    # Generate the values for the third and fourth columns (increasing from -1 to 1)
    col3_values = np.linspace(-1, 1, num_rows)
    col4_values = np.linspace(-1, 1, num_rows)

    # Concatenate the column values horizontally to form the final array
    TestEOF = np.concatenate(
        (
            col1_values[:, np.newaxis],
            col2_values[:, np.newaxis],
            col3_values[:, np.newaxis],
            col4_values[:, np.newaxis],
            col5_values[:, np.newaxis],
            col6_values[:, np.newaxis],
        ),
        axis=1,
    )
   
    print(TestEOF)
    model = EOF(data, n_modes=n_components, norm=True)
    model.solve()
    
    #pca.fit(data)
    
    #pc_scores = pca.fit_transform(data)
    eofs = model.eofs()


    eofs = TestEOF.T.reshape(6,39,80)

    

    lat = np.linspace(-90, 90, 39)
    lon = np.linspace(-180, 180, 80)
    mode = np.arange(1, n_components+1, dtype=np.int64)

    # Create the attributes for the new Xarray data array
    attributes = {
        'long_name': 'EOFs',
        'units': 'dimensionless',
        'description': 'Empirical Orthogonal Functions',
        'source': 'Some source',
    }

    # Create the new Xarray data array
    eofs_xar = xr.DataArray(
        eofs,
        dims=('mode', 'lat', 'lon'),
        coords={'lat': lat, 'lon': lon, 'mode': mode},
        attrs=attributes,
    )
    

    explained_variances = model.explained_variance_ratio()

    pcs = model.pcs()
    #print(loadings.shape)

    #varimax rotation
    rot_eofs, rot_explained_variances = rot.varimax_xeofs(model)
    
    
    return pcs, eofs_xar, rot_eofs, explained_variances*100, rot_explained_variances*100
