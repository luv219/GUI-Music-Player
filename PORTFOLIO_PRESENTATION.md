# PyTune Box Portfolio Presentation

## 20-Second Introduction
"PyTune Box is a desktop music player built with Python and Tkinter. It supports playlist management, metadata display, real-time progress tracking, themes, shuffle and repeat modes, keyboard shortcuts, a simple visualizer, and Windows executable packaging."

## 1-Minute Explanation
- **Problem**: I wanted to understand how desktop applications handle real-time state, multimedia files, and UI responsiveness without blocking the main event loop.
- **Solution**: I built PyTune Box, a lightweight local music player.
- **Tech stack**: Python, Tkinter for the GUI, pygame for audio playback, and mutagen for extracting ID3 metadata.
- **Key features**: Users can load individual files or entire folders, manage their playlists, switch between light and dark themes, and use keyboard shortcuts. The app remembers user preferences via a JSON configuration file.
- **Packaging**: Finally, I used PyInstaller to package the app into a standalone Windows executable so anyone can run it without installing Python.

## Technical Highlights
- **Modular architecture**: The GUI is strictly separated from the audio engine and playlist logic.
- **pygame playback**: Utilizing `pygame.mixer` to handle audio streaming efficiently.
- **mutagen metadata**: Extracting embedded track information, with robust fallback logic if tags are missing.
- **JSON playlist/settings**: Persistent application state management across sessions.
- **PyInstaller packaging**: Overcoming the challenge of bundling multimedia dependencies and hidden imports into a single distributable folder.

## Challenges Solved
- **Playback state handling**: Ensuring the UI stays in sync with the audio backend (e.g., automatically moving to the next track when a song finishes).
- **Playlist validation**: Checking if files still exist before attempting to play them.
- **Missing metadata fallback**: Preventing crashes when users load raw `.wav` or untagged `.mp3` files.
- **Theme persistence**: Dynamically updating all Tkinter widget colors on the fly.
- **Packaging multimedia dependencies**: Writing build scripts that ensure PyInstaller includes all necessary Tkinter and pygame DLLs.

## Future Improvements
- **Album art**: Extracting and displaying embedded cover images.
- **Real visualizer**: Performing Fast Fourier Transform (FFT) on the audio stream for accurate frequency visualization.
- **Installer**: Building a proper Windows setup wizard using tools like Inno Setup.
- **Cross-platform builds**: Creating macOS and Linux distributions.
