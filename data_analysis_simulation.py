import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from kilobots import *
from pygamesim import NUM_KILOBOTS


plt.rcParams.update({"text.usetex": True, 'font.size': 14})


def kilobot_heat_map(name=False):
    # Define the grid parameters
    grid_size = 20

    # Create a new column indicating the grid square each Kilobot is in
    kilobot_df['GridX'] = (kilobot_df['X'] // grid_size) * grid_size
    kilobot_df['GridY'] = (kilobot_df['Y'] // grid_size) * grid_size

    # Count the number of instances for each grid square
    heatmap_data = kilobot_df.groupby(['GridY', 'GridX']).size().unstack(fill_value=0)

    # Create a heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(heatmap_data, cmap='viridis', annot=False)

    # Invert y-axis
    plt.gca().invert_yaxis()

    plt.title("Heatmap of Kilobots in 20x20 Grid Squares")
    plt.xlabel("Grid X")
    plt.ylabel("Grid Y")
    if name:
        plt.savefig(f"Results/{name}.pdf")
    

def align_corr_timeseries(name=False):

    alignment_corr = kilobot_df[["TimeStep", "Theta"]]

    alignment_corr['Cos_Theta'] = np.cos(alignment_corr['Theta'])
    alignment_corr['Sin_Theta'] = np.sin(alignment_corr['Theta'])
    
    alignment_corr = alignment_corr.groupby('TimeStep')[['Cos_Theta', 'Sin_Theta']].mean()    
    alignment_corr['Norm'] = np.linalg.norm(alignment_corr[['Cos_Theta', 'Sin_Theta']], axis=1)
    
    mean_corr = np.mean(alignment_corr['Norm'])
    
    # Plot the time series of alignment correlation
    plt.figure(figsize=(12, 6))
    time = frames_to_milliseconds(np.array(alignment_corr.index, dtype=int))
    plt.plot(time, alignment_corr['Norm'], marker='o', linestyle='-', label="Alignment Corr")
    plt.axhline(y=mean_corr, color='red', linestyle='--', label=f"Average Corr = {mean_corr:.3f}")

    plt.title("Time Series of Alignment Correlation")
    plt.xlabel("Time (ms)")
    plt.ylabel("Alignment Correlation")
    plt.ylim([0, 1])
    plt.grid(True)
    plt.legend()
    if name:
        plt.savefig(f"Results/{name}.pdf")
    
    
def orient_order_timeseries(name=False):
    
    orientational_order = kilobot_df[["TimeStep", "Theta"]]
    
    orientational_order['Cos_2Theta'] = np.cos(2*orientational_order['Theta'])
    
    orientational_order = orientational_order.groupby('TimeStep')['Cos_2Theta'].mean()
    
    mean_order = np.mean(orientational_order)
    
    # Plot the time series of orientational order
    plt.figure(figsize=(12, 6))
    time = frames_to_milliseconds(np.array(orientational_order.index, dtype=int))
    plt.plot(time, orientational_order, marker='o', linestyle='-', label="Orientational Order")
    plt.axhline(y=mean_order, color='red', linestyle='--', label=f"Average Order = {mean_order:.3f}")

    plt.title("Time Series of Orientational Order")
    plt.xlabel("Time (ms)")
    plt.ylabel("Orientational Order")
    plt.ylim([-1, 1])
    plt.grid(True)
    plt.legend()
    if name:
        plt.savefig(f"Results/{name}.pdf")    
        
    
def theta_histogram(name=False):
    
    theta = kilobot_df["Theta"]
    num_bins = 16
    
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(12, 6))
    ax.set_theta_zero_location('E')
    ax.set_theta_direction(1)
    
    step = 2*math.pi/num_bins
    bins = np.arange(0, 2*math.pi + step, step)
    
    ax.hist(theta, bins=bins, label=f"Average $\\theta$ = {theta.mean():.2f}")
    ax.set_xticklabels(['0', r'$\frac{\pi}{4}$', r'$\frac{\pi}{2}$', r'$\frac{3\pi}{4}$', r'$\pi$',
                    r'$\frac{5\pi}{4}$', r'$\frac{3\pi}{2}$', r'$\frac{7\pi}{4}$'])
    ax.set_title(f"Distribution of $\\theta$")
    ax.legend(loc='upper right', bbox_to_anchor=(1.2, 1))
    if name:
        plt.savefig(f"Results/{name}.pdf")    
    
    
def kilobot_neighbor_timeseries(num_bots, name=False):
    
    plt.figure(figsize=(12, 6))
    
    id_array = [random.randint(0, NUM_KILOBOTS) for _ in range(num_bots)]
    
    for bot_id in id_array:
        bot_neighbors = kilobot_df.loc[kilobot_df['KilobotID'] == bot_id, 'Neighbors']
        
        # Plot the time series of alignment correlation
        time = frames_to_milliseconds(np.array(bot_neighbors.index, dtype=int))
        plt.plot(time, bot_neighbors, marker='o', linestyle='-', label=f"ID: {bot_id}")

    plt.title("Time Series of Kilobot Neighbors")
    plt.xlabel("Time (ms)")
    plt.ylabel("Count")
    plt.grid(True)
    plt.legend()
    if name:
        plt.savefig(f"Results/{name}.pdf")
        

def centre_of_mass_heatmap(name=False):

    grid_width = int(WIDTH / 20)
    grid_height = int(HEIGHT / 20)
    counts_matrix = np.zeros((grid_height, grid_width))
    
    com_x_coords = kilobot_df[["TimeStep", "CoMX"]]
    com_y_coords = kilobot_df[["TimeStep", "CoMY"]]
    
    com_x_coords['SingleCoMX'] = com_x_coords["CoMX"]
    com_y_coords['SingleCoMY'] = com_x_coords["CoMY"]
    
    com_x_coords = com_x_coords.groupby('TimeStep')['SingleCoMX'].mean() 
    com_y_coords = com_y_coords.groupby('TimeStep')['SingleCoMY'].mean()
    
    coords_tuples = list(zip(com_x_coords['CoMX'], com_y_coords['CoMY']))

    for x, y in coords_tuples:
        # Increment the count for the grid cell corresponding to each point
        # Ensure that x and y are within the bounds of your grid dimensions
        if 0 <= x < grid_width and 0 <= y < grid_height:
            counts_matrix[y, x] += 1  # Note: NumPy arrays are accessed as [row, column], hence [y, x] here

    # Create a heatmap
    plt.figure(figsize=(12, 10))
    sns.heatmap(counts_matrix, cmap='viridis', annot=False)

    # Invert y-axis
    plt.gca().invert_yaxis()

    plt.title("Heatmap of Kilobots CoM in 20x20 Grid Squares")
    plt.xlabel("Grid X")
    plt.ylabel("Grid Y")
    if name:
        plt.savefig(f"Results/{name}.pdf")   
    

        
def sequencing_error_plots(name=False):
    # Maybe change this to more accurately represent no estimate instead of perfect estimate
    
    def calculate_mean_and_count_zeros(group):
        non_zeros = group[group != 0]
        zeros_count = len(group) - len(non_zeros)
        mean_non_zeros = non_zeros.mean() if len(non_zeros) > 0 else np.nan  # Avoid division by zero
        return pd.Series({'MeanError': mean_non_zeros, 'ZeroCount': zeros_count})
    
    csv_triangle = "Data/kilobot_simulation_data_pandas_pattern_triangle_error.csv"
    csv_intensity = "Data/kilobot_simulation_data_pandas_pattern_intensity_error.csv"
    kilobot_df_triangle = pd.read_csv(csv_triangle)
    kilobot_df_intensity = pd.read_csv(csv_intensity)
    
    plt.figure(figsize=(12, 6))
    
    sequence_error_triangle = kilobot_df_triangle[["TimeStep", "EstimateError"]]
    sequence_error_intensity = kilobot_df_intensity[["TimeStep", "EstimateError"]]
    
    sequence_error_triangle = sequence_error_triangle.groupby("TimeStep")["EstimateError"].apply(calculate_mean_and_count_zeros).unstack()
    sequence_error_intensity = sequence_error_intensity.groupby("TimeStep")["EstimateError"].apply(calculate_mean_and_count_zeros).unstack()
    
    time = frames_to_milliseconds(np.array(sequence_error_triangle.index, dtype=int))
    
    plt.plot(time, sequence_error_triangle['MeanError'], marker='x', color="red", label="Pattern Triangle")
    plt.plot(time, sequence_error_intensity['MeanError'], marker='x', color="blue", label="Pattern Intensity")
    plt.title("Mean Sequence Error")
    plt.xlabel("Time (ms)")
    plt.ylabel("Mean Error (Radians)")
    plt.grid(True)
    plt.legend()   
    
    if name:
        plt.savefig(f"Results/{name}(a).pdf")
        
    # plt.figure(figsize=(12, 6))
    # plt.plot(time, sequence_error_triangle['ZeroCount'], marker='o', color="red", label="Pattern Triangle")
    # plt.plot(time, sequence_error_intensity['ZeroCount'], marker='o', color="blue", label="Pattern Intensity")
    # plt.title("Number of Kilobots without estimated heading over time")
    # plt.xlabel("Time (ms)")
    # plt.ylabel("Count")
    # plt.grid(True)
    
    # if name:
    #     plt.savefig(f"Results/{name}(b).pdf")
    
    
# Read the CSV file into a DataFrame
csv_filename = "Data/kilobot_simulation_data_pandas_test"
kilobot_df = pd.read_csv(csv_filename)
# kilobot_heat_map()
# align_corr_timeseries()
# orient_order_timeseries()
# theta_histogram()
# kilobot_neighbor_timeseries(5)
# centre_of_mass_heatmap()
sequencing_error_plots()
plt.show()