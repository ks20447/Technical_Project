import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.rcParams.update({"text.usetex": True, 'font.size': 16})

x_csv, y_csv = "Data/Video/x.csv", "Data/Video/y.csv"
x_df = pd.read_csv(x_csv, header=None)
y_df = pd.read_csv(y_csv, header=None)


def animated_plot(x_df, y_df):
    # Select the object to animate, here we choose the first and second objects (column 0 and 1)
    x_data_1 = x_df[0]
    y_data_1 = y_df[0]
    x_data_2 = x_df[1]
    y_data_2 = y_df[1] 

    fig, ax = plt.subplots()
    line_1, = ax.plot([], [], 'r-')  # Initialized line plot
    line_2, = ax.plot([], [], 'b-')  

    min_x = x_df.min().min() - 1
    min_y = y_df.min().min() - 1
    max_x = x_df.max().max() + 1
    max_y = y_df.max().max() + 1


    def init():
        ax.set_xlim(min_x, max_x)
        ax.set_ylim(min_y, max_y)
        plt.title("Animation of Video Tracked Kilobots")
        plt.grid(True)
        plt.xlabel('X (mm)')
        plt.ylabel('Y (mm)')      
        return line_1, line_2


    def update(frame):
        line_1.set_data(x_data_1[:frame+1], y_data_1[:frame+1])
        line_2.set_data(x_data_2[:frame+1], y_data_2[:frame+1])
    
        
        return line_1, line_2

    ani = FuncAnimation(fig, update, frames=len(x_data_1), init_func=init, blit=True, interval=10)

     # Save the animation as an MP4 file
    ani.save('Results/KilobotVideoTrackAnimation.gif')


def static_plot(x_df, y_df):

    # Plot the paths
    fig, axs = plt.subplots(1, 2, figsize=(14, 8))

    for ax in axs:
        for column in x_df.columns:
            ax.plot(x_df[column], y_df[column])
            ax.plot(x_df[column].iloc[0], y_df[column].iloc[0], color="green", marker='o', markersize=10)
            ax.plot(x_df[column].iloc[-1], y_df[column].iloc[-1], color="red", marker='o', markersize=10)
            ax.set_xlabel('X (mm)')
            ax.set_ylabel('Y (mm)')
            ax.grid(True)
        

    axs[1].invert_yaxis()
    axs[1].legend(["Kilobot 1", "Start", "End", "Kilobot 2"])
    axs[1].set_title("Sub-Domain")
    axs[0].set_xlim(0, 1800)
    axs[0].set_ylim(1000, 0)
    axs[0].legend(["Kilobot 1", "Start", "End", "Kilobot 2"])
    axs[0].set_title("Full Domain")
    plt.suptitle('Paths of two Kilobots conducting Run and Tumble motion')
    plt.savefig("Results/KilobotVideoTrackPlot.png")


# static_plot(x_df, y_df)
# animated_plot(x_df, y_df)

