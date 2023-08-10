from ComputeEOFs import *
from Data import *
from xeofs.models import EOF
from xeofs.models import Rotator
from matplotlib.colors import TwoSlopeNorm

def reflect_by_x(input_matrix, x):
    """
    reflect a data sample by a value x
    Parameters:
    ----------
    input_matrix: a numpy array to be reflected
    x: integer to reflect on
    """
    reflected_matrix = input_matrix - x
    reflected_matrix = -reflected_matrix
    reflected_matrix += x
    return reflected_matrix

def add_gaussian_noise(matrix, mean, std_dev):
    # Get the shape of the matrix
    rows, cols = matrix.shape
    
    # Generate Gaussian noise with the same shape as the matrix
    noise = np.random.normal(mean, std_dev, size=(rows, cols))

    # Add the noise to each row vector
    matrix_with_noise = matrix + noise
    
    return matrix_with_noise

# Function to plot isolines on a subplot
def plot_isoLines(dataset, ax, title, vmin, vmax):
    
    # Reshape input sample dataset to a 6x6 matrix
    dataset = dataset.reshape(6, 6)
    dataset = add_gaussian_noise(dataset, 0, 1)
    x = np.arange(dataset.shape[0])
    y = np.arange(dataset.shape[1])
    X, Y = np.meshgrid(x, y)

    # Define levels for contour lines
    levels = np.linspace(vmin, vmax, 20)

    # Flip the Y coordinates vertically
    Y = np.max(Y) - Y

    # Plot the isolines using the coolwarm colormap
    contour = ax.contourf(X, Y, dataset, levels=levels, extend='both', cmap='coolwarm')
    # Add contour lines on top of the filled shapes
    contour_lines = ax.contour(X, Y, dataset, levels=levels, colors='k', linewidths=0.5)
    plt.clabel(contour_lines, inline=True, fontsize=8, fmt='%d') 
    ax.set_title(title)  # Set subplot title
    ax.grid(True)  # Show grid lines
    ax.set_xticklabels([])  # Remove X-axis tick labels
    ax.set_yticklabels([])  # Remove Y-axis tick labels
    ax.tick_params(axis='both', which='both', length=0)  # Remove tick marks
    return contour  # Return the contour object for colorbar consistency

# Function to plot different flow types
def plot_FlowTypes(flow_samples, titles):
    num_samples = len(flow_samples)

    num_rows = (num_samples + 2) // 3
    num_cols = min(num_samples, 3)
    
    vmin = max(np.min(flow_samples), 0)
    vmax = max(np.max(flow_samples), 0)

    fig = plt.figure(figsize=(12, 8))
    gs = GridSpec(num_rows, num_cols, figure=fig, width_ratios=[1, 1, 1], wspace=0.1, hspace=0.2)
    axs = [fig.add_subplot(gs[i, j]) for i in range(num_rows) for j in range(num_cols)]

    contour_levels = None

    for i, ax in enumerate(axs):
        if i < num_samples:
            sample_data = flow_samples[i]
            title = titles[i]
            contour = plot_isoLines(sample_data, ax, title, vmin, vmax)
            ax.set_aspect('equal')
            if i == 0:
                contour_levels = contour.levels
            else:
                contour.levels = contour_levels
            ax.set_title(title)
        else:
            ax.axis('off')

    # Create a colorbar
    cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])  # Adjust position as needed
    cbar = fig.colorbar(contour, cax=cbar_ax, ticks=np.arange(vmin, vmax + 1, 2))
    cbar.set_label('hPa')  # Set colorbar label

    plt.tight_layout()
    plt.savefig('imgs/FlowPatterns.png')


def plot_isoLines_eof(dataset, ax, title, vmin, vmax):
    # Reshape input sample dataset to a 6x6 matrix
    dataset = dataset.reshape(6, 6)

    x = np.arange(dataset.shape[0])
    y = np.arange(dataset.shape[1])
    X, Y = np.meshgrid(x, y)

    # Define levels for contour lines including 0
    levels = np.linspace(vmin, vmax, 25)

    # Flip the Y coordinates vertically
    Y = np.max(Y) - Y

    # Use TwoSlopeNorm to center the white color at 0
    norm = TwoSlopeNorm(vcenter=0, vmin=vmin, vmax=vmax)

    # Plot the isolines using the RdBu colormap (centered at 0)
    contour = ax.contourf(X, Y, dataset, levels=levels, extend='both', cmap='coolwarm', norm=norm)

    # Add contour lines on top of the filled shapes
    contour_lines = ax.contour(X, Y, dataset, levels=levels, colors='k', linewidths=0.5)
    plt.clabel(contour_lines, inline=True, fontsize=10)    
    ax.set_title(title)  # Set subplot title
    ax.grid(True)  # Show grid lines
    ax.set_xticklabels([])  # Remove X-axis tick labels
    ax.set_yticklabels([])  # Remove Y-axis tick labels
    ax.tick_params(axis='both', which='both', length=0)  # Remove tick marks
    return contour  # Return the contour object for colorbar consistency

# Function to plot different flow types
def plot_EOFs(eofs, exp_var, plotTitle):
    num_samples = len(eofs)

    num_rows = (num_samples + 2) // 3
    num_cols = min(num_samples, 3)
    
    fig = plt.figure(figsize=(18, 10))
    gs = GridSpec(num_rows, num_cols, figure=fig, width_ratios=[1, 1, 1], wspace=0.1, hspace=0.2)
    axs = [fig.add_subplot(gs[i, j]) for i in range(num_rows) for j in range(num_cols)]

    # Determine the overall color limits based on the maximum and minimum values in all eofs
    vmin = min(np.min(eofs),0)
    vmax = max(np.max(eofs),0)

    for i, ax in enumerate(axs):
        if i < num_samples:
            sample_data = eofs[i]
            title = 'EOF ' + str(i+1) + ' - Explained variance= ~'+str(exp_var[i])
            if i > 2:
                title = 'VARIMAX rotated EOF ' + str(i+1) + ' - Explained variance= ~'+str(exp_var[i])
            contour = plot_isoLines_eof(sample_data, ax, title, vmin, vmax)
            ax.set_aspect('equal')
            if i == 0:
                contour_levels = contour.levels
            else:
                contour.levels = contour_levels
            ax.set_title(title)
        else:
            ax.axis('off')


    # Create a colorbar
    cbar_ax = fig.add_axes([0.92, 0.15, 0.02, 0.7])  # Adjust position as needed
    cbar = fig.colorbar(contour, cax=cbar_ax, ticks=contour_levels)

    # Format tick labels to be rounded to 2 decimal places
    cbar.ax.set_yticklabels(['{:.2f}'.format(tick) for tick in contour_levels])
    
    cbar.set_label('EOF coefficients')  # Set colorbar label

    plt.tight_layout()
    plt.savefig('imgs/'+str(plotTitle)+'.png', bbox_inches='tight')






# input: a data set (n x 36(=p)), (number of components computed))
#
# returns: PC loadings (nx36)
def compute_pca(data, n_components=3, correlation_mode=False):

    
    model = EOF(data, n_modes=n_components, norm=correlation_mode)
    model.solve()
    for i in range(3):
        model._eofs[:,i]*=np.sqrt(model._explained_variance[i])
    
    eofs = model.eofs()


    explained_variances = model.explained_variance()
   
    

    #varimax rotation
    rot_eofs, rot_explained_variances = varimax_xeofs(model)
    

    return eofs.T, rot_eofs.T, np.round(model.explained_variance_ratio()*100, 2), np.round(np.sqrt(rot_explained_variances), 2)



def varimax_xeofs(model):

    rot_var = Rotator(model, n_rot=500, power=1)


    for i in range(3):
        #eofs[i]*=np.sqrt(eofs_exp_var[i])
        rot_var._eofs[:,i]*=np.sqrt(np.sqrt(rot_var._explained_variance[i]))

    return rot_var.eofs(), rot_var.explained_variance_ratio()






















    
# Meridional flow patterns - Compagnucci and Richman (2007)
sample_inverse_MeridionalFlow = np.array([1032, 1028, 1024, 1020, 1016, 1012,
                                        1032, 1028, 1024, 1020, 1016, 1012,
                                        1032, 1028, 1024, 1020, 1016, 1012,
                                        1032, 1028, 1024, 1020, 1016, 1012,
                                        1032, 1028, 1024, 1020, 1016, 1012,
                                        1032, 1028, 1024, 1020, 1016, 1012])

sample_direct_MeridionalFlow = reflect_by_x(sample_inverse_MeridionalFlow, 1012)

# Zonal flow patterns - Compagnucci and Richman (2007)
sample_inverse_ZonalFlow= np.array([1032,1032,1032,1032,1032,1032,
                                    1028,1028,1028,1028,1028,1028,
                                    1024,1024,1024,1024,1024,1024,
                                    1020,1020,1020,1020,1020,1020,
                                    1016,1016,1016,1016,1016,1016,
                                    1012,1012,1012,1012,1012,1012])


sample_direct_ZonalFlow = reflect_by_x(sample_inverse_ZonalFlow, 1012)

# Cyclonic flow patterns - Compagnucci and Richman (2007)
sample_direct_CyclonicFlow = np.array([1032, 1028, 1024, 1024, 1028, 1032,
                                            1028, 1024, 1020, 1020, 1024, 1028,
                                            1024, 1020, 1016, 1016, 1020, 1024,
                                            1024, 1020, 1016, 1016, 1020, 1024,
                                            1028, 1024, 1020, 1020, 1024, 1028,
                                            1032, 1028, 1024, 1024, 1028, 1032])


sample_inverse_CyclonicFlow = reflect_by_x(sample_direct_CyclonicFlow, 1012)




# building the input data matrix for the artificial flow behaviour in S-Mode
# A = meridional, B = inverse meridional, C = zonal, D = inverse Zonal, E = cyclonic, F = inverse cyclonic
# sequence composition: AAAAAA BBBBBB CCCCCC DDDDDD EEEEEE FFFFFF


####### PLASMODE 1 ########
# Plasmode 2 in Compagnucci and Richman (2007)

AAAAAA = np.tile(sample_direct_MeridionalFlow, (6,1))
BBBBBB = np.tile(sample_inverse_MeridionalFlow, (6,1))
CCCCCC = np.tile(sample_direct_ZonalFlow, (6,1))
DDDDDD = np.tile(sample_inverse_ZonalFlow, (6,1))
EEEEEE = np.tile(sample_direct_CyclonicFlow, (6,1))
FFFFFF = np.tile(sample_inverse_CyclonicFlow, (6,1))


input_matrix_plasmode1 = np.vstack((AAAAAA,BBBBBB,CCCCCC,DDDDDD,EEEEEE,FFFFFF))
input_matrix_plasmode1 = add_gaussian_noise(input_matrix_plasmode1, 0, 1)


####### PLASMODE 2 #########
# Plasmode 7 in Compagnucci and Richman (2007)

AAAx20 = np.tile(sample_direct_ZonalFlow, (20,1))
CCCx5 = np.tile(sample_direct_MeridionalFlow, (5,1))
DDDx5 = np.tile(sample_inverse_MeridionalFlow, (5,1))
EEEx3 = np.tile(sample_direct_CyclonicFlow, (3,1))
FFFx3 = np.tile(sample_inverse_CyclonicFlow, (3,1))

input_matrix_plasmode2 = np.vstack((AAAx20, CCCx5, DDDx5, EEEx3, FFFx3))
input_matrix_plasmode2 = add_gaussian_noise(input_matrix_plasmode2, 0, 1)



titles = ['Direct zonal flow (A)','Inverse zonal flow (B)','Direct meridional flow (C)','Inverse meridional flow (D)','Direct cyclonic flow (E)','Inverse cyclonic flow (F)']
plot_FlowTypes([sample_direct_ZonalFlow, sample_inverse_ZonalFlow, sample_direct_MeridionalFlow, sample_inverse_MeridionalFlow, sample_direct_CyclonicFlow, sample_inverse_CyclonicFlow],titles)

eofs, rot_eofs, eofs_exp_var, rot_eofs_exp_var = compute_pca(input_matrix_plasmode1)


plot_EOFs(np.vstack((eofs,rot_eofs)), np.hstack((eofs_exp_var, rot_eofs_exp_var)), 'EOFs_artificial_flow_patterns_plasmode1')
#plot_EOFs(rot_eofs, rot_eofs_exp_var, 'Varimax_rotated_EOFs_artificial_flow_patterns')

eofs, rot_eofs, eofs_exp_var, rot_eofs_exp_var = compute_pca(input_matrix_plasmode2)


plot_EOFs(np.vstack((eofs,rot_eofs)), np.hstack((eofs_exp_var, rot_eofs_exp_var)), 'EOFs_artificial_flow_patterns_plasmode2')
