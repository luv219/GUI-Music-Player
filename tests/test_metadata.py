"""

Tests for the metadata module.

"""



from pathlib import Path



from app.metadata import MetadataReader





def test_format_duration_zero():

    """format_duration(0) should return 00:00."""

    reader = MetadataReader()

    assert reader.format_duration(0) == "00:00"





def test_format_duration_sixty_five():

    """format_duration(65) should return 01:05."""

    reader = MetadataReader()

    assert reader.format_duration(65) == "01:05"





def test_format_duration_two_forty_five():

    """format_duration(245) should return 04:05."""

    reader = MetadataReader()

    assert reader.format_duration(245) == "04:05"





def test_format_duration_none():

    """format_duration(None) should return 00:00."""

    reader = MetadataReader()

    assert reader.format_duration(None) == "00:00"





def test_format_duration_negative():

    """format_duration(-5) should return 00:00."""

    reader = MetadataReader()

    assert reader.format_duration(-5) == "00:00"





def test_safe_filename_title_from_path():

    """safe_filename_title should return the filename without extension."""

    reader = MetadataReader()

    assert reader.safe_filename_title("music/song_one.mp3") == "song_one"





def test_safe_filename_title_fallback():

    """safe_filename_title should return Unknown Title for invalid input."""

    reader = MetadataReader()

    assert reader.safe_filename_title("") == "Unknown Title"





def test_read_metadata_missing_file_raises(tmp_path):

    """read_metadata should raise FileNotFoundError for missing files."""

    reader = MetadataReader()

    missing_file = tmp_path / "missing.mp3"



    try:

        reader.read_metadata(missing_file)

        assert False, "Expected FileNotFoundError"

    except FileNotFoundError:

        pass





def test_read_metadata_fake_file_uses_fallback(tmp_path):

    """read_metadata should return fallback metadata for fake audio files."""

    reader = MetadataReader()

    fake_file = tmp_path / "demo_track.mp3"

    fake_file.write_text("not real audio", encoding="utf-8")



    metadata = reader.read_metadata(fake_file)



    assert metadata["title"] == "demo_track"

    assert metadata["artist"] == "Unknown Artist"

    assert metadata["album"] == "Unknown Album"

    assert metadata["duration_seconds"] == 0

    assert metadata["duration_text"] == "00:00"

    assert metadata["filename"] == "demo_track.mp3"

    assert Path(metadata["path"]) == fake_file.resolve()


