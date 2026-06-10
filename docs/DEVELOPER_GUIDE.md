# PyTune Box Developer Guide

## Project Architecture
PyTune Box is designed with a layered architecture to keep components separated:
- **GUI Layer**: Built with Tkinter, manages the visual interface.
- **Audio Player Service**: Handles playback, pause, stop, and volume using pygame.
- **Playlist Manager**: Manages the list of songs, adding, removing, and iterating over tracks.
- **Metadata Reader**: Extracts track information (title, artist, album, duration) using mutagen.
- **Theme System**: Manages color schemes (light and dark mode) and applies them to widgets.
- **Visualizer**: Controls the simulated Tkinter Canvas bar animation.
- **JSON Storage**: Handles loading and saving playlists and app settings.
- **Packaging Scripts**: Automates the creation of Windows executables and release ZIPs.

## Important Files

| File/Folder | Purpose |
|-------------|---------|
| `main.py` | Application entry point |
| `app/gui.py` | Main application window and UI elements |
| `app/player.py` | Audio playback wrapper (pygame) |
| `app/playlist.py` | Playlist and queue management |
| `app/metadata.py` | Metadata extraction (mutagen) |
| `app/themes.py` | Light and dark theme dictionaries |
| `app/visualizer.py` | Animated canvas visualizer logic |
| `app/config.py` | Application constants and configuration |
| `app/musicbrainz_service.py` | MusicBrainz API integration service |
| `data/settings.json` | Saved user settings and state |
| `build_scripts/` | PyInstaller build and packaging scripts |

## MusicBrainz Service
- `app/musicbrainz_service.py` handles API setup and search.
- GUI calls it from a background thread to prevent freezing.
- Tkinter updates are routed through `root.after()`.
- `PlaylistManager` stores the enriched metadata.
- Tests in `test_musicbrainz_service.py` avoid real network calls.

## Setup Development Environment

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
```

## Run App

```bash
python main.py
```

## Run Tests

```bash
pip install pytest
pytest
```

## Audio Backend
PyTune Box uses the `pygame.mixer` module for audio playback. While robust and easy to use, it has limitations, particularly regarding precise seeking and broad format support beyond standard `.mp3`, `.wav`, and `.ogg` files.

## Metadata Backend
The `mutagen` library is used for reading audio metadata. If `mutagen` fails to read metadata or if the file lacks tags, the application falls back to using the filename for the title and displays generic values for the artist and album.

## Playlist Storage
Playlists are stored in JSON format, containing a list of absolute file paths to the audio files in the playlist.

## Settings Storage
User preferences are stored in `data/settings.json`. This file is updated automatically when settings like volume, theme, shuffle, or repeat modes are changed, ensuring persistence across sessions.

## Theme System
The theme system uses dictionaries in `app/themes.py` to define color variables for different UI elements (backgrounds, text, highlights) in both light and dark modes.

## Visualizer
The current visualizer is a simulated Tkinter Canvas animation. It uses random bar heights synced to the play/pause state rather than actual frequency analysis, keeping the implementation lightweight and dependency-free.

## Packaging
Refer to the [Packaging Guide](../PACKAGING_GUIDE.md) for details on building the PyInstaller Windows executable and release ZIP file.

## Coding Rules
- **Keep GUI logic separate**: Do not mix GUI updates directly within playlist or metadata logic.
- **Avoid direct Tkinter usage in non-GUI modules**: Use callbacks or return values to communicate with the GUI layer.
- **Keep errors user-friendly**: Catch exceptions and display clean error messages to the user rather than crashing.
- **Keep code beginner-readable**: Use clear variable names and add comments to complex sections to aid learning.
