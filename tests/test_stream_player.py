"""
PyTune Box - Stream Player Tests
"""

import pytest
from app.stream_player import StreamPlayer

@pytest.fixture
def player():
    return StreamPlayer(volume=70)

def test_instantiation(player):
    # Should instantiate without crashing regardless of VLC presence
    assert player is not None
    assert hasattr(player, "is_available")

def test_set_volume(player):
    # Clamping test
    assert player.set_volume(50) == 50
    assert player.set_volume(150) == 100
    assert player.set_volume(-10) == 0
    assert player.get_volume() in (50, 100, 0) # last volume applied was 0

def test_get_volume(player):
    assert player.get_volume() == player.volume

def test_get_elapsed_seconds(player):
    # Not playing, should return 0
    assert player.get_elapsed_seconds() == 0

def test_stop_no_crash(player):
    try:
        player.stop()
        success = True
    except Exception:
        success = False
    assert success is True

def test_quit_no_crash(player):
    try:
        player.quit()
        success = True
    except Exception:
        success = False
    assert success is True
