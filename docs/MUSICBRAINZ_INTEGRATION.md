# MusicBrainz Integration

## Overview
PyTune Box can search MusicBrainz for improved metadata. This allows users to look up and apply high-quality metadata for their local audio files directly from the MusicBrainz database.

## Library Used
The integration uses the `musicbrainzngs==0.7.1` Python library to interact with the MusicBrainz Web Service.

## API Used
MusicBrainz API / Web Service.

## User-Agent
MusicBrainz requires a meaningful User-Agent. PyTune Box sets a compliant User-Agent using the application name, version, and optional contact information before making any API calls.

## Rate Limiting
- PyTune Box uses a delay between requests to strictly respect MusicBrainz rate limits (1 request per second by default).
- Lookups are strictly user-triggered.
- The app does not bulk query automatically to prevent spamming the MusicBrainz API.

## What Data Is Fetched
The following data fields are fetched when available:
- Recording ID
- Title
- Artist
- Album/release
- Duration
- Release date
- Country
- Score

## What Data Is Stored
- Metadata is updated only inside the app's in-memory playlist.
- Original audio files on the disk are NOT modified.
- If the user saves the playlist to a JSON file, the MusicBrainz metadata is saved there and will be loaded back in the future.

## Offline Behavior
- The app continues to work perfectly using local mutagen metadata.
- MusicBrainz lookup requires an active internet connection.

## Limitations
- No AcoustID fingerprinting is available in this phase.
- Search is currently based on existing title/artist/album text or filename.
- Results may require manual user selection.
- Rate limits must be respected, which limits the speed of multiple manual queries.

## Future Improvements
- AcoustID fingerprint lookup
- Cover Art Archive integration
- Album art display
- Write tags to copied files with user confirmation
- Bulk lookup with queue and strict rate limiting
