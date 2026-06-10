# PyTune Box Troubleshooting

## App does not start
**Solutions:**
- Check if Python is installed correctly.
- Run `python --version` in your terminal to verify.
- Make sure to install dependencies from `requirements.txt`.
- Run the app from a terminal using `python main.py` to see if there are any error messages.

## pygame is missing
**Command:**
```bash
pip install pygame
```

## mutagen is missing
**Command:**
```bash
pip install mutagen
```

## Music does not play
**Possible causes:**
- The selected file has an unsupported format.
- The audio file is corrupted.
- Your system's audio device is unavailable or muted.
- There is a backend issue with the `pygame` mixer.

## Seek does not work
**Explain:**
Seeking depends on the audio format and the `pygame` backend capabilities. Seeking may be imprecise or fail entirely for some file types (like certain OGG or VBR MP3 files).

## Playlist does not load
**Possible causes:**
- The playlist JSON file is invalid or corrupted.
- Some files in the playlist are missing from their original location.
- The paths stored in the JSON are unsupported or no longer valid.
- The file was moved or deleted manually.

## Theme not saving
**Check:**
Verify that the `data/settings.json` file exists and is writable. The application needs write permissions in the `data` directory to save settings.

## MusicBrainz lookup fails
**Possible causes:**
- No internet connection
- MusicBrainz service temporarily unavailable
- Rate limiting
- Search terms too weak
- Song has poor local metadata

**Solutions:**
- Try again after a short wait.
- Use Manual MusicBrainz Search.
- Add better title/artist information.
- Check internet connection.

## EXE does not open
**Solution:**
Run the executable from a terminal to see error output:
```cmd
dist\PyTuneBox\PyTuneBox.exe
```

## Antivirus warning
Unsigned PyInstaller apps can sometimes trigger false-positive warnings from antivirus software.
**Recommendation:**
- Build the executable yourself from source.
- Use a code signing certificate before distributing the app publicly.

## Missing app icon
Add an `.ico` file to the assets folder:
`assets/icons/app.ico`
Then rebuild the executable using the build script.

## YouTube streaming does not work
**Possible causes:**
- VLC Media Player is not installed.
- python-vlc cannot find VLC runtime.
- Internet is disconnected.
- yt-dlp extraction failed.
- YouTube result is unavailable.
- Firewall blocks VLC.

**Solutions:**
- Install VLC Media Player 64-bit on your system.
- Restart the terminal or your IDE after VLC installation.
- Run `pip install yt-dlp python-vlc` to ensure dependencies are installed.
- Try a different search term or URL.
- Test local file playback separately to isolate the issue.
- Run the app from terminal to check any output/logs.

## Release ZIP not created
Run the build script first:
```bat
build_scripts\build_windows_exe.bat
```
Then run the release script:
```bat
build_scripts\build_release_zip.bat
```
