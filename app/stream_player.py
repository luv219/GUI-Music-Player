"""
PyTune Box - VLC-based Stream Player

Provides playback of direct stream URLs using the python-vlc wrapper and the VLC Media Player runtime.
"""

import time
from app.config import ERROR_VLC_NOT_AVAILABLE

try:
    import vlc
except Exception:
    vlc = None

class StreamPlayer:
    def __init__(self, volume=70):
        """Initialize the StreamPlayer using python-vlc, fallback safely if VLC is missing."""
        self.is_available = False
        self.instance = None
        self.player = None
        
        self.current_stream = None
        self.current_title = None
        self.is_playing = False
        self.is_paused = False
        self.start_time = 0
        self.pause_started_at = 0
        self.total_paused_time = 0
        self.duration_seconds = 0
        self.volume = max(0, min(100, int(volume)))

        if vlc is not None:
            try:
                # --no-video ensures VLC doesn't open an external video window for audio streams
                # --no-interact and --quiet prevent VLC from spawning OS-level error dialogs
                self.instance = vlc.Instance("--no-video", "--no-interact", "--quiet")
                self.player = self.instance.media_player_new()
                self.is_available = True
                self.player.audio_set_volume(self.volume)
            except Exception:
                self.is_available = False
                self.instance = None
                self.player = None

    def validate_available(self):
        """Raise RuntimeError if VLC Player is not installed or available."""
        if not self.is_available or self.player is None:
            raise RuntimeError(ERROR_VLC_NOT_AVAILABLE)

    def load_stream(self, stream_info):
        """Load a stream from stream info dict containing 'stream_url'."""
        self.validate_available()
        if not stream_info or "stream_url" not in stream_info:
            raise RuntimeError("Missing direct stream URL.")

        stream_url = stream_info["stream_url"]
        try:
            media = self.instance.media_new(stream_url)
            self.player.set_media(media)
            self.current_stream = stream_info
            self.current_title = stream_info.get("title")
            self.duration_seconds = stream_info.get("duration_seconds", 0)
            self.is_playing = False
            self.is_paused = False
            self.start_time = 0
            self.pause_started_at = 0
            self.total_paused_time = 0
            return True
        except Exception as e:
            raise RuntimeError(f"Failed to load stream in VLC: {str(e)}")

    def play(self):
        """Start playing the loaded stream."""
        self.validate_available()
        if not self.current_stream:
            raise RuntimeError("No stream loaded.")

        try:
            self.player.play()
            self.is_playing = True
            self.is_paused = False
            self.start_time = time.time()
            self.total_paused_time = 0
            self.pause_started_at = 0
            return True
        except Exception as e:
            raise RuntimeError(f"VLC playback start failed: {str(e)}")

    def pause(self):
        """Toggle pause state."""
        self.validate_available()
        if not self.is_playing and not self.is_paused:
            return False

        try:
            self.player.pause()
            if self.is_playing:
                self.is_playing = False
                self.is_paused = True
                self.pause_started_at = time.time()
            else:
                self.is_playing = True
                self.is_paused = False
                if self.pause_started_at > 0:
                    self.total_paused_time += time.time() - self.pause_started_at
                self.pause_started_at = 0
            return True
        except Exception as e:
            raise RuntimeError(f"VLC pause toggle failed: {str(e)}")

    def resume(self):
        """Resume playback if currently paused."""
        self.validate_available()
        if self.is_paused:
            try:
                self.player.set_pause(0)
                self.is_playing = True
                self.is_paused = False
                if self.pause_started_at > 0:
                    self.total_paused_time += time.time() - self.pause_started_at
                self.pause_started_at = 0
                return True
            except Exception as e:
                raise RuntimeError(f"VLC resume failed: {str(e)}")
        return False

    def stop(self):
        """Stop playback and reset state."""
        if self.is_available and self.player:
            try:
                self.player.stop()
            except Exception:
                pass
        self.is_playing = False
        self.is_paused = False
        self.start_time = 0
        self.pause_started_at = 0
        self.total_paused_time = 0

    def set_volume(self, volume):
        """Set playback volume (clamped 0 to 100)."""
        self.volume = max(0, min(100, int(volume)))
        if self.is_available and self.player:
            try:
                self.player.audio_set_volume(self.volume)
            except Exception:
                pass
        return self.volume

    def get_volume(self):
        """Return the current volume setting."""
        return self.volume

    def get_elapsed_seconds(self):
        """Return the current elapsed time in seconds."""
        if not self.is_playing and not self.is_paused:
            return 0
            
        if self.is_available and self.player:
            try:
                current_ms = self.player.get_time()
                if current_ms and current_ms > 0:
                    return current_ms // 1000
            except Exception:
                pass

        # Fallback to internal time tracking
        if self.is_playing:
            elapsed = time.time() - self.start_time - self.total_paused_time
            return max(0, int(elapsed))
        elif self.is_paused:
            elapsed = self.pause_started_at - self.start_time - self.total_paused_time
            return max(0, int(elapsed))
        return 0

    def get_state_name(self):
        """Safely return the string representation of the VLC player state."""
        if not self.is_available or self.player is None:
            return "unavailable"
        try:
            state = self.player.get_state()
            return str(state)
        except Exception:
            return "unknown"

    def is_busy(self):
        """Return True if player is playing or buffering."""
        if not self.is_available or self.player is None:
            return False
        try:
            state = self.player.get_state()
            return state in (vlc.State.Playing, vlc.State.Opening, vlc.State.Buffering)
        except Exception:
            return self.is_playing

    def quit(self):
        """Safely stop and release player/instance resources."""
        self.stop()
        if self.player:
            try:
                self.player.release()
            except Exception:
                pass
            self.player = None
        if self.instance:
            try:
                self.instance.release()
            except Exception:
                pass
            self.instance = None
        self.is_available = False
