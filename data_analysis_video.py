import pandas as pd
import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

plt.rcParams.update({"text.usetex": True, 'font.size': 14})


x_csv, y_csv = "Data/x.csv", "Data/y.csv"
x_df = pd.read_csv(x_csv, header=None)
y_df = pd.read_csv(y_csv, header=None)

# # Select the object to animate, here we choose the first object (column 0)
# x_data = x_df[0]
# y_data = y_df[0]

# fig, ax = plt.subplots()
# line, = ax.plot([], [])  # Line plot with red circles

# def init():
#     ax.set_xlim(min(x_data) - 1, max(x_data) + 1)
#     ax.set_ylim(min(y_data) - 1, max(y_data) + 1)
#     return line,

# def update(frame):
#     line.set_data(x_data[:frame+1], y_data[:frame+1])
#     return line,

# ani = FuncAnimation(fig, update, frames=len(x_data), init_func=init, blit=True, interval=10)

# plt.show()

# Plot the paths
plt.figure(figsize=(10, 6))

for column in x_df.columns:
    plt.plot(x_df[column], y_df[column], label=f"Kilobot {column}")
    
plt.xlim(600, 1000)
plt.ylim(200, 800)
plt.xlabel('X (mm)')
plt.ylabel('Y (mm)')
plt.title('Paths of two Kilobots conducting Run and Tumble motion')
plt.legend()
plt.grid(True)
plt.savefig("Results/KilobotVideoTrackerAnalysis.png")
plt.show()



