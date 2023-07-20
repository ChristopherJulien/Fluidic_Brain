import matplotlib.pyplot as plt
from matplotlib.animation import FuncAnimation

# Define the function to visualize
def f(x):
    return x ** 2

# Define the range of variables
x_values = range(-10, 11)

# Initialize the figure and axis
fig, ax = plt.subplots()
line, = ax.plot([], [], 'r-', lw=2)

# Set up the axis labels and limits
ax.set_xlim(min(x_values), max(x_values))
ax.set_ylim(0, max(f(x) for x in x_values) + 10)
ax.set_xlabel('x')
ax.set_ylabel('f(x)')

# Initialization function for the animation
def init():
    line.set_data([], [])
    return line,

# Animation update function
def update(frame):
    x = x_values[frame]
    y = f(x)
    line.set_data([x], [y])
    return line,

# Create the animation
animation = FuncAnimation(fig, update, frames=len(x_values),
                          init_func=init, blit=True)

# Show the animation
plt.show()
