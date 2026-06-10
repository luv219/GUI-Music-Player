"""
PyTune Box - MusicBrainz Service

Handles interactions with the MusicBrainz API to fetch song metadata.
"""

import time
import musicbrainzngs
from app.config import (
    MUSICBRAINZ_APP_NAME,
    MUSICBRAINZ_APP_VERSION,
    MUSICBRAINZ_CONTACT,
    MUSICBRAINZ_MAX_RESULTS,
    MUSICBRAINZ_RATE_LIMIT_SECONDS,
)

class MusicBrainzService:
    """Service to fetch metadata from MusicBrainz API."""

    def __init__(self):
        """Initialize the MusicBrainz API service."""
        musicbrainzngs.set_useragent(
            MUSICBRAINZ_APP_NAME,
            MUSICBRAINZ_APP_VERSION,
            MUSICBRAINZ_CONTACT
        )
        self.last_request_time = 0
        self.max_results = MUSICBRAINZ_MAX_RESULTS
        self.rate_limit_seconds = MUSICBRAINZ_RATE_LIMIT_SECONDS

    def wait_for_rate_limit(self):
        """Enforce rate limits before making an API call."""
        current_time = time.time()
        elapsed = current_time - self.last_request_time
        if elapsed < self.rate_limit_seconds:
            time.sleep(self.rate_limit_seconds - elapsed)
        self.last_request_time = time.time()

    def format_duration(self, seconds):
        """Convert seconds to MM:SS."""
        try:
            total_seconds = int(seconds)
        except (TypeError, ValueError):
            return "00:00"

        if total_seconds < 0:
            total_seconds = 0

        minutes = total_seconds // 60
        secs = total_seconds % 60
        return f"{minutes:02d}:{secs:02d}"

    def milliseconds_to_seconds(self, milliseconds):
        """Convert milliseconds to int seconds."""
        if milliseconds is None:
            return 0
        try:
            return int(int(milliseconds) / 1000)
        except (TypeError, ValueError):
            return 0

    def is_unknown_value(self, value):
        """Return True if value is empty or an unknown fallback."""
        if not value:
            return True
        val_lower = str(value).lower().strip()
        return val_lower in [
            "unknown",
            "unknown artist",
            "unknown album",
            "unknown title",
            ""
        ]

    def create_search_terms_from_song(self, song):
        """Extract meaningful search terms from a playlist song dictionary."""
        title = song.get("title", "")
        if not title:
            title = song.get("filename", "")
            # Remove extension for fallback title
            if "." in title:
                title = title.rsplit(".", 1)[0]
        
        artist = song.get("artist", "")
        if self.is_unknown_value(artist):
            artist = None
            
        album = song.get("album", "")
        if self.is_unknown_value(album):
            album = None

        return {
            "title": str(title).strip() if title else None,
            "artist": str(artist).strip() if artist else None,
            "album": str(album).strip() if album else None
        }

    def normalize_recording_result(self, result):
        """Convert a raw MusicBrainz recording dictionary into our normalized format."""
        recording_id = result.get("id", "")
        title = result.get("title", "")
        
        # Extract artist credit name securely
        artist = "Unknown Artist"
        artist_credit = result.get("artist-credit", [])
        if artist_credit and isinstance(artist_credit, list):
            # MusicBrainz artist credits can be complex
            try:
                artist_parts = []
                for ac in artist_credit:
                    if isinstance(ac, dict) and "name" in ac:
                        artist_parts.append(ac.get("name", ""))
                    elif isinstance(ac, str):
                        artist_parts.append(ac)
                if artist_parts:
                    artist = "".join(artist_parts)
            except Exception:
                pass

        # Extract release info
        album = "Unknown Album"
        release_date = ""
        country = ""
        release_list = result.get("release-list", [])
        if release_list and isinstance(release_list, list) and len(release_list) > 0:
            first_release = release_list[0]
            if isinstance(first_release, dict):
                album = first_release.get("title", "Unknown Album")
                release_date = first_release.get("date", "")
                country = first_release.get("country", "")

        # Extract duration
        length_ms = result.get("length")
        duration_seconds = self.milliseconds_to_seconds(length_ms)
        duration_text = self.format_duration(duration_seconds)
        
        # Extract score
        score = result.get("ext:score", "")

        return {
            "musicbrainz_recording_id": recording_id,
            "title": title,
            "artist": artist,
            "album": album,
            "duration_seconds": duration_seconds,
            "duration_text": duration_text,
            "release_date": release_date,
            "country": country,
            "score": str(score),
            "source": "MusicBrainz"
        }

    def search_recordings(self, title=None, artist=None, album=None, limit=None):
        """Query MusicBrainz for recordings and return normalized results."""
        if not title:
            raise ValueError("Song title is required for MusicBrainz search.")

        search_limit = limit if limit else self.max_results
        
        try:
            self.wait_for_rate_limit()
            
            # Use strict parameters if available to narrow down
            kwargs = {"limit": search_limit}
            if title:
                kwargs["recording"] = title
            if artist:
                kwargs["artist"] = artist
            if album:
                kwargs["release"] = album
                
            response = musicbrainzngs.search_recordings(**kwargs)
            
            if "recording-list" not in response:
                return []
                
            raw_results = response["recording-list"]
            normalized_results = []
            
            for raw_result in raw_results:
                if isinstance(raw_result, dict):
                    normalized_results.append(self.normalize_recording_result(raw_result))
                    
            return normalized_results
            
        except musicbrainzngs.NetworkError as exc:
            raise RuntimeError(f"Network error during MusicBrainz lookup: {exc}")
        except musicbrainzngs.ResponseError as exc:
            raise RuntimeError(f"MusicBrainz API error: {exc}")
        except Exception as exc:
            raise RuntimeError(f"Unexpected error during MusicBrainz lookup: {exc}")

    def search_for_song(self, song, limit=None):
        """Search MusicBrainz for a song dictionary."""
        terms = self.create_search_terms_from_song(song)
        if not terms["title"]:
            raise ValueError("Could not extract a valid title from the song for search.")
            
        return self.search_recordings(
            title=terms["title"],
            artist=terms["artist"],
            album=terms["album"],
            limit=limit
        )
