"""
PyTune Box - MusicBrainz Service Tests
"""

import pytest
from app.musicbrainz_service import MusicBrainzService

@pytest.fixture
def service():
    return MusicBrainzService()

def test_milliseconds_to_seconds(service):
    assert service.milliseconds_to_seconds(245000) == 245
    assert service.milliseconds_to_seconds(None) == 0
    assert service.milliseconds_to_seconds("245000") == 245
    assert service.milliseconds_to_seconds("invalid") == 0

def test_format_duration(service):
    assert service.format_duration(245) == "04:05"
    assert service.format_duration(None) == "00:00"
    assert service.format_duration(0) == "00:00"
    assert service.format_duration(61) == "01:01"

def test_is_unknown_value(service):
    assert service.is_unknown_value("Unknown Artist") is True
    assert service.is_unknown_value("Unknown Album") is True
    assert service.is_unknown_value("Unknown") is True
    assert service.is_unknown_value("") is True
    assert service.is_unknown_value(None) is True
    assert service.is_unknown_value("Real Artist") is False
    assert service.is_unknown_value("Some Album") is False

def test_create_search_terms_from_song(service):
    song1 = {
        "title": "Imagine",
        "artist": "John Lennon",
        "album": "Imagine Album"
    }
    terms1 = service.create_search_terms_from_song(song1)
    assert terms1["title"] == "Imagine"
    assert terms1["artist"] == "John Lennon"
    assert terms1["album"] == "Imagine Album"

    song2 = {
        "title": "Imagine",
        "artist": "Unknown Artist",
        "album": "Unknown Album"
    }
    terms2 = service.create_search_terms_from_song(song2)
    assert terms2["title"] == "Imagine"
    assert terms2["artist"] is None
    assert terms2["album"] is None

    song3 = {
        "filename": "track01.mp3",
    }
    terms3 = service.create_search_terms_from_song(song3)
    assert terms3["title"] == "track01"
    assert terms3["artist"] is None
    assert terms3["album"] is None

def test_normalize_recording_result(service):
    fake_result = {
        "id": "1234",
        "title": "Fake Title",
        "artist-credit": [
            {"name": "Fake Artist"}
        ],
        "release-list": [
            {"title": "Fake Album", "date": "2020-01-01", "country": "US"}
        ],
        "length": 245000,
        "ext:score": "100"
    }
    normalized = service.normalize_recording_result(fake_result)
    assert normalized["musicbrainz_recording_id"] == "1234"
    assert normalized["title"] == "Fake Title"
    assert normalized["artist"] == "Fake Artist"
    assert normalized["album"] == "Fake Album"
    assert normalized["duration_seconds"] == 245
    assert normalized["duration_text"] == "04:05"
    assert normalized["release_date"] == "2020-01-01"
    assert normalized["country"] == "US"
    assert normalized["score"] == "100"
    assert normalized["source"] == "MusicBrainz"

    empty_result = {}
    normalized_empty = service.normalize_recording_result(empty_result)
    assert normalized_empty["musicbrainz_recording_id"] == ""
    assert normalized_empty["title"] == ""
    assert normalized_empty["artist"] == "Unknown Artist"
    assert normalized_empty["album"] == "Unknown Album"
    assert normalized_empty["duration_seconds"] == 0
    assert normalized_empty["duration_text"] == "00:00"
    assert normalized_empty["release_date"] == ""
    assert normalized_empty["country"] == ""
    assert normalized_empty["score"] == ""
    assert normalized_empty["source"] == "MusicBrainz"
