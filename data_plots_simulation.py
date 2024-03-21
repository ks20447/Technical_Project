import math
import random
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from kilobots import frames_to_milliseconds


plt.rcParams.update({"text.usetex": True, 'font.size': 16})


def one_bot_path(df):

    fig, axs = plt.subplots(1, 2, figsize=(14, 8))

    axs[0].plot(df['X'], df['Y'], linestyle='-', linewidth=1, label="Kilobot Path")
    axs[0].plot(df['X'].iloc[0], df['Y'].iloc[0], color='green', marker='o', markersize=10, label="Start")
    axs[0].plot(df['X'].iloc[-1], df['Y'].iloc[-1], color='red', marker='o', markersize=10, label="End")
    axs[0].set_title("Full Domain")
    axs[0].set_xlabel("X (pixels)")
    axs[0].set_ylabel("Y (pixels)")
    axs[0].set_xlim(0, 800)
    axs[0].set_ylim(0, 800)
    axs[0].grid()
    axs[0].legend()

    axs[1].plot(df['X'], df['Y'], linestyle='-', linewidth=1, label="Kilobot Path")
    axs[1].plot(df['X'].iloc[0], df['Y'].iloc[0], color='green', marker='o', markersize=10, label="Start")
    axs[1].plot(df['X'].iloc[-1], df['Y'].iloc[-1], color='red', marker='o', markersize=10, label="End")
    axs[1].set_title("Sub-Domain")
    axs[1].set_xlabel("X (pixels)")
    axs[1].set_ylabel("Y (pixels)")
    axs[1].grid()
    axs[1].legend()

    plt.tight_layout()
    plt.subplots_adjust(top=0.9)
    plt.suptitle("100 Second Kilobot Run and Tumble Simulation")
    plt.savefig("Results/RunAndTumble.png")


def heatmap_align_anti(df_align, df_anti):
    fig, axs = plt.subplots(1, 2, figsize=(14, 10))

    grid_size = 20

    df_align['GridX'] = (df_align['X'] // grid_size) * grid_size
    df_align['GridY'] = (df_align['Y'] // grid_size) * grid_size

    df_anti['GridX'] = (df_anti['X'] // grid_size) * grid_size
    df_anti['GridY'] = (df_anti['Y'] // grid_size) * grid_size

    df_align = df_align.groupby(['GridY', 'GridX']).size().unstack(fill_value=0)
    df_anti = df_anti.groupby(['GridY', 'GridX']).size().unstack(fill_value=0)

    cmap = 'inferno'
    vmin = 0
    vmax = np.max(df_anti)

    sns.heatmap(df_align, cmap=cmap, annot=False,
                ax=axs[0], cbar=False, vmin=vmin,
                vmax=vmax)
    sns.heatmap(df_anti, cmap=cmap, annot=False,
                ax=axs[1], cbar=False, vmin=vmin,
                vmax=vmax)

    axs[0].set_title(f"Alignment")
    axs[0].set_xlabel("Grid X (pixels)")
    axs[0].set_ylabel("Grid Y (pixels)")

    axs[1].set_title(f"Anti-Alignment")
    axs[1].set_xlabel("Grid X (pixels)")
    axs[1].set_ylabel("Grid Y (pixels)")

    norm = plt.Normalize(vmin=vmin, vmax=vmax)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([]) 
    cbar = fig.colorbar(sm, ax=axs, orientation='horizontal', aspect=40)
    cbar.set_label('Count')

    plt.tight_layout()
    plt.suptitle("Heatmap of Kilobot Co-Ordinates in 20$\\times$20 Grid Squares for Alignment vs Anti-Alignment")
    plt.subplots_adjust(bottom=0.32, top=0.9)  
    plt.savefig("Results/HeatmapAlignAnti")   


def com_align_anti(df_align, df_anti):
    fig, axs = plt.subplots(1, 2, figsize=(14, 6))

    com_align = df_align[['TimeStep', 'CoMX', 'CoMY']]
    com_align = com_align.groupby('TimeStep')[['CoMX', 'CoMY']].mean()

    com_anti = df_anti[['TimeStep', 'CoMX', 'CoMY']]
    com_anti = com_anti.groupby('TimeStep')[['CoMX', 'CoMY']].mean()

    axs[0].plot(com_align['CoMX'], com_align['CoMY'], marker='o', label="CoM Alignment")
    axs[0].plot(com_anti['CoMX'], com_anti['CoMY'], marker='o', label="CoM Anti-Alignment")
    axs[0].set_title("Full Domain")
    axs[0].set_xlabel("X (pixels)")
    axs[0].set_ylabel("Y (pixels)")
    axs[0].set_xlim(0, 800)
    axs[0].set_ylim(0, 800)
    axs[0].grid()
    axs[0].legend()

    axs[1].plot(com_align['CoMX'], com_align['CoMY'], marker='o', label="CoM Alignment")
    axs[1].plot(com_anti['CoMX'], com_anti['CoMY'], marker='o', label="CoM Anti-Alignment")
    axs[1].set_title("Sub-Domain")
    axs[1].set_xlabel("X (pixels)")
    axs[1].set_ylabel("Y (pixels)")
    axs[1].grid()
    axs[1].legend()

    plt.tight_layout()
    plt.subplots_adjust(top=0.85)
    plt.suptitle("Center of Mass (CoM) Co-Ordinates over 100 second Simulation for Alignment vs Anti-Alignment Swarms")
    plt.savefig("Results/CoMTwoPlot")   
    

def vicsek_order_two_plot(df_data, df_names):
    fig, axs = plt.subplots(1, 2, figsize=(14, 8))

    for i, df in enumerate(df_data):

        vicsek_order = df[["TimeStep", "Theta"]]

        vicsek_order['Cos_Theta'] = np.cos(vicsek_order['Theta'])
        vicsek_order['Sin_Theta'] = np.sin(vicsek_order['Theta'])

        vicsek_order = vicsek_order.groupby('TimeStep')[['Cos_Theta', 'Sin_Theta']].mean()    
        vicsek_order['Norm'] = np.linalg.norm(vicsek_order[['Cos_Theta', 'Sin_Theta']], axis=1)

        mean_corr = np.mean(vicsek_order['Norm'])

        time = frames_to_milliseconds(np.array(vicsek_order.index, dtype=int))
        axs[i].plot(time, vicsek_order['Norm'], marker='o', linestyle='-', label="Current $v_a$")
        axs[i].axhline(y=mean_corr, color='red', linestyle='--', label=f"Average $v_a = {mean_corr:.3f}$")

        axs[i].set_title(f"{df_names[i]}")
        axs[i].set_xlabel("Time (ms)")
        axs[i].set_ylabel("$v_a$")
        axs[i].set_ylim([0, 1])
        axs[i].grid(True)
        axs[i].legend()
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.85)
    plt.suptitle("Time Series of Vicsek Order ($v_a$) of Alignment vs Anti-Alignment Swarms")   
    plt.savefig(f"Results/OrderTwoPlot.png")   


def theta_two_plot(df_data, df_names):
    fig, axs = plt.subplots(1, 2, subplot_kw={'projection': 'polar'}, figsize=(14, 6))

    for i, df in enumerate(df_data):

        theta = df[["Theta"]]
        num_bins = 16

        axs[i].set_theta_zero_location('E')
        axs[i].set_theta_direction(1)

        step = 2*math.pi/num_bins
        bins = np.arange(0, 2*math.pi + step, step)
        
        avg_theta = theta.mean()
        avg_theta = round(avg_theta[0], 2)
        axs[i].hist(theta, bins=bins, label=f"$\\theta$ count")
        axs[i].set_xticklabels([r'$0$', r'$\frac{\pi}{4}$', r'$\frac{\pi}{2}$', r'$\frac{3\pi}{4}$', r'$\pi$',
                        r'$\frac{5\pi}{4}$', r'$\frac{3\pi}{2}$', r'$\frac{7\pi}{4}$'])
        axs[i].set_title(f"{df_names[i]} ($\\theta_{{mean}} = {avg_theta}$)")
        axs[i].legend(loc='upper right')
    
    plt.tight_layout()
    plt.subplots_adjust(top=0.8)
    plt.suptitle("Distribution of Theta of Alignment vs Anti-Alignment Swarms")    
    plt.savefig(f"Results/ThetaTwoPlot.png")


def vicsek_order_one_plot(df_data, df_names):
    
    fig, axs = plt.subplots(figsize=(14, 8))
    colors = ['C0', 'C1']

    for i, df in enumerate(df_data):

        vicsek_order = df[["TimeStep", "Theta"]]

        vicsek_order['Cos_Theta'] = np.cos(vicsek_order['Theta'])
        vicsek_order['Sin_Theta'] = np.sin(vicsek_order['Theta'])

        vicsek_order = vicsek_order.groupby('TimeStep')[['Cos_Theta', 'Sin_Theta']].mean()    
        vicsek_order['Norm'] = np.linalg.norm(vicsek_order[['Cos_Theta', 'Sin_Theta']], axis=1)

        mean_corr = np.mean(vicsek_order['Norm'])

        time = frames_to_milliseconds(np.array(vicsek_order.index, dtype=int))
        plt.plot(time, vicsek_order['Norm'], marker='o', linestyle='-', label=f"{df_names[i]}")
        plt.axhline(y=mean_corr, linestyle='--', color=colors[i], label=f"Mean $v_a = {mean_corr:.3f}$")

    plt.title(("Time Series of Vicsek Order ($v_a$) of Alignment vs Anti-Alignment Swarms") )
    plt.xlabel("Time (ms)")
    plt.ylabel("$v_a$")
    plt.ylim([0, 1])
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.subplots_adjust(top=0.85)   
    plt.savefig(f"Results/OrderOnePlot.png")   


def theta_one_plot(df_data, df_names):
    
    fig, ax = plt.subplots(subplot_kw={'projection': 'polar'}, figsize=(9, 9))
    
    num_bins = 16
    step = 2*math.pi/num_bins
    bins = np.arange(0, 2*math.pi + step, step)
    avg_thetas = []
    
    for i, df in enumerate(df_data):
        
        theta = df[["Theta"]]
        avg_theta = theta.mean()
        avg_theta = round(avg_theta[0], 2)
        avg_thetas.append(avg_theta)

        ax.set_theta_zero_location('E')
        ax.set_theta_direction(1)

        ax.hist(theta, bins=bins, label=f"$\\theta_{{{df_names[i]}}}$", alpha=1-(i*0.25))

    ax.set_xticklabels([r'$0$', r'$\frac{\pi}{4}$', r'$\frac{\pi}{2}$', r'$\frac{3\pi}{4}$', r'$\pi$',
                    r'$\frac{5\pi}{4}$', r'$\frac{3\pi}{2}$', r'$\frac{7\pi}{4}$'])
    ax.set_title(f"Mean $\\theta_{{{df_names[0]}}} = {avg_thetas[0]}$, Mean $\\theta_{{{df_names[1]}}} = {avg_thetas[1]}$") 
    plt.suptitle("Distribution of $\\theta$ of Alignment vs Anti-Alignment Swarms")
    plt.legend(loc='center left', bbox_to_anchor=(0.05, 0.65))
    plt.tight_layout()
    plt.subplots_adjust(top=0.85)   
    plt.savefig(f"Results/ThetaOnePlot.png")
    
   
def heatmap_adjust_rates(df_all, df_rates): 
  
    grid_size = 20
    heatmaps = []
    cmap = 'inferno'

    for df in df_all:
        df['GridX'] = (df['X'] // grid_size) * grid_size
        df['GridY'] = (df['Y'] // grid_size) * grid_size
        
        heatmaps.append(df.groupby(['GridY', 'GridX']).size().unstack(fill_value=0))
        
    vmin = 0
    vmax = max(np.max(heatmap) for heatmap in heatmaps)

    fig, axs = plt.subplots(2, 2, figsize=(16, 16))
    
    for i, ax in enumerate(axs.flat):
        
        sns.heatmap(heatmaps[i], cmap=cmap, annot=False, ax=ax,
                    cbar=False, vmin=vmin, vmax=vmax)
        
        ax.invert_yaxis()
        ax.set_title(f"Adjust Rate {df_rates[i]}ms")
        ax.set_xlabel("Grid X (pixels)")
        ax.set_ylabel("Grid Y (pixels)")

    norm = plt.Normalize(vmin=vmin, vmax=vmax)
    sm = plt.cm.ScalarMappable(cmap=cmap, norm=norm)
    sm.set_array([])  # You can also pass the actual data here
    cbar = fig.colorbar(sm, ax=axs, orientation='horizontal', aspect=40)
    cbar.set_label('Count')

    plt.suptitle("Heatmap of Kilobot Co-Ordinates in 20$\\times$20 Grid Squares for varying Adjustment Rates")
    plt.tight_layout()
    plt.subplots_adjust(bottom=0.3)  
    plt.savefig("Results/HeatmapAdjust")  
  
  
def sequencing_error_plots(df_triangle, df_intensity):
    fig, axs = plt.subplots(1, 2, figsize=(14, 8))
    
    sequence_error_triangle = df_triangle[["TimeStep", "EstimateError"]]
    sequence_error_intensity = df_intensity[["TimeStep", "EstimateError"]]
    
    sequence_error_triangle = df_triangle.groupby('TimeStep').agg(
        average_error=('EstimateError', 'mean'),
        nan_count=('EstimateError', lambda x: x.isna().sum())
    )
    sequence_error_intensity = df_intensity.groupby('TimeStep').agg(
        average_error=('EstimateError', 'mean'),
        nan_count=('EstimateError', lambda x: x.isna().sum())
    )
    
    time = frames_to_milliseconds(np.array(sequence_error_triangle.index, dtype=int))
    
    axs[0].plot(time, sequence_error_triangle['average_error'], marker='x', color="red", label="Pattern Triangle")
    axs[0].plot(time, sequence_error_intensity['average_error'], marker='x', color="blue", label="Pattern Intensity")
    axs[0].set_title("Mean Absolute Error per Time Step")
    axs[0].set_xlabel("Time (ms)")
    axs[0].set_ylabel("Mean Error (Radians)")
    axs[0].grid(True)
    axs[0].legend()   
    
    axs[1].plot(time, sequence_error_triangle['nan_count'], marker='x', color="red", label="Pattern Triangle")
    axs[1].plot(time, sequence_error_intensity['nan_count'], marker='x', color="blue", label="Pattern Intensity")
    axs[1].set_title("Total NaN Count per Time Step")
    axs[1].set_xlabel("Time (ms)")
    axs[1].set_ylabel("Count")
    axs[1].grid(True)
    axs[1].legend()  
    
    plt.suptitle("Mean Absolute Error and NaN count for Triangle vs Intensity Patterns")
    plt.savefig("Results/PatternErrors.png")   


def kilobot_neighbor_plot(df, df_name, num_bots):
    
    num_unique = df["KilobotID"].nunique()
    id_array = [random.randint(0, num_unique) for _ in range(num_bots)]
    
    average_neighbor_count = df[["TimeStep", "Neighbors"]]
    average_neighbor_count = average_neighbor_count.groupby('TimeStep')['Neighbors'].mean()
    
    time = frames_to_milliseconds(np.array(average_neighbor_count.index, dtype=int))
    
    plt.figure(figsize=(12, 6))
    
    for bot_id in id_array:
        bot_neighbor_count = df.loc[df['KilobotID'] == bot_id, 'Neighbors']
        
        # Plot the time series of alignment correlation
        plt.plot(time, bot_neighbor_count, marker='o', linestyle='-', label=f"ID: {bot_id}")
        
    plt.plot(time, average_neighbor_count, marker='o', linestyle="-", label="Mean Total Count",
             color="black")

    plt.title(f"Time Series of Kilobot Detected Neighbours ({df_name})")
    plt.xlabel("Time (ms)")
    plt.ylabel("Count")
    plt.grid(True)
    plt.legend()
    plt.savefig(f"Results/Neighbour{df_name}.png")    
   
     
# df_one = pd.read_csv("Data\Simulation\sim_data_one_bot.csv")

# one_bot_path(df_one)

# df_align = pd.read_csv("Data\Simulation\sim_data_alignment.csv")
# df_anti = pd.read_csv("Data\Simulation\sim_data_anti-alignment.csv")
# df_data = [df_align, df_anti]
# df_names = ["Alignment", "Anti-Alignment"]

# heatmap_align_anti(df_align, df_anti)
# com_align_anti(df_align, df_anti)
# vicsek_order_two_plot(df_data, df_names)
# theta_two_plot(df_data, df_names)
# vicsek_order_one_plot(df_data, df_names)
# theta_one_plot(df_data, df_names)
# kilobot_neighbor_plot(df=df_align, df_name="Alignment", num_bots=5)
# kilobot_neighbor_plot(df=df_anti, df_name="Anti-Alignment", num_bots=5)

# df_1000 = pd.read_csv("Data/Simulation/sim_data_adjust_1000.csv")
# df_2500 = pd.read_csv("Data/Simulation/sim_data_anti-alignment.csv")
# df_5000 = pd.read_csv("Data/Simulation/sim_data_adjust_5000.csv")
# df_10000 = pd.read_csv("Data/Simulation/sim_data_adjust_10000.csv")
# df_all = [df_1000, df_2500, df_5000, df_10000]
# df_rates = [1000, 2500, 5000, 10000]

# heatmap_adjust_rates(df_all, df_rates)

# df_triangle = pd.read_csv("Data\Simulation\sim_data_triangle_pattern.csv")
# df_intensity = pd.read_csv("Data\Simulation\sim_data_intensity_pattern.csv")

# sequencing_error_plots(df_triangle, df_intensity)

