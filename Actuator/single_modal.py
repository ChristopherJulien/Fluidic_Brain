import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# create a figure and axes
fig = plt.figure(figsize=(12,5))
ax1 = plt.subplot(1,2,1)   
ax2 = plt.subplot(1,2,2)
# set up the subplots as needed
ax1.set_xlim(( 0, 2))            
ax1.set_ylim((-2, 2))
ax1.set_xlabel('Time')
ax1.set_ylabel('Angle')
ax2.set_xlim((-2,2))
ax2.set_ylim((-2,2))
ax2.set_xlabel('X')
ax2.set_ylabel('Y')
ax2.set_title('Phase Plane')
# Create objects that will change in the animation. 
# Initially empty, have new values in the animation.
# matplotib basic colors for point: k for black, w for white
# matplotib css colors for lines: silver, tan, grey 
txt_title = ax1.set_title('Some Title')
line1, = ax1.plot([], [], 'silver', lw=2)     
# ax.plot returns a list of 2D line objects
line2, = ax1.plot([], [], 'tan', lw=2)
pt1, = ax2.plot([], [], 'k.', ms=20)
line3, = ax2.plot([], [], 'grey', lw=2)
ax1.legend(['sin','cos'])

K = 1
L = 1
q = 1

def drawframe(n):
    x = np.linspace(0, 2*np.pi,1000)
    r1 = np.sin(x - 0.1 * n)
    r2 = np.cos(x - 0.1 * n)

    # r2 = (np.pi/K) * np.cos(((x - 0.1 * n)/2))
    # r1 = (2/K) * np.sin((x - 0.1 * n)/2)
    # r2 = (np.pi/K) * np.cos(((x - 0.1 * n)/2))
    # r2 = (np.pi/k)*np.cos(2 * np.pi * (x - 0.01 * n))

    line1.set_data(x, r1)
    line2.set_data(x, r2)
    line3.set_data(r1[0:50],r2[0:50])
    pt1.set_data(r1[0],r2[0])
    txt_title.set_text('Frame = {0:4d}'.format(n))
    return (line1,line2)

from matplotlib import animation
# blit=True updates only the changed parts
anim = animation.FuncAnimation(fig, drawframe, frames=100, interval=20, blit=True )

# 1. render and display the desired animation by HTML
from IPython.display import HTML
HTML(anim.to_html5_video())
# 2. render and display the desired animation by rc
from matplotlib import rc
# equivalent to rcParams['animation.html'] = 'html5'
rc('animation', html='html5')
anim

from matplotlib.animation import FuncAnimation, PillowWriter
# save animation at 20 frames per second 
anim.save("graph.gif", dpi=250, writer=PillowWriter(fps=20))
