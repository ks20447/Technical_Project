import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pygamesim import *


plt.rcParams.update({"text.usetex": True, 'font.size': 14})


def heat_map():
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
    

def align_corr_timeseries():

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
    
    
def orient_order_timeseries():
    
    orientational_order = kilobot_df[["TimeStep", "Theta"]]
    
    orientational_order['Cos_2Theta'] = np.cos(2*orientational_order['Theta'])
    
    orientational_order = orientational_order.groupby('TimeStep')['Cos_2Theta'].mean()
    
    mean_order = np.mean(orientational_order)
    
    # Plot the time series of alignment correlation
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
    
    
def theta_histogram():
    
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
    
    
# Read the CSV file into a DataFrame
csv_filename = "Data/kilobot_simulation_data_pandas.csv"
kilobot_df = pd.read_csv(csv_filename)
heat_map()
align_corr_timeseries()
orient_order_timeseries()
theta_histogram()
plt.show()