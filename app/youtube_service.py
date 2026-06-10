"""
PyTune Box - YouTube Stream Extraction Service

Provides search and direct audio stream URL extraction using yt-dlp.
"""

import re
import yt_dlp
from app.config import (
    YOUTUBE_YTDLP_OPTIONS,
    YOUTUBE_MAX_RESULTS,
    ERROR_YOUTUBE_EMPTY_QUERY,
    ERROR_YOUTUBE_NO_RESULTS,
    ERROR_YOUTUBE_EXTRACTION_FAILED,
)

class YouTubeService:
    def __init__(self, options=None):
        """Initialize YouTubeService with yt-dlp options."""
        if options is None:
            self.options = YOUTUBE_YTDLP_OPTIONS.copy()
        else:
            self.options = options.copy()

    def is_probable_url(self, text):
        """Return True if the text looks like a URL starting with http://, https://, or www."""
        if not text:
            return False
        cleaned = text.strip().lower()
        return cleaned.startswith("http://") or cleaned.startswith("https://") or cleaned.startswith("www.")

    def normalize_query(self, query):
        """Normalize the user query: strip whitespace, check for emptiness, identify URLs."""
        if not query:
            raise ValueError(ERROR_YOUTUBE_EMPTY_QUERY)
        
        normalized = query.strip()
        if not normalized:
            raise ValueError(ERROR_YOUTUBE_EMPTY_QUERY)
            
        return normalized

    def format_duration(self, seconds):
        """Convert seconds (int/float) to MM:SS string format. Handles null/negative values."""
        if seconds is None:
            return "00:00"
        try:
            sec_val = int(float(seconds))
            if sec_val < 0:
                return "00:00"
            mins = sec_val // 60
            secs = sec_val % 60
            return f"{mins:02d}:{secs:02d}"
        except (ValueError, TypeError):
            return "00:00"

    def sanitize_text(self, value, fallback=""):
        """Safely convert value to string, strip whitespace, and return fallback if empty."""
        if value is None:
            return fallback
        try:
            stringified = str(value).strip()
            return stringified if stringified else fallback
        except Exception:
            return fallback

    def choose_best_audio_url(self, info):
        """Select the best audio stream URL from the extracted info."""
        if not info:
            return None
            
        # If there's a direct url at the top level, use it
        if "url" in info and info["url"]:
            return info["url"]

        formats = info.get("formats", [])
        if not formats:
            return None

        # Filter to formats containing url
        valid_formats = [f for f in formats if f.get("url")]
        if not valid_formats:
            return None

        # Try to find audio-only formats first
        audio_only = []
        for f in valid_formats:
            vcodec = f.get("vcodec")
            acodec = f.get("acodec")
            # In yt-dlp vcodec can be 'none' or None
            is_video_none = (vcodec == "none" or vcodec is None)
            is_audio_valid = (acodec != "none" and acodec is not None)
            if is_video_none and is_audio_valid:
                audio_only.append(f)

        target_formats = audio_only if audio_only else valid_formats

        # Sort by average bitrate (abr) if present, highest first
        def get_abr(fmt):
            try:
                return float(fmt.get("abr", 0) or 0)
            except (ValueError, TypeError):
                return 0.0

        sorted_formats = sorted(target_formats, key=get_abr, reverse=True)
        if sorted_formats:
            return sorted_formats[0]["url"]

        return None

    def extract_stream(self, query):
        """Extract streaming metadata and direct stream URL for the given query/URL."""
        normalized = self.normalize_query(query)
        
        # If it's not a URL, yt-dlp will use the default_search prefix automatically,
        # but to guarantee single video extraction, we can check and prefix or use options.
        search_query = normalized
        if not self.is_probable_url(normalized):
            search_query = f"ytsearch1:{normalized}"

        try:
            with yt_dlp.YoutubeDL(self.options) as ydl:
                info = ydl.extract_info(search_query, download=False)
        except Exception as e:
            raise RuntimeError(f"{ERROR_YOUTUBE_EXTRACTION_FAILED} Details: {str(e)}")

        if not info:
            raise RuntimeError(ERROR_YOUTUBE_NO_RESULTS)

        # If it's a search result list, take the first entry
        if "entries" in info:
            entries = info.get("entries", [])
            # Filter out None entries
            valid_entries = [e for e in entries if e is not None]
            if not valid_entries:
                raise RuntimeError(ERROR_YOUTUBE_NO_RESULTS)
            info = valid_entries[0]

        stream_url = self.choose_best_audio_url(info)
        if not stream_url:
            raise RuntimeError(ERROR_YOUTUBE_EXTRACTION_FAILED)

        # Normalize duration
        duration_sec = info.get("duration")
        try:
            duration_seconds = int(float(duration_sec)) if duration_sec is not None else 0
        except (ValueError, TypeError):
            duration_seconds = 0

        duration_text = self.format_duration(duration_seconds)

        return {
            "source": "YouTube",
            "id": self.sanitize_text(info.get("id")),
            "title": self.sanitize_text(info.get("title"), "Unknown YouTube Title"),
            "uploader": self.sanitize_text(info.get("uploader"), "Unknown Uploader"),
            "duration_seconds": duration_seconds,
            "duration_text": duration_text,
            "webpage_url": self.sanitize_text(info.get("webpage_url")),
            "stream_url": stream_url,
            "thumbnail": self.sanitize_text(info.get("thumbnail")),
            "extractor": self.sanitize_text(info.get("extractor")),
            "raw_query": query,
        }

    def search_results(self, query, limit=None):
        """Perform a YouTube search and return lightweight result summaries."""
        normalized = self.normalize_query(query)
        if self.is_probable_url(normalized):
            # If it's a direct URL, extract metadata for it directly
            try:
                with yt_dlp.YoutubeDL(self.options) as ydl:
                    info = ydl.extract_info(normalized, download=False)
                if not info:
                    return []
                # Handle playlist vs single video
                if "entries" in info:
                    entries = [e for e in info.get("entries", []) if e is not None]
                else:
                    entries = [info]
            except Exception:
                return []
        else:
            search_limit = limit if limit is not None else YOUTUBE_MAX_RESULTS
            search_query = f"ytsearch{search_limit}:{normalized}"
            try:
                with yt_dlp.YoutubeDL(self.options) as ydl:
                    info = ydl.extract_info(search_query, download=False)
                if not info or "entries" not in info:
                    return []
                entries = [e for e in info.get("entries", []) if e is not None]
            except Exception:
                return []

        results = []
        for entry in entries:
            duration_sec = entry.get("duration")
            try:
                duration_seconds = int(float(duration_sec)) if duration_sec is not None else 0
            except (ValueError, TypeError):
                duration_seconds = 0
            duration_text = self.format_duration(duration_seconds)

            results.append({
                "title": self.sanitize_text(entry.get("title"), "Unknown YouTube Title"),
                "uploader": self.sanitize_text(entry.get("uploader"), "Unknown Uploader"),
                "duration_seconds": duration_seconds,
                "duration_text": duration_text,
                "webpage_url": self.sanitize_text(entry.get("webpage_url")),
                "id": self.sanitize_text(entry.get("id")),
                "source": "YouTube",
            })
        return results
