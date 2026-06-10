# Security Policy

## Supported Version
0.1.0-beta

## Reporting Security Issues
Do not publicly disclose serious vulnerabilities before maintainers review. Please reach out to the project maintainers directly first to allow time for patching the issue.

## Security Considerations
- App opens local audio files selected by the user.
- App stores playlists as JSON containing local file paths.
- App stores settings in `data/settings.json`.
- Do not share playlist JSON publicly if it contains private file paths.
- Download EXE only from trusted release source.
- Unsigned executables may trigger antivirus warnings.

## Privacy Notes
- No cloud sync.
- No account login.
- No tracking.
- No telemetry.
- No internet connection required by default.
