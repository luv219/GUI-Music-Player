"""
PyTune Box - Application Entry Point

This is the main entry point for the PyTune Box desktop music player.
Run this file to start the application.
"""

from app.gui import PyTuneBoxApp


def main():
    """Create and run the PyTune Box application."""
    app = PyTuneBoxApp()
    app.run()


if __name__ == "__main__":
    main()
