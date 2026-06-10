# PyTune Box User Guide

## What is PyTune Box?
PyTune Box is a beginner-friendly desktop music player that lets you easily play your local music files, manage playlists, and customize your listening experience with different themes and a simulated visualizer.

## Starting the App
**Development:**
```bash
python main.py
```

**Packaged:**
```bat
dist\PyTuneBox\PyTuneBox.exe
```

## Opening Songs
**Steps:**
1. Go to **File > Open Files**
2. Select your `.mp3`, `.wav`, or `.ogg` files.
3. The selected songs will appear in your playlist.

## Opening a Folder
**Steps:**
1. Go to **File > Open Folder**
2. Select the folder containing your music.
3. Choose whether to include subfolders when prompted.
4. All supported songs in the folder will appear in your playlist.

## Playing Music
- **Double-click** a song in the playlist to start playing it immediately.
- Use the **Play/Pause** button to start or pause the current track.
- Use the **Stop** button to halt playback completely.
- Use the **Next/Previous** buttons to skip between tracks.

## Volume Control
Use the volume slider to adjust the audio level to your preference.

## Progress and Seek
- The **Progress** bar shows the elapsed time and total duration of the track.
- Dragging the progress bar may seek to different parts of the song (note: seeking support may vary by file format due to backend limitations).

## Playlist Management
- **Remove Selected**: Removes the highlighted song(s) from the playlist.
- **Clear Playlist**: Empties the entire playlist.
- **Save Playlist**: Saves the current playlist so you can load it later.
- **Load Playlist**: Loads a previously saved playlist.

## MusicBrainz Metadata Lookup
**Steps:**
1. Add songs to playlist.
2. Select a song.
3. Click Lookup MusicBrainz or use Tools > Lookup Metadata on MusicBrainz.
4. Wait for results.
5. Select the best match.
6. Click Apply Selected.
7. Save playlist if you want to preserve MusicBrainz metadata.

*Note: Original audio files are not changed.*

## Theme Switching
- Go to **View > Toggle Theme** or use the **Toggle Theme** button to switch between Light and Dark modes.
- Your theme preference is automatically saved.

## Shuffle and Repeat
- **Shuffle On/Off**: Randomizes the order in which songs are played.
- **Repeat Off**: Stops playback after the playlist finishes.
- **Repeat One**: Repeats the currently playing song continuously.
- **Repeat All**: Repeats the entire playlist from the beginning once it finishes.

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

## Visualizer
The app features a simulated visualizer with animated bars that sync with the play, pause, and stop states, adding a dynamic visual element to your music playback.

## Settings
Your preferences are automatically saved in `data/settings.json`, including:
- Theme (Light/Dark)
- Volume level
- Last loaded playlist
- Shuffle state
- Repeat mode

## Common Issues
If you experience any issues, please refer to the [Troubleshooting Guide](TROUBLESHOOTING.md).
