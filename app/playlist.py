"""

PyTune Box - Playlist Manager



Manages the in-memory song playlist independently from the GUI.

"""



import json

from datetime import datetime

from pathlib import Path



from app.config import (

    PLAYLIST_JSON_VERSION,

    SUPPORTED_AUDIO_EXTENSIONS,

    SUPPORTED_PLAYLIST_EXTENSIONS,

)

from app.metadata import MetadataReader





class PlaylistManager:

    """Manages a list of song metadata dictionaries for the music player."""



    def __init__(self):

        """Initialize an empty playlist."""

        self.songs = []

        self.metadata_reader = MetadataReader()



    def _create_fallback_metadata(self, file_path):

        """Create basic metadata when reading tags fails."""

        path = Path(file_path).resolve()



        return {

            "path": str(path),

            "filename": path.name,

            "title": self.metadata_reader.safe_filename_title(path),

            "artist": "Unknown Artist",

            "album": "Unknown Album",

            "duration_seconds": 0,

            "duration_text": "00:00",

        }



    def _build_display_name(self, song):

        """Build a playlist display string from song metadata."""

        return f"{song['title']} - {song['artist']} [{song['duration_text']}]"



    def add_song(self, file_path):

        """Add a single song if it is valid and not already in the playlist."""

        path = Path(file_path)



        if not path.exists() or not path.is_file():

            return False



        resolved_path = path.resolve()



        if resolved_path.suffix.lower() not in SUPPORTED_AUDIO_EXTENSIONS:

            return False



        if self.contains(resolved_path):

            return False



        try:

            metadata = self.metadata_reader.read_metadata(resolved_path)

        except Exception:

            metadata = self._create_fallback_metadata(resolved_path)



        self.songs.append(metadata)

        return True



    def add_songs(self, file_paths):

        """Add multiple songs and return how many were added."""

        added_count = 0



        for file_path in file_paths:

            if self.add_song(file_path):

                added_count += 1



        return added_count



    def add_folder(self, folder_path, recursive=False):

        """Scan a folder for supported audio files and add them."""

        folder = Path(folder_path)



        if not folder.exists() or not folder.is_dir():

            return 0



        folder = folder.resolve()

        added_count = 0

        matched_files = []



        try:

            if recursive:

                iterator = folder.rglob("*")

            else:

                iterator = folder.glob("*")



            for item in iterator:

                if (

                    item.is_file()

                    and item.suffix.lower() in SUPPORTED_AUDIO_EXTENSIONS

                ):

                    matched_files.append(item)

        except OSError:

            return 0



        matched_files.sort(key=lambda item: item.name.lower())



        for item in matched_files:

            if self.add_song(item):

                added_count += 1



        return added_count



    def remove_song(self, index):

        """Remove and return the song dictionary at the given index."""

        if index < 0 or index >= len(self.songs):

            raise IndexError("Invalid playlist index.")



        return self.songs.pop(index)



    def clear_playlist(self):

        """Remove all songs from the playlist."""

        self.songs.clear()



    def get_songs(self):

        """Return a copy of the current song list."""

        return self.songs.copy()



    def get_song(self, index):

        """Return the song dictionary at the given index."""

        if index < 0 or index >= len(self.songs):

            raise IndexError("Invalid playlist index.")



        return self.songs[index]



    def get_song_path(self, index):

        """Return the absolute file path for the song at the given index."""

        return self.get_song(index)["path"]



    def count(self):

        """Return the number of songs in the playlist."""

        return len(self.songs)



    def is_empty(self):

        """Return True if the playlist has no songs."""

        return len(self.songs) == 0



    def contains(self, file_path):

        """Return True if the absolute file path is already in the playlist."""

        absolute_path = str(Path(file_path).resolve())

        return any(song["path"] == absolute_path for song in self.songs)



    def get_display_names(self):

        """Return display strings for the playlist listbox."""

        return [self._build_display_name(song) for song in self.songs]



    def get_display_name(self, index):

        """Return one display string for the song at the given index."""

        return self._build_display_name(self.get_song(index))



    def export_paths(self):

        """Return a list of file paths from the current playlist."""

        return [song["path"] for song in self.songs]



    def get_playlist_summary(self):

        """Return a summary of the current playlist."""

        return {

            "song_count": self.count(),

            "songs": self.get_songs(),

        }



    def save_to_json(self, file_path, playlist_name="Untitled Playlist"):

        """Save the current playlist to a JSON file."""

        path = Path(file_path)



        try:

            path.parent.mkdir(parents=True, exist_ok=True)



            playlist_data = {

                "app": "PyTune Box",

                "playlist_version": PLAYLIST_JSON_VERSION,

                "playlist_name": playlist_name,

                "created_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),

                "song_count": self.count(),

                "songs": self.get_songs(),

            }



            with open(path, "w", encoding="utf-8") as file:

                json.dump(playlist_data, file, indent=4, ensure_ascii=False)



            return True



        except Exception as exc:

            raise RuntimeError(f"Failed to save playlist: {exc}") from exc



    def load_from_json(self, file_path):

        """Load a playlist from a JSON file and refresh song metadata."""

        path = Path(file_path)



        if not path.exists() or not path.is_file():

            raise FileNotFoundError(f"Playlist file not found: {file_path}")



        if path.suffix.lower() not in SUPPORTED_PLAYLIST_EXTENSIONS:

            raise ValueError("Invalid playlist file format.")



        try:

            with open(path, "r", encoding="utf-8") as file:

                data = json.load(file)

        except json.JSONDecodeError as exc:

            raise ValueError("Invalid playlist file format.") from exc



        if not isinstance(data, dict) or "songs" not in data:

            raise ValueError("Invalid playlist file format.")



        if not isinstance(data["songs"], list):

            raise ValueError("Invalid playlist file format.")



        playlist_name = data.get("playlist_name", "Untitled Playlist")



        new_songs = []

        loaded = 0

        skipped = 0

        missing_files = []

        seen_paths = set()



        for item in data["songs"]:

            if not isinstance(item, dict):

                skipped += 1

                continue



            song_path = item.get("path")

            if not song_path:

                skipped += 1

                continue



            song_file = Path(song_path)



            if not song_file.exists() or not song_file.is_file():

                missing_files.append(song_path)

                skipped += 1

                continue



            if song_file.suffix.lower() not in SUPPORTED_AUDIO_EXTENSIONS:

                skipped += 1

                continue



            absolute_path = str(song_file.resolve())



            if absolute_path in seen_paths:

                skipped += 1

                continue



            try:

                metadata = self.metadata_reader.read_metadata(song_file)

            except Exception:

                metadata = self._create_fallback_metadata(song_file)



            new_songs.append(metadata)

            seen_paths.add(absolute_path)

            loaded += 1



        # Replace the playlist only after JSON is parsed and processed successfully

        self.songs = new_songs



        return {

            "loaded": loaded,

            "skipped": skipped,

            "missing_files": missing_files,

            "playlist_name": playlist_name,

        }


