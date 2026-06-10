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
    "border_color": "#cbd5e1",
    "visualizer_bg": "#ffffff",
    "visualizer_bar": "#6366f1",
    "tab_bg": "#e2e8f0",
    "tab_selected_bg": "#ffffff",
}

DARK_THEME = {
    "name": "dark",
    "bg": "#0b0f19",
    "fg": "#e8edf5",
    "frame_bg": "#0b0f19",
    "label_bg": "#0b0f19",
    "label_fg": "#e8edf5",
    "button_bg": "#0b0f19",
    "button_fg": "#e8edf5",
    "entry_bg": "#ffffff",
    "entry_fg": "#0f172a",
    "listbox_bg": "#0b0f19",
    "listbox_fg": "#e8edf5",
    "select_bg": "#3b82f6",
    "select_fg": "#ffffff",
    "status_bg": "#0b0f19",
    "status_fg": "#94a3b8",
    "border_color": "#d1d5db",
    "visualizer_bg": "#0b0f19",
    "visualizer_bar": "#3b82f6",
    "tab_bg": "#1a2233",
    "tab_selected_bg": "#2a3548",
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
