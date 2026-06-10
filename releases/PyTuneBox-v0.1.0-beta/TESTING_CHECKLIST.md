# PyTune Box Manual Testing Checklist

Use this checklist before release or packaging.

## 1. Startup Tests

- [ ] App starts with `python main.py`
- [ ] Window opens correctly
- [ ] Theme loads correctly
- [ ] Volume loads correctly
- [ ] Status bar shows Phase 10 ready message or audio warning if needed

## 2. File Import Tests

- [ ] Open files
- [ ] Open folder
- [ ] Open folder with subfolders
- [ ] Unsupported files are skipped
- [ ] Duplicate files are skipped
- [ ] Cancelled file dialog does not break the app
- [ ] Cancelled folder dialog does not break the app

## 3. Playback Tests

- [ ] Play
- [ ] Pause
- [ ] Resume
- [ ] Stop
- [ ] Next
- [ ] Previous
- [ ] Volume
- [ ] Seek
- [ ] Auto-next

## 4. Playlist Tests

- [ ] Remove selected
- [ ] Clear playlist
- [ ] Save playlist
- [ ] Load playlist
- [ ] Load playlist with missing files
- [ ] Load invalid JSON
- [ ] Invalid playlist does not destroy current playlist before confirmation

## 5. Metadata Tests

- [ ] Title shown
- [ ] Artist shown
- [ ] Album shown
- [ ] Duration shown
- [ ] Missing metadata fallback works

## 6. Theme Tests

- [ ] Toggle theme
- [ ] Restart app and verify saved theme
- [ ] Visualizer colors update

## 7. Shortcut Tests

- [ ] Space
- [ ] S
- [ ] Left Arrow
- [ ] Right Arrow
- [ ] H
- [ ] R
- [ ] Ctrl+O
- [ ] Ctrl+Shift+O
- [ ] Ctrl+S
- [ ] Ctrl+L

## 8. Visualizer Tests

- [ ] Animates during play
- [ ] Pauses during pause
- [ ] Stops during stop
- [ ] Stops on clear playlist
- [ ] Stops on exit

## 9. Exit Tests

- [ ] Close while stopped
- [ ] Close while playing
- [ ] Close while paused

## 10. Regression Checklist

- [ ] No traceback in terminal during normal use
- [ ] No GUI freeze
- [ ] No broken buttons
- [ ] No unreadable text in dark mode
- [ ] Missing audio file shows error instead of crashing
- [ ] Corrupted or unsupported playback shows error instead of crashing
