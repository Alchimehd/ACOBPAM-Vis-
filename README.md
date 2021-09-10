# ACOBPAM-Vis

This script is a Gtk3+ visualizer for the plugin ACOBPAM in ProM 6; the de facto standard framework for Process Mining. It allows to visualize Behavioral Patterns and their relationships specified within the JSON file outputted by the plugin.

It is based on the [xdot module](https://github.com/jrfonseca/xdot.py).

Follow the instructions in [xdot module](https://github.com/jrfonseca/xdot.py) to install.

# Screenshots

![unzoomed view](https://github.com/Alchimehd/ACOBPAM-Vis-/blob/main/s1.png)
![zoomed view](https://github.com/Alchimehd/ACOBPAM-Vis-/blob/main/s2.png)

# Features
- Nodes represent patterns that are drawn inside. Their size depends on their support which can be seen when hovering.
- Relationships are visible in different colors/shapes specified in the legend.
- Relationships can be enabled/disabled and their thresholds modified interactively. The modifications on the graph are seen in real time.

Plus the xdot module features:

- Since it doesn't use bitmaps it is fast and has a small memory footprint.
- Arbitrary zoom.
- Keyboard/mouse navigation.
- Animated jumping between nodes.
- Highlights node/edge under mouse.
