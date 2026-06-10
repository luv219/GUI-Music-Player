"""
PyTune Box - UI Themes

Color theme dictionaries and helpers for light and dark mode.
"""

LIGHT_THEME = {
    "name": "light",
    "bg": "#f8fafc",
    "fg": "#0f172a",
    "frame_bg": "#ffffff",
    "label_bg": "#ffffff",
    "label_fg": "#0f172a",
    "button_bg": "#f1f5f9",
    "button_fg": "#334155",
    "entry_bg": "#ffffff",
    "entry_fg": "#0f172a",
    "listbox_bg": "#ffffff",
    "listbox_fg": "#0f172a",
    "select_bg": "#3b82f6",
    "select_fg": "#ffffff",
    "status_bg": "#f1f5f9",
    "status_fg": "#475569",
    "visualizer_bg": "#ffffff",
    "visualizer_bar": "#6366f1",
}

DARK_THEME = {
    "name": "dark",
    "bg": "#090d16",
    "fg": "#f8fafc",
    "frame_bg": "#151c2c",
    "label_bg": "#151c2c",
    "label_fg": "#f8fafc",
    "button_bg": "#222e47",
    "button_fg": "#f8fafc",
    "entry_bg": "#090d16",
    "entry_fg": "#f8fafc",
    "listbox_bg": "#0c111d",
    "listbox_fg": "#f8fafc",
    "select_bg": "#3b82f6",
    "select_fg": "#ffffff",
    "status_bg": "#05080e",
    "status_fg": "#94a3b8",
    "visualizer_bg": "#0c111d",
    "visualizer_bar": "#3b82f6",
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
