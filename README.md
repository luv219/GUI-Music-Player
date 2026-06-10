# PyTune Box

PyTune Box is a Python Tkinter desktop music player with playlist management, metadata display, real-time progress tracking, theme switching, shuffle/repeat modes, keyboard shortcuts, and Windows executable packaging.

![Python](https://img.shields.io/badge/Python-3.10%2B-blue)
![Tkinter](https://img.shields.io/badge/Tkinter-GUI-green)
![pygame](https://img.shields.io/badge/pygame-audio-yellow)
![mutagen](https://img.shields.io/badge/mutagen-metadata-orange)
![Windows](https://img.shields.io/badge/Windows-10%2F11-blue)
![Beta](https://img.shields.io/badge/Status-Beta-red)

## Overview
PyTune Box is designed to be a clean, beginner-friendly desktop music player. It handles basic audio playback needs while showcasing fundamental desktop application development concepts. With its modular architecture, the project provides a solid foundation for further expansion. 

The application is built entirely using Python, utilizing Tkinter for the GUI, pygame for audio playback, and mutagen for extracting metadata from audio files.

## Key Features
- Desktop GUI built with Tkinter
- Open audio files
- Open folders
- Playlist management
- Remove selected songs
- Clear playlist
- Save/load playlists using JSON
- MusicBrainz metadata lookup
- User-selected MusicBrainz result application
- MusicBrainz metadata saved in playlist JSON
- Offline fallback to local metadata
- Metadata display
- Duration display
- Real-time progress tracking
- Basic seek support
- Volume control
- Shuffle mode
- Repeat Off / Repeat One / Repeat All
- Keyboard shortcuts
- Light/dark theme
- Saved settings
- Simple animated visualizer
- Windows executable packaging using PyInstaller

## Screenshots
Screenshots will be stored in `assets/screenshots/`.

- `01-light-theme.png`
- `02-dark-theme.png`
- `03-playlist-loaded.png`
- `04-now-playing.png`
- `05-packaged-app.png`

## Demo
Demo GIF/video will be stored in `assets/demo/`.

- `pytune-box-demo.gif`
- `pytune-box-demo.mp4`

## Tech Stack
| Technology | Usage |
|------------|-------|
| Python | Core language |
| Tkinter | Desktop GUI framework |
| pygame | Audio playback backend |
| mutagen | Audio metadata extraction |
| musicbrainzngs 0.7.1 | MusicBrainz API integration |
| JSON | Settings and playlist storage |
| PyInstaller | Windows executable packaging |
| pytest | Automated testing |

## Project Structure
```
├── app/                 # Application modules
│   ├── gui.py           # Main window GUI
│   ├── player.py        # Audio player wrapper
│   ├── playlist.py      # Playlist logic
│   ├── metadata.py      # Metadata extraction
│   ├── themes.py        # Theme definitions
│   ├── visualizer.py    # Simulated visualizer
│   └── config.py        # Configuration
├── assets/              # Icons, screenshots, demo media
├── build_scripts/       # Scripts for packaging and release
├── data/                # Settings and playlist storage
├── docs/                # Comprehensive documentation
├── tests/               # Unit tests
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
└── VERSION.txt          # Release version information
```

## Installation for Development

```bash
python -m venv .venv
.venv\Scripts\activate
pip install -r requirements.txt
python main.py
```

## Run Tests

```bash
pip install pytest
pytest
```

## Build Windows Executable

```bat
build_scripts\build_windows_exe.bat
```

**Output:**
`dist\PyTuneBox\PyTuneBox.exe`

## Create Release ZIP

```bat
build_scripts\build_release_zip.bat
```

**Output:**
`releases\PyTuneBox-v0.1.0-beta.zip`

## Keyboard Shortcuts

| Shortcut | Action |
|----------|--------|
| Space | Play/Pause |
| S | Stop |
| Right Arrow | Next |
| Left Arrow | Previous |
| H | Shuffle |
| R | Repeat |
| Ctrl+O | Open Files |
| Ctrl+Shift+O | Open Folder |
| Ctrl+S | Save Playlist |
| Ctrl+L | Load Playlist |

## Supported Audio Formats
- `.mp3`
- `.wav`
- `.ogg`

## MusicBrainz Metadata Lookup
PyTune Box can search MusicBrainz for improved song metadata. Select a song, then use **Tools > Lookup Metadata on MusicBrainz** or the **Lookup MusicBrainz** button. The app shows possible matches and lets you apply the selected result to the playlist item.

- The app does not modify original audio files.
- MusicBrainz metadata is saved when saving playlist JSON.
- Internet connection is required.
- Local metadata still works offline.

See [docs/MUSICBRAINZ_INTEGRATION.md](docs/MUSICBRAINZ_INTEGRATION.md).

## Current Status
**Version:** 0.1.0-beta
**Status:** Beta / Portfolio-ready

## Known Limitations
- Seeking support depends on pygame and audio format.
- Visualizer is simulated, not frequency-based.
- No album art yet.
- No lyrics support yet.
- No installer yet.
- App is not code-signed.
- Supported formats are limited to .mp3, .wav, and .ogg.

## Roadmap
See [Roadmap](docs/ROADMAP.md) for planned features and improvements.

## Documentation
- [User Guide](docs/USER_GUIDE.md)
- [Developer Guide](docs/DEVELOPER_GUIDE.md)
- [Features](docs/FEATURES.md)
- [Troubleshooting](docs/TROUBLESHOOTING.md)
- [Packaging Guide](PACKAGING_GUIDE.md)
- [Testing Checklist](TESTING_CHECKLIST.md)
- [Release Notes](RELEASE_NOTES.md)

## License
License not selected yet. Add a LICENSE file before public release if required.

## Author / Project
PyTune Box Project
