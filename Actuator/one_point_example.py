import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider

a = np.linspace(0, np.pi, 1000)  # Generate x values

K = 1
L = 1

# Define the equation
def x_equation(a):
    return (2/K) * np.sin(a/2)  # Example equation, you can replace it with your own

def y_equation(a):
    return (np.pi/K) * np.cos(a/2)  # Example equation, you can replace it with your own

# Create a figure and axes
fig, ax = plt.subplots()
plt.subplots_adjust(bottom=0.25)  # Adjust the bottom margin to make room for the slider

# Plot the graph
line, = ax.plot(x_equation(a), y_equation(a), label='Equation')
point, = ax.plot([], [], 'ro', label='Point')

# Slider position and size
slider_ax = plt.axes([0.25, 0.1, 0.65, 0.03])

# Create the slider
slider = Slider(slider_ax, 'angle', 0, np.pi, valinit=0)

# Update the plot when the slider value changes
def update(val):
    a_value = slider.val
    x_value = x_equation(a_value)
    y_value = y_equation(a_value)

    point.set_data(x_value, y_value)
    plt.title('angle = {:.2f}'.format(a_value))
    fig.canvas.draw_idle()

slider.on_changed(update)

# Set labels and legend
ax.set_xlabel('x')
ax.set_ylabel('y')

# Add a legend for K and L values
legend_text = 'K = {}\nL = {}'.format(K, L)
ax.legend([line, point], ['Equation', 'Point'], loc='upper right', title=legend_text)

plt.show()
