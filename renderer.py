"""
Real-time animation using matplotlib.
"""

import time

import matplotlib
import matplotlib.pyplot as plt
import numpy as np


# https://matplotlib.org/stable/users/explain/animations/blitting.html
class Renderer:
    def __init__(
        self,
        title=None,
        xlabel=None,
        ylabel=None,
        xlim=[-1.5, 1.5],
        ylim=None,
        hide_axis=False,
        tight=False,
        enable_grid=False,
        enable_legend=False,
    ):
        matplotlib.rcParams["toolbar"] = "None"
        self.fig = plt.figure()
        self.ax = self.fig.add_subplot()

        if ylim is None:
            ylim = xlim

        self.ax.set_xlim(xlim)
        self.ax.set_ylim(ylim)
        self.ax.set_aspect("equal", adjustable="box")

        self.ax.set_title(title)
        self.ax.set_xlabel(xlabel)
        self.ax.set_ylabel(ylabel)

        if hide_axis:
            self.ax.set_axis_off()

        # See https://stackoverflow.com/a/47893499
        if tight:
            self.fig.tight_layout(pad=0)
            w, h = self.fig.get_size_inches()
            x1, x2 = self.ax.get_xlim()
            y1, y2 = self.ax.get_ylim()
            self.fig.set_size_inches(
                2 * 1.08 * w, 2 * self.ax.get_aspect() * (y2 - y1) / (x2 - x1) * w
            )

        if enable_grid:
            self.ax.grid()

        # Enabling legend will slow down rendering
        self.enable_legend = enable_legend

        self.plot_dict = {}

        plt.show(block=False)
        plt.pause(0.1)
        self.bg = self.fig.canvas.copy_from_bbox(self.fig.bbox)

    def register_item(self, label, m="o", alpha=1, legend_label=None):
        if legend_label is not None:
            (points,) = self.ax.plot(
                [], [], m, alpha=alpha, animated=True, label=legend_label
            )
        else:
            (points,) = self.ax.plot([], [], m, alpha=alpha, animated=True)
        self.plot_dict[label] = points

    def start_drawing(self):
        self.fig.canvas.restore_region(self.bg)

    def draw_item(self, label, x, y):
        if label not in self.plot_dict:
            raise ValueError(f"Plot {label} not registered")
        self.plot_dict[label].set_data(x, y)
        self.ax.draw_artist(self.plot_dict[label])

    def end_drawing(self, delay=0):
        if self.enable_legend:
            self.ax.draw_artist(self.ax.legend())
        self.fig.canvas.blit(self.fig.bbox)
        self.fig.canvas.flush_events()

        if delay > 0:
            plt.pause(delay)


class SimpleRenderer(Renderer):
    def __init__(
        self,
        title=None,
        xlabel=None,
        ylabel=None,
        xlim=[-1.5, 1.5],
        ylim=None,
        hide_axis=False,
        tight=False,
        enable_grid=False,
        m="o",
        alpha=1,
    ):
        super().__init__(
            title=title,
            xlabel=xlabel,
            ylabel=ylabel,
            xlim=xlim,
            ylim=ylim,
            hide_axis=hide_axis,
            tight=tight,
            enable_grid=enable_grid,
            enable_legend=False,
        )

        self.register_item("default", m=m, alpha=alpha)

    def draw(self, x, y):
        self.start_drawing()
        self.draw_item("default", x, y)
        self.end_drawing()


if __name__ == "__main__":
    renderer_choice = input("Choose renderer (normal/simple): ")
    if renderer_choice not in ["normal", "simple"]:
        raise ValueError("Invalid renderer choice")

    if renderer_choice == "normal":
        r = Renderer("Dots circling", enable_legend=True)
        r.register_item("dots", legend_label="Item 1")
        r.register_item("lines", m="-", legend_label="Item 2")
    else:
        r = SimpleRenderer("Dots circling")

    def draw(x, y):
        if renderer_choice == "normal":
            r.start_drawing()
            r.draw_item("dots", x, y)
            r.draw_item("lines", x, y)
            r.end_drawing()
        else:
            r.draw(x, y)

    frame_count = 500
    num_dots = 15
    speed = 0.01

    tic = time.time()
    for i in range(frame_count):
        t = (2 * np.pi / num_dots) * np.arange(num_dots)
        t += i * speed

        x = np.cos(t) * np.cos(4 * t)
        y = np.sin(t) * np.cos(4 * t)

        draw(x, y)

    print(f"Average FPS: {frame_count / (time.time() - tic)}")
