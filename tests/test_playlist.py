"""

Tests for the playlist module.

"""



import json



from app.playlist import PlaylistManager





def test_new_playlist_count_is_zero():

    """A new playlist should start empty."""

    manager = PlaylistManager()

    assert manager.count() == 0





def test_add_fake_mp3_returns_true(tmp_path):

    """Adding a fake .mp3 file that exists should succeed with fallback metadata."""

    manager = PlaylistManager()

    fake_file = tmp_path / "song_one.mp3"

    fake_file.write_text("fake audio", encoding="utf-8")



    added = manager.add_song(fake_file)



    assert added is True

    assert manager.count() == 1

    assert manager.get_song(0)["title"] == "song_one"





def test_add_duplicate_returns_false(tmp_path):

    """Adding the same file twice should return False the second time."""

    manager = PlaylistManager()

    fake_file = tmp_path / "song_one.mp3"

    fake_file.write_text("fake audio", encoding="utf-8")



    assert manager.add_song(fake_file) is True

    assert manager.add_song(fake_file) is False

    assert manager.count() == 1





def test_remove_song_reduces_count(tmp_path):

    """Removing a song should reduce the playlist count."""

    manager = PlaylistManager()

    fake_file = tmp_path / "song_one.mp3"

    fake_file.write_text("fake audio", encoding="utf-8")

    manager.add_song(fake_file)



    removed = manager.remove_song(0)



    assert removed["filename"] == "song_one.mp3"

    assert manager.count() == 0





def test_clear_playlist_sets_count_to_zero(tmp_path):

    """Clearing the playlist should remove all songs."""

    manager = PlaylistManager()

    fake_file = tmp_path / "song_one.mp3"

    fake_file.write_text("fake audio", encoding="utf-8")

    manager.add_song(fake_file)



    manager.clear_playlist()



    assert manager.count() == 0





def test_unsupported_extension_returns_false(tmp_path):

    """Unsupported file extensions should not be added."""

    manager = PlaylistManager()

    fake_file = tmp_path / "notes.txt"

    fake_file.write_text("not audio", encoding="utf-8")



    assert manager.add_song(fake_file) is False

    assert manager.count() == 0





def test_save_empty_playlist_creates_json(tmp_path):

    """Saving an empty playlist should create a JSON file."""

    manager = PlaylistManager()

    save_path = tmp_path / "empty_playlist.json"



    manager.save_to_json(save_path, playlist_name="Empty Test")



    assert save_path.is_file()



    with open(save_path, "r", encoding="utf-8") as file:

        data = json.load(file)



    assert data["playlist_name"] == "Empty Test"

    assert data["song_count"] == 0

    assert data["songs"] == []





def test_load_invalid_json_raises_value_error(tmp_path):

    """Loading invalid JSON should raise ValueError."""

    manager = PlaylistManager()

    playlist_file = tmp_path / "broken.json"

    playlist_file.write_text("{not valid json", encoding="utf-8")



    try:

        manager.load_from_json(playlist_file)

        assert False, "Expected ValueError"

    except ValueError:

        pass





def test_load_playlist_skips_missing_files(tmp_path):

    """Loading a playlist should skip missing files safely."""

    manager = PlaylistManager()

    playlist_file = tmp_path / "playlist.json"

    playlist_data = {

        "playlist_name": "Test Playlist",

        "songs": [

            {"path": str(tmp_path / "missing.mp3")},

        ],

    }



    with open(playlist_file, "w", encoding="utf-8") as file:

        json.dump(playlist_data, file, indent=4)



    result = manager.load_from_json(playlist_file)



    assert result["loaded"] == 0

    assert result["skipped"] == 1

    assert len(result["missing_files"]) == 1

    assert manager.count() == 0





def test_invalid_playlist_index_raises_clear_error(tmp_path):

    """Invalid playlist indexes should raise a clear IndexError."""

    manager = PlaylistManager()



    try:

        manager.get_song(0)

        assert False, "Expected IndexError"

    except IndexError as exc:

        assert str(exc) == "Invalid playlist index."


