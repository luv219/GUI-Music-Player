# PyTune Box Release Notes

## Version

0.1.0-beta

## Release Type

Windows beta build

## Packaging Status

PyInstaller folder-based executable build ready.

## Build Output

`dist/PyTuneBox/PyTuneBox.exe`

## Release ZIP

`releases/PyTuneBox-v0.1.0-beta.zip`

## Completed Features

- Tkinter GUI
- Audio playback
- Playlist management
- Folder import
- Metadata display
- Progress tracking
- Basic seek
- Save/load playlists
- Light/dark theme
- Saved settings
- Shuffle
- Repeat modes
- Keyboard shortcuts
- Simple visualizer
- Improved error handling and validation
- Basic automated tests
- Manual testing checklist
- Windows executable packaging script
- Build cleanup script
- Release ZIP script
- Packaging guide
- Version file

## MusicBrainz Integration
- Added MusicBrainz metadata lookup using musicbrainzngs 0.7.1.
- Added user-triggered metadata search.
- Added candidate result selection dialog.
- Added MusicBrainz metadata application to playlist items.
- Added MusicBrainz metadata persistence in playlist JSON.
- Added offline fallback to local metadata.

Known limitation:
- No fingerprinting yet.
- Search depends on title/artist/album text.
- Original audio files are not modified.

## YouTube Streaming Integration
- Added YouTube search/URL audio streaming.
- Added yt-dlp stream extraction service.
- Added VLC-based streaming player.
- Added background-thread extraction to prevent GUI freeze.
- Added shared controls for stream play/pause, stop, and volume.
- Added YouTube streaming documentation.


## Known Limitations

- YouTube streaming requires VLC Media Player 64-bit to be installed separately.
- Seeking is not supported during YouTube streaming in this phase.
- Seeking may vary by audio format and pygame backend.
- Visualizer is simulated, not frequency-based.
- Supported formats are `.mp3`, `.wav`, and `.ogg`.
- App is not code-signed yet.
- Antivirus false positives may occur with unsigned PyInstaller apps.
- Windows installer is not created yet.
- Portable folder-based release is used.
- One-file EXE is not enabled yet.
- No album art yet.
- No lyrics support yet.
- No AcoustID fingerprint lookup.
- No automatic bulk MusicBrainz lookup.
- No writing metadata back to audio files.

## Next Possible Improvements

- Code signing
- Installer creation
- Album art
- Lyrics
- Real frequency-based visualizer
- Cross-platform builds
- Final GitHub cleanup, screenshots, demo GIF/video, and portfolio presentation

## Documentation and Portfolio Readiness
- Professional README updated.
- User guide added.
- Developer guide added.
- Features documentation added.
- Roadmap added.
- Troubleshooting guide added.
- Screenshot guide added.
- Demo script added.
- Contributing guide added.
- Security notes added.
- Changelog added.
- Project summary added.
- Portfolio presentation added.
