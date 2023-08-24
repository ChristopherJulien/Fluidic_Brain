import numpy as np
import matplotlib.pyplot as plt
from matplotlib.widgets import Slider
import matplotlib.pyplot as plt
import numpy as np

angle = np.linspace(0, 12*np.pi, 1000)  # Generate x values

K = 1
# L = 2.27*2 #cm
L = 1  # cm)
# R = L/2

# Define the equation


def x_equation(angle):
    # Example equation, you can replace it with your own
    return (L/angle) * np.sin(angle/2)


def y_equation(angle):
    # Example equation, you can replace it with your own
    return -(L) * np.cos(angle/2)


# Create a figure and axes
fig, ax = plt.subplots()
# Adjust the bottom margin to make room for the slider
plt.subplots_adjust(bottom=0.35)

# Plot the graph
line, = ax.plot(x_equation(angle), y_equation(angle), label='Equation')
point, = ax.plot([], [], 'ro', label='Point')

# Slider position and size
slider_ax = plt.axes([0.25, 0.1, 0.65, 0.03])

# Create the slider
slider = Slider(slider_ax, 'radians', 0, 12*np.pi, valinit=0)

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
ax.axis('equal')

# Add a legend for K and L values
legend_text = 'K = {}\nL = {}'.format(K, L)
ax.legend([line, point], ['Equation', 'Point'],
          loc='upper right', title=legend_text)

plt.show()


# matplot lib librarr FANCY ARROW
