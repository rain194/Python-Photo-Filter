"""
Main entry point for the Python Image Editor application.
"""

from gui import ImageEditorApp

def main() -> None:
    """
    Main function to run the image editor application.
    """
    app = ImageEditorApp()
    app.mainloop()

if __name__ == "__main__":
    main()
