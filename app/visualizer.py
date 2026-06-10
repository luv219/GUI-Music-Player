"""
PyTune Box - Audio Visualizer

Simple animated bar visualizer using Tkinter Canvas.
"""

import random
import tkinter as tk


class AudioVisualizer:
    """Displays a simulated bar animation on a Tkinter Canvas."""

    def __init__(self, parent, width=500, height=90, bar_count=32):
        """Initialize the visualizer canvas and bars."""
        self.parent = parent
        self.width = width
        self.height = height
        self.bar_count = bar_count

        self.canvas = tk.Canvas(
            parent,
            width=width,
            height=height,
            highlightthickness=0,
            bd=0,
        )

        self.is_running = False
        self.animation_job = None
        self.bar_items = []
        self.theme = {}
        self.bg_color = "#ffffff"
        self.bar_color = "#3a7bd5"

        self.current_levels = [random.uniform(0.05, 0.2) for _ in range(bar_count)]
        self.target_levels = [random.uniform(0.05, 0.2) for _ in range(bar_count)]

        self.canvas.bind("<Configure>", self.on_resize)
        self.create_bars()

    def get_widget(self):
        """Return the canvas widget for layout."""
        return self.canvas

    def create_bars(self):
        """Create vertical bars on the canvas."""
        self.canvas.delete("all")
        self.bar_items = []

        if self.width <= 0 or self.height <= 0 or self.bar_count <= 0:
            return

        padding = 8
        usable_width = max(self.width - (padding * 2), 1)
        gap = 2
        bar_width = max((usable_width - (gap * (self.bar_count - 1))) / self.bar_count, 2)

        for index in range(self.bar_count):
            x1 = padding + index * (bar_width + gap)
            x2 = x1 + bar_width
            y2 = self.height - padding
            y1 = y2 - 4

            bar_id = self.canvas.create_rectangle(
                x1,
                y1,
                x2,
                y2,
                fill=self.bar_color,
                outline="",
            )
            self.bar_items.append(bar_id)

        self.safe_configure_canvas(bg=self.bg_color)

    def start(self):
        """Start the visualizer animation."""
        if self.is_running:
            return

        self.is_running = True
        self.animate()

    def pause(self):
        """Pause the visualizer animation."""
        self.is_running = False

        if self.animation_job is not None:
            try:
                self.canvas.after_cancel(self.animation_job)
            except tk.TclError:
                pass
            self.animation_job = None

    def stop(self):
        """Stop the visualizer and reset bars to low height."""
        self.pause()

        self.current_levels = [0.05 for _ in range(self.bar_count)]
        self.target_levels = [0.05 for _ in range(self.bar_count)]
        self.update_bars()

    def animate(self):
        """Animate bars with smooth level changes."""
        if not self.is_running:
            return

        for index in range(self.bar_count):
            if random.random() < 0.25:
                self.target_levels[index] = random.uniform(0.08, 1.0)

            current = self.current_levels[index]
            target = self.target_levels[index]
            self.current_levels[index] = (current * 0.65) + (target * 0.35)

        self.update_bars()

        self.animation_job = self.canvas.after(100, self.animate)

    def update_bars(self):
        """Update bar heights based on current levels."""
        if not self.bar_items or self.width <= 0 or self.height <= 0:
            return

        padding = 8
        usable_width = max(self.width - (padding * 2), 1)
        usable_height = max(self.height - (padding * 2), 1)
        gap = 2
        bar_width = max((usable_width - (gap * (self.bar_count - 1))) / self.bar_count, 2)

        for index, bar_id in enumerate(self.bar_items):
            level = max(0.0, min(1.0, self.current_levels[index]))
            bar_height = max(4, int(usable_height * level))

            x1 = padding + index * (bar_width + gap)
            x2 = x1 + bar_width
            y2 = self.height - padding
            y1 = y2 - bar_height

            try:
                self.canvas.coords(bar_id, x1, y1, x2, y2)
                self.canvas.itemconfig(bar_id, fill=self.bar_color)
            except tk.TclError:
                pass

    def apply_theme(self, theme):
        """Apply theme colors to the visualizer."""
        self.theme = theme or {}

        self.bg_color = self.theme.get(
            "visualizer_bg",
            self.theme.get("frame_bg", self.theme.get("bg", "#ffffff")),
        )
        self.bar_color = self.theme.get(
            "visualizer_bar",
            self.theme.get("fg", "#111111"),
        )

        self.safe_configure_canvas(bg=self.bg_color)
        self.update_bars()

    def on_resize(self, event):
        """Handle canvas resize events."""
        if event.width <= 0 or event.height <= 0:
            return

        self.width = event.width
        self.height = event.height
        self.create_bars()
        self.update_bars()

    def safe_configure_canvas(self, **kwargs):
        """Safely configure the canvas."""
        try:
            self.canvas.configure(**kwargs)
        except tk.TclError:
            pass
        except Exception:
            pass
