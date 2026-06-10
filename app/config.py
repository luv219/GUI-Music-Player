"""
PyTune Box - Application Configuration

Basic constants used across the application.
"""

APP_NAME = "PyTune Box"
APP_DISPLAY_NAME = "PyTune Box"
APP_EXECUTABLE_NAME = "PyTuneBox"
APP_VERSION = "0.1.0"
APP_RELEASE_STAGE = "beta"
APP_AUTHOR = "PyTune Box Project"

WINDOW_WIDTH = 900
WINDOW_HEIGHT = 600
MIN_WINDOW_WIDTH = 700
MIN_WINDOW_HEIGHT = 450

SUPPORTED_AUDIO_EXTENSIONS = [".mp3", ".wav", ".ogg"]

DEFAULT_VOLUME = 70

SETTINGS_FILE = "data/settings.json"

AVAILABLE_THEMES = ["light", "dark"]

DEFAULT_THEME = "light"

AUDIO_FILE_TYPES = [
    ("Audio Files", "*.mp3 *.wav *.ogg"),
    ("MP3 Files", "*.mp3"),
    ("WAV Files", "*.wav"),
    ("OGG Files", "*.ogg"),
    ("All Files", "*.*"),
]

PLAYLIST_PLACEHOLDER_ITEMS = [
    "Playlist is empty",
    "Use File > Open Files or Open Folder",
]

PLAYLIST_FILE_TYPES = [
    ("PyTune Box Playlist", "*.json"),
    ("JSON Files", "*.json"),
    ("All Files", "*.*"),
]

DEFAULT_PLAYLIST_DIR = "data/playlists"

PLAYLIST_JSON_VERSION = "1.0"

REPEAT_MODES = ["off", "one", "all"]

DEFAULT_REPEAT_MODE = "off"

DEFAULT_SHUFFLE = False

KEYBOARD_SHORTCUTS = {
    "play_pause": "space",
    "stop": "s",
    "next": "Right",
    "previous": "Left",
    "shuffle": "h",
    "repeat": "r",
    "open_files": "Control-o",
    "open_folder": "Control-Shift-O",
    "save_playlist": "Control-s",
    "load_playlist": "Control-l",
}

MAX_MISSING_FILES_TO_DISPLAY = 5

STATUS_READY = "Ready"

ERROR_UNSUPPORTED_FILE = "Unsupported audio file format."

ERROR_FILE_NOT_FOUND = "The selected audio file no longer exists."

ERROR_EMPTY_PLAYLIST = "Playlist is empty. Please add songs first."

ERROR_PLAYBACK_FAILED = "Playback failed. The file may be corrupted or unsupported."

SUPPORTED_PLAYLIST_EXTENSIONS = [".json"]
