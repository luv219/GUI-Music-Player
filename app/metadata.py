"""

PyTune Box - Metadata Reader



Reads song metadata from audio files using mutagen.

"""



from pathlib import Path



from mutagen import File





class MetadataReader:

    """Reads metadata from supported audio files."""



    def __init__(self):

        """Initialize the metadata reader."""

        pass



    def _get_first_tag_value(self, audio, tag_name, fallback):

        """Return the first tag value if available, otherwise the fallback."""

        try:

            if audio is None:

                return fallback



            tags = getattr(audio, "tags", None)

            if tags is None:

                return fallback



            value = tags.get(tag_name)

            if value is None:

                return fallback



            if isinstance(value, (list, tuple)):

                if not value:

                    return fallback

                text = str(value[0]).strip()

                return text if text else fallback



            text = str(value).strip()

            return text if text else fallback



        except Exception:

            return fallback



    def format_duration(self, seconds):

        """Format seconds into MM:SS display text."""

        try:

            total_seconds = int(seconds)

        except (TypeError, ValueError):

            total_seconds = 0



        if total_seconds < 0:

            total_seconds = 0



        minutes = total_seconds // 60

        secs = total_seconds % 60

        return f"{minutes:02d}:{secs:02d}"



    def safe_filename_title(self, file_path):

        """Return the filename without extension, or a safe fallback title."""

        try:

            path = Path(file_path)

            stem = path.stem.strip()

            if stem:

                return stem

        except Exception:

            pass



        return "Unknown Title"



    def read_metadata(self, file_path):

        """Read metadata from an audio file and return a safe dictionary."""

        path = Path(file_path)



        if not path.exists():

            raise FileNotFoundError(f"File not found: {file_path}")



        if not path.is_file():

            raise FileNotFoundError(f"File not found: {file_path}")



        resolved_path = path.resolve()

        filename = resolved_path.name

        title = self.safe_filename_title(resolved_path)

        artist = "Unknown Artist"

        album = "Unknown Album"

        duration_seconds = 0



        try:

            audio = File(str(resolved_path), easy=True)



            if audio is not None:

                title = self._get_first_tag_value(audio, "title", title)

                artist = self._get_first_tag_value(audio, "artist", "Unknown Artist")

                album = self._get_first_tag_value(audio, "album", "Unknown Album")



                if hasattr(audio, "info") and audio.info is not None:

                    length = getattr(audio.info, "length", None)

                    if length is not None:

                        try:

                            duration_seconds = max(0, int(length))

                        except (TypeError, ValueError):

                            duration_seconds = 0



        except Exception:

            # Corrupted or unsupported metadata falls back to safe defaults

            pass



        duration_text = self.format_duration(duration_seconds)



        return {

            "path": str(resolved_path),

            "filename": filename,

            "title": title,

            "artist": artist,

            "album": album,

            "duration_seconds": duration_seconds,

            "duration_text": duration_text,

        }


