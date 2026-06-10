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

WINDOW_WIDTH = 1200
WINDOW_HEIGHT = 640
MIN_WINDOW_WIDTH = 1100
MIN_WINDOW_HEIGHT = 640

SUPPORTED_AUDIO_EXTENSIONS = [".mp3", ".wav", ".ogg"]

DEFAULT_VOLUME = 45

SETTINGS_FILE = "data/settings.json"

AVAILABLE_THEMES = ["light", "dark"]

DEFAULT_THEME = "dark"

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

MUSICBRAINZ_ENABLED = True
MUSICBRAINZ_APP_NAME = "PyTune Box"
MUSICBRAINZ_APP_VERSION = "0.1.0-beta"
MUSICBRAINZ_CONTACT = None
MUSICBRAINZ_MAX_RESULTS = 10
MUSICBRAINZ_RATE_LIMIT_SECONDS = 1.2
MUSICBRAINZ_DEFAULT_INCLUDES = [
    "artists",
    "releases",
    "release-groups"
]

ERROR_MUSICBRAINZ_NETWORK = "MusicBrainz lookup failed. Please check your internet connection."
ERROR_MUSICBRAINZ_NO_RESULTS = "No MusicBrainz matches found."
ERROR_MUSICBRAINZ_RATE_LIMIT = "MusicBrainz rate limit reached. Please wait and try again."

YOUTUBE_STREAMING_ENABLED = True

YOUTUBE_MAX_RESULTS = 5

YOUTUBE_DEFAULT_SEARCH_PREFIX = "ytsearch"

YOUTUBE_YTDLP_OPTIONS = {
    "format": "bestaudio/best",
    "default_search": "ytsearch",
    "noplaylist": True,
    "quiet": True,
    "no_warnings": True,
    "extract_flat": False
}

YOUTUBE_STREAM_STATUS_READY = "YouTube streaming ready"

YOUTUBE_STREAM_STATUS_SEARCHING = "Searching YouTube..."

YOUTUBE_STREAM_STATUS_BUFFERING = "Buffering YouTube audio..."

YOUTUBE_STREAM_STATUS_PLAYING = "Streaming from YouTube"

ERROR_YOUTUBE_EMPTY_QUERY = "Please enter a YouTube search term or URL."

ERROR_YOUTUBE_NO_RESULTS = "No YouTube results found."

ERROR_YOUTUBE_EXTRACTION_FAILED = "Could not extract YouTube audio stream."

ERROR_YOUTUBE_NETWORK = "YouTube streaming failed. Please check your internet connection."

ERROR_VLC_NOT_AVAILABLE = "VLC Media Player is required for YouTube streaming. Please install VLC 64-bit for your 64-bit Python."

YOUTUBE_STREAM_SOURCE = "YouTube"
