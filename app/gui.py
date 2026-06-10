"""
PyTune Box - Main GUI Window

Provides the primary Tkinter interface for the music player.
Phase 10: Testing, error handling, and polish.
"""

import json
import random
import tkinter as tk
from pathlib import Path
from tkinter import filedialog, messagebox, simpledialog, ttk

from app.config import (
    APP_NAME,
    APP_VERSION,
    AUDIO_FILE_TYPES,
    AVAILABLE_THEMES,
    DEFAULT_PLAYLIST_DIR,
    DEFAULT_REPEAT_MODE,
    DEFAULT_SHUFFLE,
    DEFAULT_THEME,
    DEFAULT_VOLUME,
    ERROR_EMPTY_PLAYLIST,
    ERROR_FILE_NOT_FOUND,
    ERROR_PLAYBACK_FAILED,
    MAX_MISSING_FILES_TO_DISPLAY,
    MIN_WINDOW_HEIGHT,
    MIN_WINDOW_WIDTH,
    PLAYLIST_FILE_TYPES,
    PLAYLIST_PLACEHOLDER_ITEMS,
    REPEAT_MODES,
    SETTINGS_FILE,
    SUPPORTED_AUDIO_EXTENSIONS,
    SUPPORTED_PLAYLIST_EXTENSIONS,
    WINDOW_HEIGHT,
    WINDOW_WIDTH,
)
from app.player import AudioPlayer
from app.playlist import PlaylistManager
from app.themes import get_next_theme_name, get_theme
from app.visualizer import AudioVisualizer

import threading
from app.musicbrainz_service import MusicBrainzService
from app.youtube_service import YouTubeService
from app.stream_player import StreamPlayer
from app.config import (
    MUSICBRAINZ_ENABLED,
    ERROR_MUSICBRAINZ_NO_RESULTS,
    ERROR_MUSICBRAINZ_NETWORK,
    YOUTUBE_STREAMING_ENABLED,
    YOUTUBE_STREAM_STATUS_READY,
    YOUTUBE_STREAM_STATUS_SEARCHING,
    YOUTUBE_STREAM_STATUS_BUFFERING,
    YOUTUBE_STREAM_STATUS_PLAYING,
    ERROR_YOUTUBE_EMPTY_QUERY,
    ERROR_YOUTUBE_NO_RESULTS,
    ERROR_YOUTUBE_EXTRACTION_FAILED,
    ERROR_YOUTUBE_NETWORK,
    ERROR_VLC_NOT_AVAILABLE,
    YOUTUBE_STREAM_SOURCE,
    DEFAULT_VOLUME,
)


class PyTuneBoxApp:
    """Main application window for PyTune Box."""

    def __init__(self):
        """Initialize the main window and layout."""
        self.root = tk.Tk()
        self.root.title(f"{APP_NAME} - Music Player")
        self.root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root.minsize(MIN_WINDOW_WIDTH, MIN_WINDOW_HEIGHT)

        # Load saved settings before creating audio player and UI
        self.settings = self.load_settings()
        self.current_theme_name = self.settings.get("theme", DEFAULT_THEME)
        self.current_theme = get_theme(self.current_theme_name)
        saved_volume = self.settings.get("volume", DEFAULT_VOLUME)
        self._last_saved_volume = saved_volume

        shuffle_setting = self.settings.get("shuffle", DEFAULT_SHUFFLE)
        self.shuffle_enabled = shuffle_setting if isinstance(shuffle_setting, bool) else DEFAULT_SHUFFLE

        repeat_setting = self.settings.get("repeat_mode", DEFAULT_REPEAT_MODE)
        self.repeat_mode = repeat_setting if repeat_setting in REPEAT_MODES else DEFAULT_REPEAT_MODE

        self.play_history = []

        self.ttk_style = ttk.Style(self.root)

        # Audio player and playlist state
        self.playlist_manager = PlaylistManager()
        self.current_index = None
        self.progress_update_job = None
        self.user_dragging_progress = False
        self.updating_progress_ui = False
        self.current_song_duration = 0
        self.handling_song_finish = False
        self._startup_status = "Phase 10: Testing and polish ready"

        if MUSICBRAINZ_ENABLED:
            self.musicbrainz_service = MusicBrainzService()
        else:
            self.musicbrainz_service = None
        self.musicbrainz_lookup_in_progress = False

        self.youtube_service = YouTubeService()
        self.stream_player = StreamPlayer(volume=saved_volume)
        self.youtube_streaming_active = False
        self.youtube_lookup_in_progress = False
        self.current_youtube_stream_info = None
        self.youtube_progress_job = None

        try:
            self.audio_player = AudioPlayer(volume=saved_volume / 100)
        except RuntimeError:
            self.audio_player = AudioPlayer.create_offline(volume=saved_volume / 100)
            self._startup_status = (
                "Audio output unavailable - connect speakers/headphones and restart"
            )

        # Allow the window to resize smoothly
        self.root.columnconfigure(0, weight=1)
        self.root.rowconfigure(0, weight=1)

        # UI references
        self.main_frame = None
        self.menubar = None
        self.status_label = None
        self.volume_value_label = None
        self.playlist_count_label = None
        self.theme_toggle_button = None
        self.shuffle_button = None
        self.repeat_button = None
        self.previous_button = None
        self.play_pause_button = None
        self.stop_button = None
        self.next_button = None
        self.remove_selected_button = None
        self.clear_playlist_button = None

        self._build_menu_bar()
        self._build_layout()
        self.apply_theme()
        self.update_playback_mode_buttons()
        self.bind_keyboard_shortcuts()

        # Handle window close button (X)
        self.root.protocol("WM_DELETE_WINDOW", self.on_exit)

    def _build_menu_bar(self):
        """Create the application menu bar."""
        self.menubar = tk.Menu(self.root)
        menubar = self.menubar
        self.root.config(menu=menubar)

        # File menu
        file_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="File", menu=file_menu)
        file_menu.add_command(label="Open Files", command=self.open_files)
        file_menu.add_command(label="Open Folder", command=self.open_folder)
        file_menu.add_separator()
        file_menu.add_command(label="Save Playlist", command=self.save_playlist)
        file_menu.add_command(label="Load Playlist", command=self.load_playlist)
        file_menu.add_separator()
        file_menu.add_command(label="Exit", command=self.on_exit)

        # Playback menu
        playback_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Playback", menu=playback_menu)
        playback_menu.add_command(label="Play / Pause    Space", command=self.on_play_pause)
        playback_menu.add_command(label="Stop    S", command=self.on_stop)
        playback_menu.add_separator()
        playback_menu.add_command(label="Next    Right", command=self.on_next)
        playback_menu.add_command(label="Previous    Left", command=self.on_previous)
        playback_menu.add_separator()
        playback_menu.add_command(label="Toggle Shuffle    H", command=self.on_shuffle)
        playback_menu.add_command(label="Cycle Repeat    R", command=self.on_repeat)

        # View menu
        view_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="View", menu=view_menu)
        view_menu.add_command(label="Toggle Theme", command=self.toggle_theme)

        # Help menu
        help_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Help", menu=help_menu)
        help_menu.add_command(label="About", command=self.show_about)

        # Tools menu
        tools_menu = tk.Menu(menubar, tearoff=0)
        menubar.add_cascade(label="Tools", menu=tools_menu)
        tools_menu.add_command(label="Lookup Metadata on MusicBrainz", command=self.lookup_musicbrainz_for_selected_song)
        tools_menu.add_command(label="Manual MusicBrainz Search", command=self.manual_musicbrainz_search)
        tools_menu.add_separator()
        tools_menu.add_command(label="YouTube Search & Stream", command=self.on_youtube_stream_clicked)
        tools_menu.add_command(label="Stop YouTube Stream", command=self.stop_youtube_stream)

    def _build_layout(self):
        """Build the full layout with all sections."""
        self.main_frame = ttk.Frame(self.root, padding=15)
        self.main_frame.grid(row=0, column=0, sticky="nsew")
        self.main_frame.columnconfigure(0, weight=1)
        self.main_frame.rowconfigure(2, weight=1)  # Playlist section expands

        self._build_header(self.main_frame)
        self._build_now_playing(self.main_frame)
        self._build_playlist(self.main_frame)
        self._build_controls(self.main_frame)
        self._build_youtube_stream(self.main_frame)
        self._build_visualizer(self.main_frame)
        self._build_status_bar(self.main_frame)

    def _build_header(self, parent):
        """Build the header section with title and version."""
        header_frame = ttk.Frame(parent)
        header_frame.grid(row=0, column=0, sticky="ew", pady=(0, 10))

        title_label = ttk.Label(
            header_frame,
            text=APP_NAME,
            font=("Segoe UI", 24, "bold"),
            anchor="center",
        )
        title_label.pack()

        subtitle_label = ttk.Label(
            header_frame,
            text="Desktop Music Player",
            font=("Segoe UI", 11),
            anchor="center",
        )
        subtitle_label.pack(pady=(2, 0))

        version_label = ttk.Label(
            header_frame,
            text=f"Version {APP_VERSION}",
            font=("Segoe UI", 9),
            anchor="center",
        )
        version_label.pack(pady=(2, 0))

        self.theme_toggle_button = ttk.Button(
            header_frame,
            text="Toggle Theme",
            command=self.toggle_theme,
        )
        self.theme_toggle_button.pack(pady=(8, 0))

    def _build_now_playing(self, parent):
        """Build the Now Playing section."""
        now_playing_frame = ttk.LabelFrame(parent, text="Now Playing", padding=10)
        now_playing_frame.grid(row=1, column=0, sticky="ew", pady=(0, 10))
        now_playing_frame.columnconfigure(0, weight=1)

        self.song_title_label = ttk.Label(
            now_playing_frame,
            text="No song selected",
            font=("Segoe UI", 14, "bold"),
        )
        self.song_title_label.grid(row=0, column=0, sticky="w")

        self.artist_label = ttk.Label(
            now_playing_frame,
            text="Artist: Unknown Artist",
            font=("Segoe UI", 10),
        )
        self.artist_label.grid(row=1, column=0, sticky="w", pady=(4, 0))

        self.album_label = ttk.Label(
            now_playing_frame,
            text="Album: Unknown Album",
            font=("Segoe UI", 10),
        )
        self.album_label.grid(row=2, column=0, sticky="w", pady=(4, 0))

        self.duration_label = ttk.Label(
            now_playing_frame,
            text="Duration: 00:00 / 00:00",
            font=("Segoe UI", 10),
        )
        self.duration_label.grid(row=3, column=0, sticky="w", pady=(4, 0))

        self.progress_scale = ttk.Scale(
            now_playing_frame,
            from_=0,
            to=100,
            orient="horizontal",
            value=0,
            command=self.on_progress_drag,
        )
        self.progress_scale.grid(row=4, column=0, sticky="ew", pady=(8, 0))
        self.progress_scale.bind("<ButtonPress-1>", self.on_progress_press)
        self.progress_scale.bind("<ButtonRelease-1>", self.on_progress_release)

    def _build_playlist(self, parent):
        """Build the Playlist section with search, listbox, and management buttons."""
        playlist_frame = ttk.LabelFrame(parent, text="Playlist", padding=10)
        playlist_frame.grid(row=2, column=0, sticky="nsew", pady=(0, 10))
        playlist_frame.columnconfigure(0, weight=1)
        playlist_frame.rowconfigure(2, weight=1)

        # Search and count row
        top_row = ttk.Frame(playlist_frame)
        top_row.grid(row=0, column=0, sticky="ew", pady=(0, 8))
        top_row.columnconfigure(1, weight=1)

        ttk.Label(top_row, text="Search:").grid(row=0, column=0, padx=(0, 8))
        self.search_entry = ttk.Entry(top_row)
        self.search_entry.grid(row=0, column=1, sticky="ew")

        self.playlist_count_label = ttk.Label(top_row, text="Songs: 0")
        self.playlist_count_label.grid(row=0, column=2, padx=(12, 0))

        # Management buttons row
        button_row = ttk.Frame(playlist_frame)
        button_row.grid(row=1, column=0, sticky="ew", pady=(0, 8))

        self.remove_selected_button = ttk.Button(
            button_row, text="Remove Selected", command=self.remove_selected_song
        )
        self.remove_selected_button.pack(side="left", padx=(0, 6))
        self.clear_playlist_button = ttk.Button(
            button_row, text="Clear Playlist", command=self.clear_playlist
        )
        self.clear_playlist_button.pack(side="left")

        self.musicbrainz_button = ttk.Button(
            button_row, text="Lookup MusicBrainz", command=self.lookup_musicbrainz_for_selected_song
        )
        self.musicbrainz_button.pack(side="right")

        # Listbox with scrollbar
        list_frame = ttk.Frame(playlist_frame)
        list_frame.grid(row=2, column=0, sticky="nsew")
        list_frame.columnconfigure(0, weight=1)
        list_frame.rowconfigure(0, weight=1)

        self.playlist_listbox = tk.Listbox(list_frame, height=8)
        self.playlist_listbox.grid(row=0, column=0, sticky="nsew")
        self.playlist_listbox.bind("<Double-Button-1>", self.on_playlist_double_click)

        scrollbar = ttk.Scrollbar(
            list_frame, orient="vertical", command=self.playlist_listbox.yview
        )
        scrollbar.grid(row=0, column=1, sticky="ns")
        self.playlist_listbox.config(yscrollcommand=scrollbar.set)

        self.show_playlist_placeholder()

    def _build_controls(self, parent):
        """Build the Controls and Volume sections."""
        controls_frame = ttk.LabelFrame(parent, text="Controls", padding=10)
        controls_frame.grid(row=3, column=0, sticky="ew", pady=(0, 10))

        # Playback buttons row
        buttons_frame = ttk.Frame(controls_frame)
        buttons_frame.pack(fill="x")

        self.previous_button = ttk.Button(
            buttons_frame, text="Previous", command=self.on_previous
        )
        self.previous_button.pack(side="left", padx=4)
        self.play_pause_button = ttk.Button(
            buttons_frame, text="Play / Pause", command=self.on_play_pause
        )
        self.play_pause_button.pack(side="left", padx=4)
        self.stop_button = ttk.Button(buttons_frame, text="Stop", command=self.on_stop)
        self.stop_button.pack(side="left", padx=4)
        self.next_button = ttk.Button(buttons_frame, text="Next", command=self.on_next)
        self.next_button.pack(side="left", padx=4)
        self.shuffle_button = ttk.Button(
            buttons_frame, text="Shuffle: Off", command=self.on_shuffle
        )
        self.shuffle_button.pack(side="left", padx=4)

        self.repeat_button = ttk.Button(
            buttons_frame, text="Repeat: Off", command=self.on_repeat
        )
        self.repeat_button.pack(side="left", padx=4)

        # Volume row
        volume_frame = ttk.Frame(controls_frame)
        volume_frame.pack(fill="x", pady=(12, 0))

        ttk.Label(volume_frame, text="Volume:").pack(side="left", padx=(0, 8))

        saved_volume = self.settings.get("volume", DEFAULT_VOLUME)

        self.volume_scale = ttk.Scale(
            volume_frame,
            from_=0,
            to=100,
            orient="horizontal",
            value=saved_volume,
            command=self.on_volume_change,
        )
        self.volume_scale.pack(side="left", fill="x", expand=True, padx=(0, 8))

        self.volume_value_label = ttk.Label(
            volume_frame,
            text=f"{saved_volume}%",
            width=5,
        )
        self.volume_value_label.pack(side="left")

    def _build_youtube_stream(self, parent):
        """Build the YouTube stream search/playback section."""
        yt_frame = ttk.LabelFrame(parent, text="YouTube Stream", padding=10)
        yt_frame.grid(row=4, column=0, sticky="ew", pady=(0, 10))
        yt_frame.columnconfigure(1, weight=1)

        ttk.Label(yt_frame, text="Search or URL:").grid(row=0, column=0, sticky="w", padx=(0, 8))
        self.youtube_query_entry = ttk.Entry(yt_frame)
        self.youtube_query_entry.grid(row=0, column=1, sticky="ew", padx=(0, 8))

        btn_frame = ttk.Frame(yt_frame)
        btn_frame.grid(row=0, column=2, sticky="e")

        self.youtube_stream_button = ttk.Button(
            btn_frame, text="Search & Stream", command=self.on_youtube_stream_clicked
        )
        self.youtube_stream_button.pack(side="left", padx=(0, 6))

        self.youtube_stop_button = ttk.Button(
            btn_frame, text="Stop Stream", command=self.stop_youtube_stream
        )
        self.youtube_stop_button.pack(side="left")

        # Status row
        status_row = ttk.Frame(yt_frame)
        status_row.grid(row=1, column=0, columnspan=3, sticky="ew", pady=(6, 0))
        status_row.columnconfigure(0, weight=1)

        self.youtube_status_label = ttk.Label(
            status_row, text=YOUTUBE_STREAM_STATUS_READY, font=("Segoe UI", 9, "italic")
        )
        self.youtube_status_label.grid(row=0, column=0, sticky="w")

        note_label = ttk.Label(
            status_row, text="Requires internet & VLC Player.", font=("Segoe UI", 8)
        )
        note_label.grid(row=0, column=1, sticky="e")

    def _build_visualizer(self, parent):
        """Build the visualizer section."""
        self.visualizer_frame = ttk.LabelFrame(parent, text="Visualizer", padding=10)
        self.visualizer_frame.grid(row=5, column=0, sticky="ew", pady=(0, 10))
        self.visualizer_frame.columnconfigure(0, weight=1)

        self.visualizer = AudioVisualizer(
            self.visualizer_frame,
            width=500,
            height=90,
            bar_count=32,
        )
        self.visualizer.get_widget().grid(row=0, column=0, sticky="ew")

    def _build_status_bar(self, parent):
        """Build the status bar at the bottom."""
        status_frame = ttk.Frame(parent)
        status_frame.grid(row=6, column=0, sticky="ew")

        separator = ttk.Separator(status_frame, orient="horizontal")
        separator.pack(fill="x", pady=(0, 6))

        self.status_label = ttk.Label(
            status_frame,
            text=self._startup_status,
            font=("Segoe UI", 9),
            anchor="w",
        )
        self.status_label.pack(side="left", fill="x", expand=True)

    # -------------------------------------------------------------------------
    # Playlist display helpers
    # -------------------------------------------------------------------------

    def show_playlist_placeholder(self):
        """Show placeholder text when the playlist is empty."""
        self.playlist_listbox.delete(0, tk.END)

        for item in PLAYLIST_PLACEHOLDER_ITEMS:
            self.playlist_listbox.insert(tk.END, item)

        self.update_playlist_count()

    def refresh_playlist_display(self):
        """Refresh the playlist listbox from playlist_manager."""
        self.playlist_listbox.delete(0, tk.END)

        if self.playlist_manager.is_empty():
            self.show_playlist_placeholder()
            return

        for display_name in self.playlist_manager.get_display_names():
            self.playlist_listbox.insert(tk.END, display_name)

        self.update_playlist_count()

        # Keep current selection if the index is still valid
        if self.current_index is not None and self.current_index < self.playlist_manager.count():
            self.playlist_listbox.selection_clear(0, tk.END)
            self.playlist_listbox.selection_set(self.current_index)
            self.playlist_listbox.see(self.current_index)

    def update_playlist_count(self):
        """Update the playlist song count label."""
        if self.playlist_count_label:
            self.playlist_count_label.config(
                text=f"Songs: {self.playlist_manager.count()}"
            )

    def format_duration(self, seconds):
        """Convert seconds into MM:SS display text."""
        try:
            total_seconds = int(seconds)
        except (TypeError, ValueError):
            return "00:00"

        if total_seconds < 0:
            total_seconds = 0

        minutes = total_seconds // 60
        secs = total_seconds % 60
        return f"{minutes:02d}:{secs:02d}"

    def set_progress_value(self, value):
        """Set the progress scale without triggering a seek."""
        self.updating_progress_ui = True
        self.progress_scale.set(value)
        self.updating_progress_ui = False

    def reset_now_playing(self):
        """Reset the Now Playing labels to their default state."""
        self.stop_progress_updates()
        self.current_song_duration = 0

        if hasattr(self, "song_title_label") and self.song_title_label:
            self.song_title_label.config(text="No song selected")
        if hasattr(self, "artist_label") and self.artist_label:
            self.artist_label.config(text="Artist: Unknown Artist")
        if hasattr(self, "album_label") and self.album_label:
            self.album_label.config(text="Album: Unknown Album")
        if hasattr(self, "duration_label") and self.duration_label:
            self.duration_label.config(text="Duration: 00:00 / 00:00")

        self.set_progress_value(0)

        if hasattr(self, "visualizer"):
            self.visualizer.stop()

    def _stop_and_reset_playback(self):
        """Stop audio and reset the current playback state."""
        self.stop_progress_updates()
        try:
            self.audio_player.stop()
        except RuntimeError:
            pass
        self.current_index = None
        self.reset_now_playing()

    def start_progress_updates(self):
        """Start periodic progress bar updates."""
        self.stop_progress_updates()
        self.update_progress()

    def stop_progress_updates(self):
        """Stop periodic progress bar updates."""
        if self.progress_update_job is not None:
            self.root.after_cancel(self.progress_update_job)
            self.progress_update_job = None

    def update_progress(self):
        """Update elapsed time, progress scale, and detect song end."""
        self.progress_update_job = None

        if self.current_index is None or self.current_song_duration <= 0:
            self.set_progress_value(0)
            return

        elapsed = self.audio_player.get_elapsed_seconds()
        elapsed = max(0, min(elapsed, self.current_song_duration))
        total_text = self.format_duration(self.current_song_duration)
        elapsed_text = self.format_duration(elapsed)

        if self.audio_player.is_playing or self.audio_player.is_paused:
            percentage = (elapsed / self.current_song_duration) * 100

            if not self.user_dragging_progress:
                self.set_progress_value(percentage)

            self.duration_label.config(text=f"Duration: {elapsed_text} / {total_text}")

            if self.audio_player.is_playing and not self.audio_player.is_paused:
                if (
                    elapsed >= 1
                    and not self.audio_player.is_busy()
                    and (
                        self.current_song_duration == 0
                        or elapsed >= self.current_song_duration - 1
                    )
                ):
                    self.handle_song_finished()
                    return

                self.progress_update_job = self.root.after(1000, self.update_progress)
            else:
                self.progress_update_job = self.root.after(1000, self.update_progress)

    def handle_song_finished(self):
        """Handle automatic transition when the current song ends."""
        if self.handling_song_finish:
            return

        self.handling_song_finish = True

        try:
            self.stop_progress_updates()

            if self.playlist_manager.is_empty():
                try:
                    self.audio_player.stop()
                except RuntimeError:
                    pass
                self.set_progress_value(0)
                if hasattr(self, "visualizer"):
                    self.visualizer.stop()
                self.update_status("Playback finished")
                return

            if self.repeat_mode == "one" and self.current_index is not None:
                self.play_song_at_index(self.current_index)
                return

            next_index = self.get_next_index()

            if next_index is None:
                try:
                    self.audio_player.stop()
                except RuntimeError:
                    pass
                total_text = self.format_duration(self.current_song_duration)
                self.set_progress_value(0)
                self.duration_label.config(text=f"Duration: 00:00 / {total_text}")
                if hasattr(self, "visualizer"):
                    self.visualizer.stop()
                self.update_status("Playlist finished")
                return

            self.play_song_at_index(next_index)
        finally:
            self.handling_song_finish = False

    def on_progress_press(self, event):
        """Mark that the user is dragging the progress control."""
        if self.current_song_duration > 0 and self.current_index is not None:
            self.user_dragging_progress = True

    def on_progress_release(self, event):
        """Seek to the position selected on the progress control."""
        if not self.user_dragging_progress:
            return

        self.user_dragging_progress = False
        self.seek_to_progress_position()

    def on_progress_drag(self, value):
        """Update display while the user drags the progress control."""
        if self.updating_progress_ui or not self.user_dragging_progress:
            return

        if self.current_song_duration <= 0:
            return

        percentage = float(value)
        target_seconds = int((percentage / 100) * self.current_song_duration)
        elapsed_text = self.format_duration(target_seconds)
        total_text = self.format_duration(self.current_song_duration)
        self.duration_label.config(text=f"Duration: {elapsed_text} / {total_text}")

    def seek_to_progress_position(self):
        """Seek playback to the current progress scale position."""
        if self.current_index is None or self.current_song_duration <= 0:
            return

        percentage = float(self.progress_scale.get())
        target_seconds = int((percentage / 100) * self.current_song_duration)

        if self.audio_player.seek(target_seconds):
            seek_text = self.format_duration(target_seconds)
            self.update_status(f"Seeked to {seek_text}")
            self.start_progress_updates()
        else:
            messagebox.showwarning(
                "Seek Unsupported",
                "Seeking is not supported for this file.",
            )
            elapsed = self.audio_player.get_elapsed_seconds()
            if self.current_song_duration > 0:
                reset_percentage = (elapsed / self.current_song_duration) * 100
                self.set_progress_value(reset_percentage)
            self.start_progress_updates()

    # -------------------------------------------------------------------------
    # Theme and settings helpers
    # -------------------------------------------------------------------------

    def safe_configure(self, widget, **kwargs):
        """Safely configure a widget without crashing on unsupported options."""
        try:
            widget.configure(**kwargs)
        except tk.TclError:
            pass
        except Exception:
            pass

    def load_settings(self):
        """Load application settings from data/settings.json."""
        defaults = {
            "theme": DEFAULT_THEME,
            "volume": DEFAULT_VOLUME,
            "last_playlist": None,
            "shuffle": DEFAULT_SHUFFLE,
            "repeat_mode": DEFAULT_REPEAT_MODE,
        }

        try:
            settings_path = Path(SETTINGS_FILE)
            if settings_path.exists():
                with open(settings_path, "r", encoding="utf-8") as file:
                    loaded = json.load(file)

                if isinstance(loaded, dict):
                    settings = defaults.copy()
                    settings.update(loaded)

                    if settings.get("theme") not in AVAILABLE_THEMES:
                        settings["theme"] = DEFAULT_THEME

                    try:
                        volume = int(settings.get("volume", DEFAULT_VOLUME))
                        settings["volume"] = max(0, min(100, volume))
                    except (TypeError, ValueError):
                        settings["volume"] = DEFAULT_VOLUME

                    if not isinstance(settings.get("shuffle"), bool):
                        settings["shuffle"] = DEFAULT_SHUFFLE

                    if settings.get("repeat_mode") not in REPEAT_MODES:
                        settings["repeat_mode"] = DEFAULT_REPEAT_MODE

                    return settings
        except Exception:
            pass

        return defaults.copy()

    def save_settings(self):
        """Save current settings to data/settings.json."""
        try:
            settings_path = Path(SETTINGS_FILE)
            settings_path.parent.mkdir(parents=True, exist_ok=True)

            with open(settings_path, "w", encoding="utf-8") as file:
                json.dump(self.settings, file, indent=4, ensure_ascii=False)
        except Exception:
            if self.status_label:
                self.update_status("Failed to save settings")

    def update_setting(self, key, value):
        """Update one setting value and save to disk."""
        self.settings[key] = value
        self.save_settings()

    def toggle_theme(self):
        """Switch between light and dark themes."""
        self.current_theme_name = get_next_theme_name(self.current_theme_name)
        self.current_theme = get_theme(self.current_theme_name)
        self.apply_theme()
        self.update_setting("theme", self.current_theme_name)

        if self.current_theme_name == "dark":
            self.update_status("Theme changed to Dark Mode")
        else:
            self.update_status("Theme changed to Light Mode")

    def apply_theme(self):
        """Apply the current theme to the GUI."""
        theme = self.current_theme

        self.safe_configure(self.root, bg=theme["bg"])

        try:
            self.ttk_style.theme_use("clam")
        except tk.TclError:
            pass

        self.ttk_style.configure("TFrame", background=theme["frame_bg"])
        self.ttk_style.configure(
            "TLabel",
            background=theme["label_bg"],
            foreground=theme["label_fg"],
        )
        self.ttk_style.configure(
            "TButton",
            background=theme["button_bg"],
            foreground=theme["button_fg"],
        )
        self.ttk_style.configure(
            "TLabelframe",
            background=theme["frame_bg"],
            foreground=theme["fg"],
        )
        self.ttk_style.configure(
            "TLabelframe.Label",
            background=theme["frame_bg"],
            foreground=theme["fg"],
        )
        self.ttk_style.configure("Horizontal.TScale", background=theme["frame_bg"])
        self.ttk_style.configure(
            "Horizontal.TProgressbar",
            background=theme["button_bg"],
            troughcolor=theme["entry_bg"],
        )
        self.ttk_style.configure(
            "Status.TLabel",
            background=theme["status_bg"],
            foreground=theme["status_fg"],
        )

        self.safe_configure(
            self.playlist_listbox,
            bg=theme["listbox_bg"],
            fg=theme["listbox_fg"],
            selectbackground=theme["select_bg"],
            selectforeground=theme["select_fg"],
            highlightbackground=theme["frame_bg"],
            highlightcolor=theme["select_bg"],
        )

        if self.status_label:
            self.status_label.configure(style="Status.TLabel")

        if self.menubar:
            self.safe_configure(
                self.menubar,
                bg=theme["bg"],
                fg=theme["fg"],
                activebackground=theme["button_bg"],
                activeforeground=theme["button_fg"],
            )

        if hasattr(self, "visualizer"):
            self.visualizer.apply_theme(theme)

    def get_default_playlist_dir(self):
        """Return the default playlist folder, creating it if needed."""
        playlist_dir = Path(DEFAULT_PLAYLIST_DIR)

        if not playlist_dir.is_absolute():
            playlist_dir = Path.cwd() / playlist_dir

        try:
            playlist_dir.mkdir(parents=True, exist_ok=True)
            return playlist_dir
        except OSError:
            return Path.cwd()

    def update_last_playlist(self, file_path):
        """Store the last saved or loaded playlist path in settings."""
        self.update_setting("last_playlist", str(Path(file_path).resolve()))

    # -------------------------------------------------------------------------
    # File and playlist methods
    # -------------------------------------------------------------------------

    def save_playlist(self):
        """Save the current playlist to a JSON file."""
        if self.playlist_manager.is_empty():
            confirmed = messagebox.askyesno(
                title="Save Empty Playlist",
                message="The playlist is empty. Do you still want to save it?",
            )
            if not confirmed:
                return

        playlist_name = simpledialog.askstring(
            title="Playlist Name",
            prompt="Enter playlist name:",
        )

        if not playlist_name or not playlist_name.strip():
            playlist_name = "Untitled Playlist"
        else:
            playlist_name = playlist_name.strip()

        initial_file = playlist_name.replace(" ", "_") + ".json"
        default_dir = self.get_default_playlist_dir()

        file_path = filedialog.asksaveasfilename(
            title="Save Playlist",
            initialdir=str(default_dir),
            defaultextension=".json",
            filetypes=PLAYLIST_FILE_TYPES,
            initialfile=initial_file,
        )

        if not file_path:
            return

        save_path = Path(file_path)
        if save_path.suffix.lower() not in SUPPORTED_PLAYLIST_EXTENSIONS:
            save_path = save_path.with_suffix(".json")

        try:
            self.playlist_manager.save_to_json(str(save_path), playlist_name)
            try:
                self.update_last_playlist(str(save_path))
            except Exception:
                pass
            filename = save_path.name
            self.update_status(f"Playlist saved: {filename}")
            messagebox.showinfo("Playlist Saved", "Playlist saved successfully.")
        except RuntimeError as exc:
            self.show_error("Save Failed", str(exc), "Failed to save playlist")

    def load_playlist(self):
        """Load a playlist from a JSON file."""
        default_dir = self.get_default_playlist_dir()

        file_path = filedialog.askopenfilename(
            title="Load Playlist",
            initialdir=str(default_dir),
            filetypes=PLAYLIST_FILE_TYPES,
        )

        if not file_path:
            return

        playlist_path = Path(file_path)

        if not playlist_path.exists() or not playlist_path.is_file():
            self.show_error(
                "Load Failed",
                "Playlist file not found.",
                "Playlist file not found",
            )
            return

        if playlist_path.suffix.lower() not in SUPPORTED_PLAYLIST_EXTENSIONS:
            self.show_error(
                "Load Failed",
                "Invalid playlist file format.",
                "Invalid playlist file",
            )
            return

        if not self.playlist_manager.is_empty():
            confirmed = messagebox.askyesno(
                title="Replace Current Playlist",
                message="Loading a playlist will replace the current playlist. Continue?",
            )
            if not confirmed:
                return

        try:
            self.stop_progress_updates()
            try:
                self.audio_player.stop()
            except RuntimeError:
                pass

            self.current_index = None
            self.play_history = []
            self.reset_now_playing()

            result = self.playlist_manager.load_from_json(str(playlist_path))
            self.refresh_playlist_display()

            try:
                self.update_last_playlist(str(playlist_path))
            except Exception:
                pass

            loaded = result["loaded"]
            skipped = result["skipped"]
            missing_files = result["missing_files"]
            missing_count = len(missing_files)

            self.update_status(f"Loaded {loaded} song(s), skipped {skipped}")

            summary_lines = [
                "Playlist loaded successfully.",
                f"Loaded: {loaded}",
                f"Skipped: {skipped}",
                f"Missing files: {missing_count}",
            ]

            if missing_files:
                summary_lines.append(
                    "Some files were skipped because they no longer exist."
                )
                preview = missing_files[:MAX_MISSING_FILES_TO_DISPLAY]
                for missing_path in preview:
                    summary_lines.append(f"- {Path(missing_path).name}")

                remaining = missing_count - len(preview)
                if remaining > 0:
                    summary_lines.append(f"... and {remaining} more")

            messagebox.showinfo("Playlist Loaded", "\n".join(summary_lines))

        except FileNotFoundError:
            self.show_error(
                "Load Failed",
                "Playlist file not found.",
                "Playlist file not found",
            )

        except ValueError:
            self.show_error(
                "Load Failed",
                "Invalid playlist file format.",
                "Invalid playlist file",
            )

        except Exception as exc:
            self.show_error(
                "Load Failed",
                f"Failed to load playlist.\n\n{exc}",
                "Failed to load playlist",
            )

    def open_files(self):
        """Open one or more audio files and add them to the playlist."""
        file_paths = filedialog.askopenfilenames(
            title="Open Audio Files",
            filetypes=AUDIO_FILE_TYPES,
        )

        if not file_paths:
            self.update_status("Open files cancelled")
            return

        added_count = 0
        skipped_count = 0

        for file_path in file_paths:
            if self.playlist_manager.add_song(file_path):
                added_count += 1
            else:
                skipped_count += 1

        self.refresh_playlist_display()
        self.update_status(f"Added {added_count} song(s). Skipped {skipped_count}.")

        if added_count == 0:
            self.show_warning(
                "No Songs Added",
                "No new supported audio files were added.",
                f"Added 0 song(s). Skipped {skipped_count}.",
            )

    def open_folder(self):
        """Open a folder and import supported audio files."""
        folder_path = filedialog.askdirectory(title="Open Folder")

        if not folder_path:
            self.update_status("Open folder cancelled")
            return

        include_subfolders = messagebox.askyesno(
            title="Include Subfolders?",
            message="Do you want to include audio files from subfolders?",
        )

        folder = Path(folder_path).resolve()
        matched_files = []

        if not folder.is_dir():
            self.show_warning(
                "Invalid Folder",
                "The selected folder could not be opened.",
                "Invalid folder selected",
            )
            return

        try:
            iterator = folder.rglob("*") if include_subfolders else folder.glob("*")
            for item in iterator:
                if (
                    item.is_file()
                    and item.suffix.lower() in SUPPORTED_AUDIO_EXTENSIONS
                ):
                    matched_files.append(item)
        except OSError:
            self.show_warning(
                "Folder Error",
                "Could not read the selected folder.",
                "Could not read selected folder",
            )
            return

        matched_files.sort(key=lambda item: item.name.lower())

        added_count = 0
        for item in matched_files:
            if self.playlist_manager.add_song(item):
                added_count += 1

        skipped_count = len(matched_files) - added_count
        self.refresh_playlist_display()

        if added_count > 0:
            self.update_status(
                f"Added {added_count} song(s) from folder. Skipped {skipped_count}."
            )
        else:
            self.show_warning(
                "No Songs Found",
                "No supported audio files found in selected folder.",
                "No supported audio files found in selected folder",
            )

    def remove_selected_song(self):
        """Remove the selected song from the playlist."""
        if self.playlist_manager.is_empty():
            messagebox.showwarning("Playlist Empty", "Playlist is empty.")
            return

        selection = self.playlist_listbox.curselection()
        if not selection:
            messagebox.showwarning("No Selection", "Please select a song to remove.")
            return

        index = selection[0]
        if index >= self.playlist_manager.count():
            return

        removed_song = self.playlist_manager.remove_song(index)
        filename = removed_song["filename"]

        if self.current_index == index:
            self._stop_and_reset_playback()
        elif self.current_index is not None and index < self.current_index:
            self.current_index -= 1

        self.rebuild_history_after_remove(index)

        if self.playlist_manager.is_empty():
            self.current_index = None
            self.play_history = []

        self.refresh_playlist_display()
        self.update_status(f"Removed: {filename}")

    def clear_playlist(self):
        """Clear the entire playlist after user confirmation."""
        if self.playlist_manager.is_empty():
            self.update_status("Playlist is already empty")
            return

        confirmed = messagebox.askyesno(
            title="Clear Playlist",
            message="Are you sure you want to clear the playlist?",
        )

        if not confirmed:
            return

        self._stop_and_reset_playback()
        self.playlist_manager.clear_playlist()
        self.play_history = []
        if hasattr(self, "visualizer"):
            self.visualizer.stop()
        self.refresh_playlist_display()
        self.update_status("Playlist cleared")

    def on_playlist_double_click(self, event):
        """Play the song that was double-clicked in the playlist."""
        if self.playlist_manager.is_empty():
            return

        selection = self.playlist_listbox.curselection()
        if not selection:
            return

        index = selection[0]
        if index >= self.playlist_manager.count():
            return

        self.play_song_at_index(index)

    def play_song_at_index(self, index):
        """Load and play the song at the given playlist index."""
        if self.playlist_manager.is_empty():
            self.show_warning("Playlist Empty", ERROR_EMPTY_PLAYLIST)
            return

        if index < 0 or index >= self.playlist_manager.count():
            self.update_status("Invalid playlist selection")
            return

        try:
            song = self.playlist_manager.get_song(index)
        except IndexError:
            self.update_status("Invalid playlist selection")
            return

        file_path = song["path"]
        song_path = Path(file_path)

        if not song_path.exists() or not song_path.is_file():
            self.show_error(
                "File Missing",
                ERROR_FILE_NOT_FOUND,
                f"File missing: {song['filename']}",
            )

            if self.current_index == index:
                self._stop_and_reset_playback()
            elif self.current_index is not None and index < self.current_index:
                self.current_index -= 1

            try:
                self.playlist_manager.remove_song(index)
            except IndexError:
                pass

            self.refresh_playlist_display()
            return

        try:
            if self.youtube_streaming_active:
                self.stop_youtube_stream()

            self.stop_progress_updates()
            self.set_progress_value(0)

            self.audio_player.load(file_path)
            self.audio_player.play()

            self.current_index = index
            self.current_song_duration = song.get("duration_seconds", 0)

            if hasattr(self, "song_title_label") and self.song_title_label:
                self.song_title_label.config(text=song["title"])
            if hasattr(self, "artist_label") and self.artist_label:
                self.artist_label.config(text=f"Artist: {song['artist']}")
            if hasattr(self, "album_label") and self.album_label:
                self.album_label.config(text=f"Album: {song['album']}")
            if hasattr(self, "duration_label") and self.duration_label:
                self.duration_label.config(
                    text=f"Duration: 00:00 / {song['duration_text']}"
                )

            self.playlist_listbox.selection_clear(0, tk.END)
            self.playlist_listbox.selection_set(index)
            self.playlist_listbox.see(index)

            self.update_status(f"Playing: {song['filename']}")
            self.start_progress_updates()
            if hasattr(self, "visualizer"):
                self.visualizer.start()

        except FileNotFoundError:
            self.show_error(
                "File Not Found",
                ERROR_FILE_NOT_FOUND,
                f"Error: File not found - {song['filename']}",
            )

        except RuntimeError as exc:
            message = ERROR_PLAYBACK_FAILED
            if str(exc) == "Audio system is not initialized.":
                message = str(exc)
            self.show_error("Playback Error", message, f"Error: Cannot play - {song['filename']}")

        except Exception as exc:
            self.show_error(
                "Playback Error",
                ERROR_PLAYBACK_FAILED,
                f"Error: Cannot play - {song['filename']} ({exc})",
            )

    # -------------------------------------------------------------------------
    # Playback control methods
    # -------------------------------------------------------------------------

    def update_status(self, message):
        """Update the status bar text."""
        if self.status_label:
            self.status_label.config(text=message)

    def show_error(self, title, message, status_message=None):
        """Show an error dialog and update the status bar."""
        messagebox.showerror(title, message)
        self.update_status(status_message if status_message is not None else message)

    def show_warning(self, title, message, status_message=None):
        """Show a warning dialog and update the status bar."""
        messagebox.showwarning(title, message)
        self.update_status(status_message if status_message is not None else message)

    def set_controls_state(self, enabled=True):
        """Enable or disable playback-related controls."""
        state = "normal" if enabled else "disabled"
        control_buttons = [
            getattr(self, "play_pause_button", None),
            getattr(self, "stop_button", None),
            getattr(self, "next_button", None),
            getattr(self, "previous_button", None),
            getattr(self, "shuffle_button", None),
            getattr(self, "repeat_button", None),
            getattr(self, "remove_selected_button", None),
            getattr(self, "clear_playlist_button", None),
        ]

        for button in control_buttons:
            if button is not None:
                self.safe_configure(button, state=state)

    def show_future_feature_message(self, feature_name):
        """Show a status message for features not yet implemented."""
        self.update_status(f"{feature_name} - feature coming in a future phase")

    def on_play_pause(self):
        """Play, pause, or resume the current song."""
        if self.youtube_streaming_active:
            if not self.stream_player.is_available:
                return
            try:
                self.stream_player.pause()
                if self.stream_player.is_paused:
                    self.update_status("YouTube stream paused")
                    if hasattr(self, "visualizer"):
                        self.visualizer.pause()
                else:
                    self.update_status("YouTube stream resumed")
                    if hasattr(self, "visualizer"):
                        self.visualizer.start()
            except Exception as e:
                self.show_error("YouTube Playback Error", str(e))
            return

        if self.playlist_manager.is_empty():
            self.show_warning(
                "No Songs",
                ERROR_EMPTY_PLAYLIST,
                "No song available",
            )
            return

        try:
            if self.audio_player.is_paused:
                self.audio_player.resume()
                self.update_status("Playback resumed")
                self.start_progress_updates()
                if hasattr(self, "visualizer"):
                    self.visualizer.start()

            elif self.audio_player.is_playing:
                self.audio_player.pause()
                self.update_status("Playback paused")
                if hasattr(self, "visualizer"):
                    self.visualizer.pause()

            else:
                if (
                    self.current_index is not None
                    and self.current_index < self.playlist_manager.count()
                ):
                    self.play_song_at_index(self.current_index)
                else:
                    selection = self.playlist_listbox.curselection()
                    if selection and selection[0] < self.playlist_manager.count():
                        self.play_song_at_index(selection[0])
                    else:
                        self.play_song_at_index(0)

        except RuntimeError as exc:
            self.show_error("Playback Error", str(exc))

        except Exception:
            self.show_error("Playback Error", ERROR_PLAYBACK_FAILED)

    def on_stop(self):
        """Stop playback."""
        if self.youtube_streaming_active:
            self.stop_youtube_stream()
            return

        self.stop_progress_updates()

        try:
            self.audio_player.stop()
        except RuntimeError:
            pass

        self.set_progress_value(0)

        if hasattr(self, "duration_label") and self.duration_label:
            if self.current_song_duration > 0:
                total_text = self.format_duration(self.current_song_duration)
                self.duration_label.config(text=f"Duration: 00:00 / {total_text}")
            else:
                self.duration_label.config(text="Duration: 00:00 / 00:00")

        self.update_status("Playback stopped")
        if hasattr(self, "visualizer"):
            self.visualizer.stop()

    def update_playback_mode_buttons(self):
        """Update Shuffle and Repeat button labels."""
        if self.shuffle_button:
            state = "On" if self.shuffle_enabled else "Off"
            self.shuffle_button.config(text=f"Shuffle: {state}")

        if self.repeat_button:
            repeat_labels = {"off": "Off", "one": "One", "all": "All"}
            label = repeat_labels.get(self.repeat_mode, "Off")
            self.repeat_button.config(text=f"Repeat: {label}")

    def get_next_index(self):
        """Return the next playlist index based on shuffle and repeat mode."""
        count = self.playlist_manager.count()

        if count == 0:
            return None

        if self.current_index is None:
            return 0

        if self.repeat_mode == "one":
            return self.current_index

        if self.shuffle_enabled:
            if count == 1:
                return self.current_index

            self.play_history.append(self.current_index)
            choices = [index for index in range(count) if index != self.current_index]
            return random.choice(choices)

        if self.current_index < count - 1:
            return self.current_index + 1

        if self.repeat_mode == "all":
            return 0

        return None

    def get_previous_index(self):
        """Return the previous playlist index based on shuffle and repeat mode."""
        count = self.playlist_manager.count()

        if count == 0:
            return None

        if self.current_index is None:
            return 0

        if self.shuffle_enabled and self.play_history:
            return self.play_history.pop()

        if self.current_index > 0:
            return self.current_index - 1

        if self.current_index == 0:
            if self.repeat_mode == "all":
                return count - 1
            return 0

        return 0

    def rebuild_history_after_remove(self, removed_index):
        """Adjust shuffle history after a song is removed."""
        updated_history = []

        for index in self.play_history:
            if index == removed_index:
                continue
            if index > removed_index:
                updated_history.append(index - 1)
            else:
                updated_history.append(index)

        self.play_history = updated_history

    def on_next(self):
        """Play the next song based on shuffle and repeat settings."""
        if self.playlist_manager.is_empty():
            self.show_warning(
                "No Songs",
                ERROR_EMPTY_PLAYLIST,
                "No song available",
            )
            return

        try:
            self.stop_progress_updates()
            self.set_progress_value(0)

            next_index = self.get_next_index()

            if next_index is None:
                try:
                    self.audio_player.stop()
                except RuntimeError:
                    pass

                if hasattr(self, "duration_label") and self.duration_label:
                    if self.current_song_duration > 0:
                        total_text = self.format_duration(self.current_song_duration)
                        self.duration_label.config(text=f"Duration: 00:00 / {total_text}")

                if hasattr(self, "visualizer"):
                    self.visualizer.stop()

                self.update_status("End of playlist")
                return

            self.play_song_at_index(next_index)

        except RuntimeError as exc:
            self.show_error("Playback Error", str(exc))

        except Exception:
            self.show_error("Playback Error", ERROR_PLAYBACK_FAILED)

    def on_previous(self):
        """Play the previous song based on shuffle and repeat settings."""
        if self.playlist_manager.is_empty():
            self.show_warning(
                "No Songs",
                ERROR_EMPTY_PLAYLIST,
                "No song available",
            )
            return

        try:
            self.stop_progress_updates()
            self.set_progress_value(0)

            previous_index = self.get_previous_index()

            if previous_index is None:
                return

            self.play_song_at_index(previous_index)

        except RuntimeError as exc:
            self.show_error("Playback Error", str(exc))

        except Exception:
            self.show_error("Playback Error", ERROR_PLAYBACK_FAILED)

    def on_shuffle(self):
        """Toggle shuffle mode on or off."""
        self.shuffle_enabled = not self.shuffle_enabled

        if not self.shuffle_enabled:
            self.play_history = []

        self.update_setting("shuffle", self.shuffle_enabled)
        self.update_playback_mode_buttons()

        if self.shuffle_enabled:
            self.update_status("Shuffle enabled")
        else:
            self.update_status("Shuffle disabled")

    def on_repeat(self):
        """Cycle repeat mode: off -> one -> all -> off."""
        mode_cycle = {"off": "one", "one": "all", "all": "off"}
        self.repeat_mode = mode_cycle.get(self.repeat_mode, "off")

        self.update_setting("repeat_mode", self.repeat_mode)
        self.update_playback_mode_buttons()

        repeat_labels = {"off": "Off", "one": "One", "all": "All"}
        self.update_status(f"Repeat mode: {repeat_labels[self.repeat_mode]}")

    def is_text_input_focused(self, event):
        """Return True if keyboard focus is in a text entry field."""
        widget = event.widget
        widget_class = widget.winfo_class()
        return isinstance(widget, (tk.Entry, ttk.Entry)) or widget_class in (
            "Entry",
            "TEntry",
        )

    def bind_keyboard_shortcuts(self):
        """Bind global keyboard shortcuts for common actions."""
        self.root.bind_all("<space>", self._shortcut_play_pause)
        self.root.bind_all("s", self._shortcut_stop)
        self.root.bind_all("S", self._shortcut_stop)
        self.root.bind_all("<Right>", self._shortcut_next)
        self.root.bind_all("<Left>", self._shortcut_previous)
        self.root.bind_all("h", self._shortcut_shuffle)
        self.root.bind_all("H", self._shortcut_shuffle)
        self.root.bind_all("r", self._shortcut_repeat)
        self.root.bind_all("R", self._shortcut_repeat)
        self.root.bind_all("<Control-o>", self._shortcut_open_files)
        self.root.bind_all("<Control-O>", self._shortcut_open_files)
        self.root.bind_all("<Control-Shift-O>", self._shortcut_open_folder)
        self.root.bind_all("<Control-Shift-o>", self._shortcut_open_folder)
        self.root.bind_all("<Control-s>", self._shortcut_save_playlist)
        self.root.bind_all("<Control-S>", self._shortcut_save_playlist)
        self.root.bind_all("<Control-l>", self._shortcut_load_playlist)
        self.root.bind_all("<Control-L>", self._shortcut_load_playlist)
        self.root.bind_all("<Control-y>", self._shortcut_focus_youtube)
        self.root.bind_all("<Control-Y>", self._shortcut_focus_youtube)

    def _shortcut_play_pause(self, event):
        """Keyboard shortcut for play/pause."""
        if self.is_text_input_focused(event):
            return
        self.on_play_pause()
        return "break"

    def _shortcut_stop(self, event):
        """Keyboard shortcut for stop."""
        if self.is_text_input_focused(event):
            return
        self.on_stop()
        return "break"

    def _shortcut_next(self, event):
        """Keyboard shortcut for next track."""
        self.on_next()
        return "break"

    def _shortcut_previous(self, event):
        """Keyboard shortcut for previous track."""
        self.on_previous()
        return "break"

    def _shortcut_shuffle(self, event):
        """Keyboard shortcut for shuffle toggle."""
        if self.is_text_input_focused(event):
            return
        self.on_shuffle()
        return "break"

    def _shortcut_repeat(self, event):
        """Keyboard shortcut for repeat cycle."""
        if self.is_text_input_focused(event):
            return
        self.on_repeat()
        return "break"

    def _shortcut_open_files(self, event):
        """Keyboard shortcut for open files."""
        self.open_files()
        return "break"

    def _shortcut_open_folder(self, event):
        """Keyboard shortcut for open folder."""
        self.open_folder()
        return "break"

    def _shortcut_save_playlist(self, event):
        """Keyboard shortcut for save playlist."""
        self.save_playlist()
        return "break"

    def _shortcut_load_playlist(self, event):
        """Keyboard shortcut for load playlist."""
        self.load_playlist()
        return "break"

    def _shortcut_focus_youtube(self, event):
        """Focus the YouTube query entry."""
        if hasattr(self, "youtube_query_entry") and self.youtube_query_entry:
            self.youtube_query_entry.focus_set()
        return "break"

    def on_volume_change(self, value):
        """Update volume label, apply volume, and save setting."""
        volume = int(float(value))

        if self.volume_value_label:
            self.volume_value_label.config(text=f"{volume}%")

        try:
            self.audio_player.set_volume(volume)
        except RuntimeError:
            self.audio_player.volume = max(0.0, min(1.0, volume / 100.0))

        if hasattr(self, "stream_player") and self.stream_player and self.stream_player.is_available:
            try:
                self.stream_player.set_volume(volume)
            except Exception:
                pass

        if self._last_saved_volume != volume:
            self._last_saved_volume = volume
            try:
                self.update_setting("volume", volume)
            except Exception:
                pass

    def on_exit(self):
        """Stop audio, save settings, and safely close the application."""
        try:
            self.stop_progress_updates()
            self.stop_youtube_progress_updates()
            if hasattr(self, "visualizer"):
                self.visualizer.stop()

            self.settings["theme"] = self.current_theme_name
            self.settings["volume"] = self.audio_player.get_volume()
            self.settings["shuffle"] = self.shuffle_enabled
            self.settings["repeat_mode"] = self.repeat_mode

            try:
                self.save_settings()
            except Exception:
                pass

            if hasattr(self, "stream_player") and self.stream_player:
                try:
                    self.stream_player.quit()
                except Exception:
                    pass

            self.audio_player.quit()
        except Exception:
            pass
        finally:
            try:
                self.root.destroy()
            except Exception:
                pass

    def show_about(self):
        """Show the About dialog."""
        messagebox.showinfo(
            title="About PyTune Box",
            message=(
                f"{APP_NAME}\n"
                f"Version {APP_VERSION}\n\n"
                "A Python Tkinter desktop music player project.\n\n"
                "Keyboard shortcuts:\n"
                "- Space: Play/Pause\n"
                "- S: Stop\n"
                "- Right Arrow: Next\n"
                "- Left Arrow: Previous\n"
                "- H: Shuffle\n"
                "- R: Repeat\n"
                "- Ctrl+O: Open Files\n"
                "- Ctrl+Shift+O: Open Folder\n"
                "- Ctrl+S: Save Playlist\n"
                "- Ctrl+L: Load Playlist"
            ),
        )

    def run(self):
        """Start the Tkinter main event loop."""
        self.root.mainloop()

    # -------------------------------------------------------------------------
    # MusicBrainz lookup helpers
    # -------------------------------------------------------------------------

    def get_selected_playlist_index(self):
        """Return the selected index from the playlist listbox, or current_index if playing, or None."""
        if self.playlist_manager.is_empty():
            return None
        selection = self.playlist_listbox.curselection()
        if selection and selection[0] < self.playlist_manager.count():
            return selection[0]
        if self.current_index is not None and self.current_index < self.playlist_manager.count():
            return self.current_index
        return None

    def lookup_musicbrainz_for_selected_song(self):
        if not MUSICBRAINZ_ENABLED or not self.musicbrainz_service:
            self.show_warning("Disabled", "MusicBrainz integration is disabled.")
            return
        if self.musicbrainz_lookup_in_progress:
            self.show_warning("In Progress", "MusicBrainz lookup is already in progress.")
            return

        index = self.get_selected_playlist_index()
        if index is None:
            self.show_warning("No Selection", "Please select a song first.")
            return

        try:
            song = self.playlist_manager.get_song(index)
        except IndexError:
            return

        self.update_status("Searching MusicBrainz...")
        if hasattr(self, "musicbrainz_button"):
            self.safe_configure(self.musicbrainz_button, state="disabled")
            
        threading.Thread(target=self._musicbrainz_lookup_worker, args=(index, song), daemon=True).start()

    def _musicbrainz_lookup_worker(self, index, song):
        self.musicbrainz_lookup_in_progress = True
        try:
            results = self.musicbrainz_service.search_for_song(song)
            self.root.after(0, self._musicbrainz_lookup_finished, index, results)
        except Exception as e:
            self.root.after(0, self._musicbrainz_lookup_failed, str(e))
        finally:
            self.root.after(0, self._reset_musicbrainz_lookup_state)

    def _reset_musicbrainz_lookup_state(self):
        self.musicbrainz_lookup_in_progress = False
        if hasattr(self, "musicbrainz_button"):
            self.safe_configure(self.musicbrainz_button, state="normal")

    def _musicbrainz_lookup_failed(self, error_message):
        self._reset_musicbrainz_lookup_state()
        self.show_error("MusicBrainz Lookup Failed", f"Could not fetch metadata from MusicBrainz.\n\nDetails: {error_message}")
        self.update_status("MusicBrainz lookup failed")

    def _musicbrainz_lookup_finished(self, index, results):
        self._reset_musicbrainz_lookup_state()
        if not results:
            self.show_warning("No Results", ERROR_MUSICBRAINZ_NO_RESULTS)
            self.update_status("No MusicBrainz matches found")
            return
            
        self.show_musicbrainz_results_dialog(index, results)

    def show_musicbrainz_results_dialog(self, index, results):
        dialog = tk.Toplevel(self.root)
        dialog.title("MusicBrainz Results")
        dialog.geometry("700x400")
        dialog.transient(self.root)
        dialog.grab_set()

        lbl = ttk.Label(dialog, text="Select the best metadata match:")
        lbl.pack(pady=10, padx=10, anchor="w")

        list_frame = ttk.Frame(dialog)
        list_frame.pack(fill="both", expand=True, padx=10, pady=5)
        
        listbox = tk.Listbox(list_frame, font=("Segoe UI", 10))
        listbox.pack(side="left", fill="both", expand=True)
        
        scrollbar = ttk.Scrollbar(list_frame, orient="vertical", command=listbox.yview)
        scrollbar.pack(side="right", fill="y")
        listbox.config(yscrollcommand=scrollbar.set)
        
        for r in results:
            display = f"{r['title']} - {r['artist']} | {r['album']} | {r['duration_text']} | {r['release_date']} | Score: {r['score']}"
            listbox.insert(tk.END, display)
            
        btn_frame = ttk.Frame(dialog)
        btn_frame.pack(fill="x", padx=10, pady=10)
        
        def apply_selected(event=None):
            selection = listbox.curselection()
            if not selection:
                messagebox.showwarning("No Selection", "Please select a MusicBrainz result.", parent=dialog)
                return
            
            selected_result = results[selection[0]]
            
            try:
                self.playlist_manager.apply_musicbrainz_metadata(index, selected_result)
                self.refresh_playlist_display()
                
                if index < self.playlist_manager.count():
                    self.playlist_listbox.selection_clear(0, tk.END)
                    self.playlist_listbox.selection_set(index)
                    self.playlist_listbox.see(index)
                
                if index == self.current_index:
                    song = self.playlist_manager.get_song(index)
                    if hasattr(self, "song_title_label") and self.song_title_label:
                        self.song_title_label.config(text=song["title"])
                    if hasattr(self, "artist_label") and self.artist_label:
                        self.artist_label.config(text=f"Artist: {song['artist']}")
                    if hasattr(self, "album_label") and self.album_label:
                        self.album_label.config(text=f"Album: {song['album']}")
                    if hasattr(self, "duration_label") and self.duration_label:
                        elapsed = self.audio_player.get_elapsed_seconds()
                        elapsed_text = self.format_duration(elapsed)
                        self.duration_label.config(text=f"Duration: {elapsed_text} / {song['duration_text']}")
                        self.current_song_duration = song.get("duration_seconds", 0)
                        
                self.update_status(f"Applied MusicBrainz metadata: {selected_result['title']} - {selected_result['artist']}")
                dialog.destroy()
            except Exception as exc:
                messagebox.showerror("Error", f"Failed to apply metadata: {exc}", parent=dialog)

        apply_btn = ttk.Button(btn_frame, text="Apply Selected", command=apply_selected)
        apply_btn.pack(side="left", padx=5)
        
        cancel_btn = ttk.Button(btn_frame, text="Cancel", command=dialog.destroy)
        cancel_btn.pack(side="right", padx=5)
        
        listbox.bind("<Double-Button-1>", apply_selected)

    def manual_musicbrainz_search(self):
        index = self.get_selected_playlist_index()
        if index is None:
            self.show_warning("No Selection", "Please select a playlist song before manual MusicBrainz search.")
            return

        title = simpledialog.askstring("MusicBrainz Search", "Enter Song Title:")
        if not title or not title.strip():
            return
            
        artist = simpledialog.askstring("MusicBrainz Search", "Enter Artist (optional):")
        album = simpledialog.askstring("MusicBrainz Search", "Enter Album (optional):")
        
        song = {
            "title": title.strip(),
            "artist": artist.strip() if artist else "",
            "album": album.strip() if album else ""
        }
        
        if not MUSICBRAINZ_ENABLED or not self.musicbrainz_service:
            self.show_warning("Disabled", "MusicBrainz integration is disabled.")
            return
        if self.musicbrainz_lookup_in_progress:
            self.show_warning("In Progress", "MusicBrainz lookup is already in progress.")
            return

        self.update_status("Searching MusicBrainz (Manual)...")
        if hasattr(self, "musicbrainz_button"):
            self.safe_configure(self.musicbrainz_button, state="disabled")
            
        threading.Thread(target=self._musicbrainz_lookup_worker, args=(index, song), daemon=True).start()

    # -------------------------------------------------------------------------
    # YouTube streaming helpers
    # -------------------------------------------------------------------------

    def on_youtube_stream_clicked(self):
        """Handle YouTube streaming start request."""
        if not YOUTUBE_STREAMING_ENABLED:
            self.show_warning("Disabled", "YouTube streaming integration is disabled.")
            return

        if not self.stream_player.is_available:
            self.show_error("VLC Missing", ERROR_VLC_NOT_AVAILABLE)
            return

        if not hasattr(self, "youtube_query_entry") or not self.youtube_query_entry:
            return

        query = self.youtube_query_entry.get().strip()
        if not query:
            self.show_warning("Empty Search", ERROR_YOUTUBE_EMPTY_QUERY)
            return

        if self.youtube_lookup_in_progress:
            self.show_warning("In Progress", "YouTube lookup is already in progress.")
            return

        # Stop local pygame playback before starting YouTube stream
        self._stop_and_reset_playback()

        self.update_status(YOUTUBE_STREAM_STATUS_SEARCHING)
        if hasattr(self, "youtube_status_label") and self.youtube_status_label:
            self.youtube_status_label.config(text=YOUTUBE_STREAM_STATUS_SEARCHING)

        if hasattr(self, "youtube_stream_button") and self.youtube_stream_button:
            self.safe_configure(self.youtube_stream_button, state="disabled")

        threading.Thread(target=self._youtube_stream_worker, args=(query,), daemon=True).start()

    def _youtube_stream_worker(self, query):
        """Background thread worker to extract stream info from YouTube."""
        self.youtube_lookup_in_progress = True
        try:
            stream_info = self.youtube_service.extract_stream(query)
            self.root.after(0, self._youtube_stream_ready, stream_info)
        except Exception as e:
            self.root.after(0, self._youtube_stream_failed, str(e))
        finally:
            self.root.after(0, self._youtube_stream_cleanup)

    def _youtube_stream_cleanup(self):
        """Cleanup lookup state on the main thread."""
        self.youtube_lookup_in_progress = False
        if hasattr(self, "youtube_stream_button") and self.youtube_stream_button:
            self.safe_configure(self.youtube_stream_button, state="normal")

    def _youtube_stream_failed(self, error_message):
        """Handle extraction failure on the main thread."""
        self.youtube_streaming_active = False
        self.stop_youtube_stream()
        
        self.show_error(
            "YouTube Stream Error",
            f"Could not start YouTube stream.\n\nDetails: {error_message}"
        )
        self.update_status("YouTube streaming failed")
        if hasattr(self, "youtube_status_label") and self.youtube_status_label:
            self.youtube_status_label.config(text="YouTube streaming failed")

    def _youtube_stream_ready(self, stream_info):
        """Handle successful stream extraction and start playback on the main thread."""
        try:
            self.stream_player.stop()
            self.stream_player.load_stream(stream_info)
            
            # Apply current volume slider setting
            volume = int(self.volume_scale.get()) if hasattr(self, "volume_scale") else DEFAULT_VOLUME
            self.stream_player.set_volume(volume)
            
            # Start playing
            self.stream_player.play()

            self.youtube_streaming_active = True
            self.current_youtube_stream_info = stream_info

            # Update Now Playing labels
            if hasattr(self, "song_title_label") and self.song_title_label:
                self.song_title_label.config(text=stream_info["title"])
            if hasattr(self, "artist_label") and self.artist_label:
                self.artist_label.config(text=f"Uploader: {stream_info['uploader']}")
            if hasattr(self, "album_label") and self.album_label:
                self.album_label.config(text="Source: YouTube")
            if hasattr(self, "duration_label") and self.duration_label:
                self.duration_label.config(
                    text=f"Duration: 00:00 / {stream_info['duration_text']}"
                )

            # Clear playlist selections visually
            self.playlist_listbox.selection_clear(0, tk.END)

            self.update_status(f"Streaming from YouTube: {stream_info['title']}")
            if hasattr(self, "youtube_status_label") and self.youtube_status_label:
                self.youtube_status_label.config(text=f"Streaming: {stream_info['title']}")

            if hasattr(self, "visualizer"):
                self.visualizer.start()

            self.start_youtube_progress_updates()
        except Exception as e:
            self._youtube_stream_failed(str(e))

    def stop_youtube_stream(self):
        """Stop YouTube stream and reset associated UI states."""
        self.stop_youtube_progress_updates()
        if hasattr(self, "stream_player") and self.stream_player:
            self.stream_player.stop()

        self.youtube_streaming_active = False
        self.current_youtube_stream_info = None

        if hasattr(self, "visualizer"):
            self.visualizer.stop()

        self.set_progress_value(0)
        self.reset_now_playing()

        self.update_status("YouTube stream stopped")
        if hasattr(self, "youtube_status_label") and self.youtube_status_label:
            self.youtube_status_label.config(text="YouTube stream stopped")

    def start_youtube_progress_updates(self):
        """Start periodic YouTube progress bar updates."""
        self.stop_youtube_progress_updates()
        self.update_youtube_progress()

    def stop_youtube_progress_updates(self):
        """Stop periodic YouTube progress bar updates."""
        if self.youtube_progress_job is not None:
            self.root.after_cancel(self.youtube_progress_job)
            self.youtube_progress_job = None

    def update_youtube_progress(self):
        """Update progress bar and labels for active YouTube streams."""
        self.youtube_progress_job = None

        if not self.youtube_streaming_active or not self.current_youtube_stream_info:
            self.set_progress_value(0)
            return

        elapsed = self.stream_player.get_elapsed_seconds()
        total_duration = self.current_youtube_stream_info.get("duration_seconds", 0)

        if total_duration > 0:
            elapsed = max(0, min(elapsed, total_duration))
            self.set_progress_value(int((elapsed / total_duration) * 100))
            total_text = self.current_youtube_stream_info.get("duration_text", "00:00")
            elapsed_text = self.format_duration(elapsed)
            if hasattr(self, "duration_label") and self.duration_label:
                self.duration_label.config(text=f"Duration: {elapsed_text} / {total_text}")
        else:
            self.set_progress_value(0)
            elapsed_text = self.format_duration(elapsed)
            if hasattr(self, "duration_label") and self.duration_label:
                self.duration_label.config(text=f"Duration: {elapsed_text} / Live/Unknown")

        # Check if stream ended naturally
        if self.stream_player.is_available:
            try:
                state = self.stream_player.get_state_name()
                if "Ended" in state or "Error" in state:
                    self.update_status("YouTube stream finished")
                    self.stop_youtube_stream()
                    return
            except Exception:
                pass

        self.youtube_progress_job = self.root.after(1000, self.update_youtube_progress)
