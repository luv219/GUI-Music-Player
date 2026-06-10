"""
PyTune Box - YouTube Service Tests
"""

import pytest
from app.youtube_service import YouTubeService

@pytest.fixture
def service():
    return YouTubeService()

def test_is_probable_url(service):
    assert service.is_probable_url("https://youtube.com/watch?v=test") is True
    assert service.is_probable_url("http://google.com") is True
    assert service.is_probable_url("www.youtube.com") is True
    assert service.is_probable_url("song name") is False
    assert service.is_probable_url("") is False
    assert service.is_probable_url(None) is False

def test_normalize_query(service):
    assert service.normalize_query("  hello song  ") == "hello song"
    with pytest.raises(ValueError):
        service.normalize_query("")
    with pytest.raises(ValueError):
        service.normalize_query("   ")
    with pytest.raises(ValueError):
        service.normalize_query(None)

def test_format_duration(service):
    assert service.format_duration(245) == "04:05"
    assert service.format_duration("245") == "04:05"
    assert service.format_duration(None) == "00:00"
    assert service.format_duration(0) == "00:00"
    assert service.format_duration(-5) == "00:00"
    assert service.format_duration("invalid") == "00:00"

def test_sanitize_text(service):
    assert service.sanitize_text(" hello ", "Fallback") == "hello"
    assert service.sanitize_text("", "Fallback") == "Fallback"
    assert service.sanitize_text(None, "Fallback") == "Fallback"

def test_choose_best_audio_url_direct_url(service):
    info = {"url": "https://stream.direct.url"}
    assert service.choose_best_audio_url(info) == "https://stream.direct.url"

def test_choose_best_audio_url_formats(service):
    # Select audio-only formats, preferring highest abr
    info = {
        "formats": [
            {"url": "https://stream.video", "vcodec": "h264", "acodec": "aac", "abr": 128},
            {"url": "https://stream.audio.low", "vcodec": "none", "acodec": "aac", "abr": 64},
            {"url": "https://stream.audio.high", "vcodec": "none", "acodec": "aac", "abr": 192},
        ]
    }
    assert service.choose_best_audio_url(info) == "https://stream.audio.high"

def test_choose_best_audio_url_no_playable(service):
    info = {"formats": []}
    assert service.choose_best_audio_url(info) is None
    
    info_no_url = {
        "formats": [
            {"vcodec": "none", "acodec": "aac"}
        ]
    }
    assert service.choose_best_audio_url(info_no_url) is None
