import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib.animation import FuncAnimation

data = np.load('data_20230817_201340.npy')

# Define the connections between points as pairs of indices
connections = [(0,1), (1,2), (2,3), (3,4), (0,5),
                (5,9), (9,13), (13,17), (17,0),
                (5,6), (6,7), (7,8), (9,10), (10,11),
                (11,12), (13,14), (14,15), (15,16),
                (17,18), (18,19), (19,20)]  # Replace with your desired connections


# Set up the figure and 3D axes
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')

def init():
    return []

def update(frame):
    ax.clear()
    ax.set_title(f"Frame {frame + 1}")
    ax.set_xlim(0, 1)
    ax.set_ylim(0, 1)
    ax.set_zlim(0, 1)
    ax.scatter(data[frame, :, 0], data[frame, :, 1], data[frame, :, 2], marker='o')
    # ax.scatter(data[frame, :, 2], data[frame, :, 0], data[frame, :, 1], marker='o')

     # Plot lines connecting specified points
    for connection in connections:
        point1 = data[frame, connection[0], :]
        point2 = data[frame, connection[1], :]
        ax.plot([point1[0], point2[0]], [point1[1], point2[1]], [point1[2], point2[2]], color='red')


num_frames = data.shape[0]
ani = FuncAnimation(fig, update, frames=num_frames, init_func=init, repeat=True)

plt.show()
