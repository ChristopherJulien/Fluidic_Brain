import numpy as np
import matplotlib.pyplot as plt
# import MouseEvents as me


class BlittedCursor:
    """
    A cross-hair cursor using blitting for faster redraw.
    """

    def __init__(self, ax):
        self.ax = ax
        self.background = None
        self.horizontal_line = ax.axhline(color='k', lw=0.8, ls='--')
        self.vertical_line = ax.axvline(color='k', lw=0.8, ls='--')
        # text location in axes coordinates
        self.text = ax.text(0.72, 0.9, '', transform=ax.transAxes)
        self._creating_background = False
        ax.figure.canvas.mpl_connect('draw_event', self.on_draw)

    def on_draw(self, event):
        self.create_new_background()

    def set_cross_hair_visible(self, visible):
        need_redraw = self.horizontal_line.get_visible() != visible
        self.horizontal_line.set_visible(visible)
        self.vertical_line.set_visible(visible)
        self.text.set_visible(visible)
        return need_redraw

    def create_new_background(self):
        if self._creating_background:
            # discard calls triggered from within this function
            return
        self._creating_background = True
        self.set_cross_hair_visible(False)
        self.ax.figure.canvas.draw()
        self.background = self.ax.figure.canvas.copy_from_bbox(self.ax.bbox)
        self.set_cross_hair_visible(True)
        self._creating_background = False

    def on_mouse_move(self, event):
        if self.background is None:
            self.create_new_background()
        if not event.inaxes:
            need_redraw = self.set_cross_hair_visible(False)
            if need_redraw:
                self.ax.figure.canvas.restore_region(self.background)
                self.ax.figure.canvas.blit(self.ax.bbox)
        else:
            self.set_cross_hair_visible(True)
            # update the line positions
            x, y = event.xdata, event.ydata
            self.horizontal_line.set_ydata([y])
            self.vertical_line.set_xdata([x])
            self.text.set_text('x=%1.2f, y=%1.2f' % (x, y))

            self.ax.figure.canvas.restore_region(self.background)
            self.ax.draw_artist(self.horizontal_line)
            self.ax.draw_artist(self.vertical_line)
            self.ax.draw_artist(self.text)
            self.ax.figure.canvas.blit(self.ax.bbox)


x = np.arange(0, 1, 0.01)
y = np.sin(2 * 2 * np.pi * x)

fig, ax = plt.subplots()
ax.set_title('Blitted cursor')
ax.plot(x, y, 'o')
blitted_cursor = BlittedCursor(ax)
fig.canvas.mpl_connect('motion_notify_event', blitted_cursor.on_mouse_move)

# Simulate a mouse move to (0.5, 0.5), needed for online docs
t = ax.transData
MouseEvent(
    "motion_notify_event", ax.figure.canvas, *t.transform((0.5, 0.5))
)._process()

# import numpy as np
# import matplotlib.pyplot as plt
# import matplotlib.animation as animation
# from matplotlib.patches import ConnectionPatch

# fig, (axl, axr) = plt.subplots(
#     ncols=2,
#     sharey=True,
#     figsize=(6, 2),
#     gridspec_kw=dict(width_ratios=[1, 3], wspace=0),
# )
# axl.set_aspect(1)
# axr.set_box_aspect(1 / 3)
# axr.yaxis.set_visible(False)
# axr.xaxis.set_ticks([0, np.pi, 2 * np.pi], ["0", r"$\pi$", r"$2\pi$"])

# # draw circle with initial point in left Axes
# x = np.linspace(0, 2 * np.pi, 50)
# axl.plot(np.cos(x), np.sin(x), "k", lw=0.3)
# point, = axl.plot(0, 0, "o")

# # draw full curve to set view limits in right Axes
# sine, = axr.plot(x, np.sin(x))

# # draw connecting line between both graphs
# con = ConnectionPatch(
#     (1, 0),
#     (0, 0),
#     "data",
#     "data",
#     axesA=axl,
#     axesB=axr,
#     color="C0",
#     ls="dotted",
# )
# fig.add_artist(con)


# def animate(i):
#     x = np.linspace(0, i, int(i * 25 / np.pi))
#     sine.set_data(x, np.sin(x))
#     x, y = np.cos(i), np.sin(i)
#     point.set_data([x], [y])
#     con.xy1 = x, y
#     con.xy2 = i, y
#     return point, sine, con


# ani = animation.FuncAnimation(
#     fig,
#     animate,
#     interval=50,
#     blit=False,  # blitting can't be used with Figure artists
#     frames=x,
#     repeat_delay=100,
# )

# plt.show()
