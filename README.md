# Usage

```py
# Use Renderer for drawing different plots in multiple steps
r = Renderer("Dots circling", enable_legend=True)
r.register_item("dots", legend_label="Item 1")
r.register_item("lines", m="-", legend_label="Item 2")

frame_count = 500
for i in range(frame_count):
    t = (2 * np.pi / 5) * np.arange(5)
    t += i * 0.01

    x = np.cos(t) * np.cos(4 * t)
    y = np.sin(t) * np.cos(4 * t)

    r.start_drawing()
    r.draw_item("dots", x, y)
    r.draw_item("lines", x, y)
    r.end_drawing()

# Use SimpleRenderer for drawing a single plot in one step
r = SimpleRenderer("Dots circling")

frame_count = 500
for i in range(frame_count):
    t = (2 * np.pi / 5) * np.arange(5)
    t += i * 0.01

    x = np.cos(t) * np.cos(4 * t)
    y = np.sin(t) * np.cos(4 * t)

    r.draw(x, y)
```