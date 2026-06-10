# PyTune Box Packaging Guide

## Purpose

This guide explains how to package **PyTune Box** into a standalone Windows executable using **PyInstaller**. The result is a portable folder you can share without requiring users to install Python.

## Requirements

- Windows 10 or 11
- Python 3.10 or newer installed
- Project dependencies installed
- PyInstaller installed through `requirements.txt`

## Step 1: Open Terminal

Open **PowerShell** or **Command Prompt** inside the project root folder.

Example:

```bat
cd "E:\Github_luv219\GUI Music Player"
```

## Step 2: Install Dependencies

```bat
pip install -r requirements.txt
```

If pip has SSL issues on your machine, you may need:

```bat
pip install -r requirements.txt --trusted-host pypi.org --trusted-host files.pythonhosted.org
```

## Step 3: Test Source App

```bat
python main.py
```

**Expected:** PyTune Box opens normally.

## Step 4: Build EXE

```bat
build_scripts\build_windows_exe.bat
```

**Expected output:**

```text
dist\PyTuneBox\PyTuneBox.exe
```

The build script:

- Cleans old `build/` and `dist/` folders
- Uses folder-based PyInstaller output (recommended for pygame)
- Bundles `data/` and `assets/`
- Uses `assets/icons/app.ico` automatically when that file exists

## Step 5: Run EXE

```bat
dist\PyTuneBox\PyTuneBox.exe
```

**Expected:** The desktop app opens without running `python main.py`.

## Step 6: Create Release ZIP

```bat
build_scripts\build_release_zip.bat
```

**Expected output:**

```text
releases\PyTuneBox-v0.1.0-beta.zip
```

This ZIP includes:

- The packaged `PyTuneBox` application folder contents
- `README.md`
- `RELEASE_NOTES.md`
- `PACKAGING_GUIDE.md`
- `VERSION.txt`
- `TESTING_CHECKLIST.md`

## Step 7: Clean Build Files

```bat
build_scripts\clean_build.bat
```

This removes `build/`, `dist/`, `PyTuneBox.spec`, and safe `__pycache__` folders. It does **not** delete `data/settings.json` or saved playlists.

## Notes

- Folder-based build is preferred for pygame reliability.
- One-file mode can be added later if needed.
- If antivirus gives a warning, test on your own machine first and avoid unknown sources.
- Code signing is recommended for serious public distribution.
- Test the packaged app on another Windows machine before sharing widely.

## Packaging Note for YouTube Streaming
- `python-vlc` uses the VLC Media Player runtime installed on the user's host operating system.
- The packaged `PyTuneBox.exe` does **not** bundle the VLC runtime. Users running the executable must have VLC Media Player (64-bit) installed separately on their Windows machine to use YouTube streaming.
- If VLC is missing, the packaged app will still start and local file playback (using pygame) will work perfectly. YouTube streaming will show a clear warning message requesting VLC installation.
- Do not attempt to bundle VLC runtime inside PyInstaller in this phase.

## Troubleshooting

### 1. PyInstaller not found

**Solution:**

```bat
pip install pyinstaller
```

Or reinstall all requirements:

```bat
pip install -r requirements.txt
```

### 2. pygame error after packaging

**Solution:** Use the provided folder-based build, not one-file mode.

### 3. App opens but cannot find `data/settings.json`

**Solution:** Confirm `--add-data "data;data"` is present in `build_scripts/build_windows_exe.bat`.

### 4. App icon missing

**Solution:** Add `assets/icons/app.ico` and rebuild.

### 5. EXE does not start

**Solution:** Run from Command Prompt to check for errors:

```bat
dist\PyTuneBox\PyTuneBox.exe
```

### 6. Build fails with permission denied or missing EXE during windowed build

**Solution:**

- Close any running `PyTuneBox.exe` before rebuilding.
- Temporarily allow the project folder in Windows Security / antivirus.
- The build script uses `--noupx` and a temp work folder for better reliability.
- If Defender blocks the windowed bootloader, rebuild after adding a PyInstaller exclusion.

## Before Publishing Release
Checklist:
- Run pytest.
- Run python main.py.
- Build EXE.
- Test EXE.
- Create release ZIP.
- Add screenshots.
- Add demo GIF/video if available.
- Check README links.
- Confirm no private file paths are visible.
- Confirm no personal audio files are included.

