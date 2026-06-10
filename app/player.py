"""

PyTune Box - Audio Player



Handles audio playback using pygame mixer.

"""



import time



import pygame

from pathlib import Path





class AudioPlayer:

    """Handles audio playback with pygame mixer."""



    def __init__(self, volume=0.7):

        """Initialize pygame mixer and set default volume."""

        self._init_state(volume)



        if not self._init_mixer():

            raise RuntimeError("Audio system could not be initialized.")



    @classmethod

    def create_offline(cls, volume=0.7):

        """Create a player instance when audio hardware is unavailable."""

        player = cls.__new__(cls)

        player._init_state(volume)

        player.is_initialized = False

        player.init_error = "Audio system could not be initialized."

        return player



    def _init_state(self, volume):

        """Initialize player state without starting the mixer."""

        self.current_file = None

        self.is_loaded = False

        self.is_playing = False

        self.is_paused = False

        self.is_initialized = False

        self.init_error = None



        if volume > 1.0:

            volume = volume / 100.0



        try:

            volume = float(volume)

        except (TypeError, ValueError):

            volume = 0.7



        self.volume = max(0.0, min(1.0, volume))



        # Playback timing for progress tracking

        self.start_time = 0

        self.pause_started_at = 0

        self.total_paused_time = 0

        self.seek_offset = 0



    @property

    def mixer_ready(self):

        """Backward-compatible alias for mixer initialization state."""

        return self.is_initialized



    def _init_mixer(self):

        """Initialize pygame mixer, trying fallback settings if needed."""

        init_attempts = [

            {},

            {"frequency": 44100, "size": -16, "channels": 2, "buffer": 4096},

            {"frequency": 22050, "size": -16, "channels": 2, "buffer": 4096},

        ]



        for settings in init_attempts:

            try:

                if pygame.mixer.get_init():

                    pygame.mixer.quit()



                pygame.mixer.init(**settings)

                pygame.mixer.music.set_volume(self.volume)

                self.is_initialized = True

                self.init_error = None

                return True

            except pygame.error as exc:

                self.init_error = str(exc)



        self.is_initialized = False

        return False



    def validate_initialized(self):

        """Raise an error if the audio system is not ready."""

        if not self.is_initialized:

            raise RuntimeError("Audio system is not initialized.")



    def _reset_timing(self):

        """Reset playback timing values."""

        self.start_time = 0

        self.pause_started_at = 0

        self.total_paused_time = 0

        self.seek_offset = 0



    def load(self, file_path):

        """Load an audio file for playback."""

        self.validate_initialized()



        path = Path(file_path)



        if not path.exists():

            raise FileNotFoundError(f"File not found: {file_path}")



        if not path.is_file():

            raise FileNotFoundError(f"File not found: {file_path}")



        try:

            pygame.mixer.music.load(str(path))

        except pygame.error as exc:

            raise RuntimeError("Unable to load audio file.") from exc



        self.current_file = str(path.resolve())

        self.is_loaded = True

        self.is_playing = False

        self.is_paused = False

        self._reset_timing()

        return True



    def play(self, start=0):

        """Start playback of the loaded audio file."""

        self.validate_initialized()



        if not self.is_loaded:

            raise RuntimeError("No audio file loaded.")



        try:

            start = max(0, float(start))

        except (TypeError, ValueError):

            start = 0



        try:

            pygame.mixer.music.play(start=start)

        except pygame.error:

            # Some formats/backends do not support start position

            pygame.mixer.music.play()

            start = 0



        self.start_time = time.time()

        self.seek_offset = start

        self.total_paused_time = 0

        self.pause_started_at = 0

        self.is_playing = True

        self.is_paused = False



    def pause(self):

        """Pause playback if currently playing."""

        self.validate_initialized()



        if self.is_playing and not self.is_paused:

            try:

                pygame.mixer.music.pause()

                self.pause_started_at = time.time()

                self.is_paused = True

                self.is_playing = False

            except pygame.error:

                pass



    def resume(self):

        """Resume playback if currently paused."""

        self.validate_initialized()



        if self.is_paused:

            try:

                pygame.mixer.music.unpause()

                self.total_paused_time += time.time() - self.pause_started_at

                self.pause_started_at = 0

                self.is_paused = False

                self.is_playing = True

            except pygame.error:

                pass



    def stop(self):

        """Stop playback."""

        self.validate_initialized()



        try:

            pygame.mixer.music.stop()

        except pygame.error:

            pass



        self.is_playing = False

        self.is_paused = False

        self._reset_timing()



    def get_elapsed_seconds(self):

        """Return elapsed playback time in seconds."""

        if not self.is_loaded:

            return 0



        if not self.is_playing and not self.is_paused:

            return 0



        if self.is_paused:

            if self.start_time == 0:

                return int(self.seek_offset)

            elapsed = (

                self.seek_offset

                + self.pause_started_at

                - self.start_time

                - self.total_paused_time

            )

        else:

            if self.start_time == 0:

                return int(self.seek_offset)

            elapsed = (

                self.seek_offset

                + time.time()

                - self.start_time

                - self.total_paused_time

            )



        return max(0, int(elapsed))



    def seek(self, seconds):

        """Seek to a position in the current song."""

        self.validate_initialized()



        if not self.is_loaded:

            raise RuntimeError("No audio file loaded.")



        try:

            seconds = max(0, float(seconds))

        except (TypeError, ValueError):

            seconds = 0



        try:

            pygame.mixer.music.stop()

        except pygame.error:

            pass



        try:

            pygame.mixer.music.play(start=seconds)

            self.start_time = time.time()

            self.seek_offset = seconds

            self.total_paused_time = 0

            self.pause_started_at = 0

            self.is_playing = True

            self.is_paused = False

            return True

        except pygame.error:

            self.is_playing = False

            self.is_paused = False

            return False



    def is_busy(self):

        """Return True if pygame mixer is currently playing music."""

        self.validate_initialized()



        try:

            return pygame.mixer.music.get_busy()

        except pygame.error:

            return False



    def set_volume(self, volume):

        """Set volume from 0-100 or 0.0-1.0."""

        self.validate_initialized()



        try:

            volume = float(volume)

        except (TypeError, ValueError):

            volume = self.volume



        if volume > 1.0:

            volume = volume / 100.0



        self.volume = max(0.0, min(1.0, volume))



        try:

            pygame.mixer.music.set_volume(self.volume)

        except pygame.error:

            pass



    def get_volume(self):

        """Return volume as a percentage integer (0-100)."""

        return int(round(self.volume * 100))



    def unload(self):

        """Stop playback and unload the current file."""

        if self.is_initialized:

            try:

                self.stop()

            except RuntimeError:

                pass



        try:

            pygame.mixer.music.unload()

        except (pygame.error, AttributeError, RuntimeError):

            # unload() may not exist in older pygame versions

            pass



        self.current_file = None

        self.is_loaded = False



    def quit(self):

        """Stop playback and shut down pygame mixer."""

        if not self.is_initialized:

            return



        try:

            try:

                pygame.mixer.music.stop()

            except pygame.error:

                pass



            self.is_playing = False

            self.is_paused = False

            self._reset_timing()



            pygame.mixer.quit()

        except pygame.error:

            pass

        finally:

            self.is_initialized = False


