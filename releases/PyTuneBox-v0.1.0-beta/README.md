# PyTune Box

A desktop music player built with Python and Tkinter for Windows 10/11.

PyTune Box is designed to be a clean, beginner-friendly music player with playlist management, metadata display, themes, and optional audio visualization.

## Current Status

**Phase 11 complete — Windows executable packaging ready**

### Completed

- All Phase 0 to Phase 10 features
- PyInstaller Windows build script
- Clean build script
- Release ZIP script
- Packaging guide
- Version file

### Visualizer Note

The current visualizer is a simulated Tkinter Canvas bar animation. Real frequency or waveform analysis can be added in a future advanced version.

### Keyboard Shortcuts

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

### Settings File

`data/settings.json`

### Supported Formats

- `.mp3`
- `.wav`
- `.ogg`

### Next Phase

**Phase 12 — Final GitHub cleanup, screenshots, demo GIF/video, and portfolio presentation**

## Setup Instructions (Windows)

### Prerequisites

- Python 3.10 or newer
- Windows 10 or 11

### 1. Clone or download the project

```bash
git clone <repository-url>
cd "GUI Music Player"
```

### 2. Create a virtual environment (recommended)

```bash
python -m venv .venv
.venv\Scripts\activate
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
pip install pytest
```

### 4. Run the application

```bash
python main.py
```

## Build Windows Executable

```bat
pip install -r requirements.txt
build_scripts\build_windows_exe.bat
```

**Output:**

```text
dist\PyTuneBox\PyTuneBox.exe
```

For full packaging instructions, see `PACKAGING_GUIDE.md`.

## Create Release ZIP

```bat
build_scripts\build_release_zip.bat
```

**Output:**

```text
releases\PyTuneBox-v0.1.0-beta.zip
```

## Clean Build

```bat
build_scripts\clean_build.bat
```

## Testing

Run automated tests:

```bash
pip install -r requirements.txt
pip install pytest
pytest
```

Use the manual checklist in `TESTING_CHECKLIST.md` before packaging or release.

## Usage

1. Launch the app with `python main.py` or `dist\PyTuneBox\PyTuneBox.exe`
2. Add audio files or open a folder
3. Play, pause, seek, and manage playlists
4. Toggle light/dark theme and use keyboard shortcuts
5. Watch the visualizer animate while music plays

## Project Structure

```
├── main.py              # Application entry point
├── requirements.txt     # Python dependencies
├── README.md
├── PACKAGING_GUIDE.md   # PyInstaller packaging guide
├── VERSION.txt          # Release version info
├── TESTING_CHECKLIST.md # Manual QA checklist
├── RELEASE_NOTES.md     # Beta release notes
├── .gitignore
├── app/                 # Application modules
│   ├── gui.py           # Main window
│   ├── player.py        # Audio player (pygame mixer)
│   ├── playlist.py      # Playlist manager
│   ├── metadata.py      # Metadata reader (mutagen)
│   ├── themes.py        # Light and dark themes
│   ├── visualizer.py    # Animated bar visualizer
│   └── config.py        # App constants
├── assets/              # Icons and screenshots
├── data/                # Settings and saved playlists
├── tests/               # Unit tests
├── build_scripts/       # Windows packaging scripts
└── releases/            # Generated release ZIP output
```

## Future Roadmap

| Phase | Focus | Status |
|-------|-------|--------|
| Phase 0–10 | Foundation through release readiness | Complete |
| Phase 11 | Windows EXE packaging with PyInstaller | Complete |
| Phase 12 | GitHub cleanup, screenshots, portfolio | Next |

## License

This project is open for learning and personal use.
