"""
PyTune Box - UI Themes

Color theme dictionaries and helpers for light and dark mode.
"""

LIGHT_THEME = {
    "name": "light",
    "bg": "#f4f4f4",
    "fg": "#111111",
    "frame_bg": "#ffffff",
    "label_bg": "#ffffff",
    "label_fg": "#111111",
    "button_bg": "#e6e6e6",
    "button_fg": "#111111",
    "entry_bg": "#ffffff",
    "entry_fg": "#111111",
    "listbox_bg": "#ffffff",
    "listbox_fg": "#111111",
    "select_bg": "#cce5ff",
    "select_fg": "#000000",
    "status_bg": "#e8e8e8",
    "status_fg": "#111111",
    "visualizer_bg": "#ffffff",
    "visualizer_bar": "#3a7bd5",
}

DARK_THEME = {
    "name": "dark",
    "bg": "#1e1e1e",
    "fg": "#f5f5f5",
    "frame_bg": "#2d2d2d",
    "label_bg": "#2d2d2d",
    "label_fg": "#f5f5f5",
    "button_bg": "#3a3a3a",
    "button_fg": "#f5f5f5",
    "entry_bg": "#252525",
    "entry_fg": "#f5f5f5",
    "listbox_bg": "#252525",
    "listbox_fg": "#f5f5f5",
    "select_bg": "#4a6984",
    "select_fg": "#ffffff",
    "status_bg": "#111111",
    "status_fg": "#f5f5f5",
    "visualizer_bg": "#1b1b1b",
    "visualizer_bar": "#4fc3f7",
}


def get_theme(theme_name):
    """Return the theme dictionary for the given theme name."""
    if theme_name == "dark":
        return DARK_THEME.copy()
    return LIGHT_THEME.copy()


def get_next_theme_name(current_theme_name):
    """Return the opposite theme name for toggling."""
    if current_theme_name == "dark":
        return "light"
    return "dark"
