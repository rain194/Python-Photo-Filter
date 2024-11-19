"""
Contains utility functions for image operations.
"""

from PIL import Image
from typing import Optional

class ImageUtils:
    """
    Utility class for image loading and saving.
    """

    @staticmethod
    def load_image(file_path: str) -> Optional[Image.Image]:
        """
        Load an image from a file.

        Args:
            file_path (str): Path to the image file.

        Returns:
            Optional[Image.Image]: Loaded image or None if failed.
        """
        try:
            img = Image.open(file_path)
            return img.convert("RGB")
        except Exception as e:
            print(f"Error loading image: {e}")
            return None

    @staticmethod
    def save_image(img: Image.Image, file_path: str) -> None:
        """
        Save an image to a file.

        Args:
            img (Image.Image): Image to save.
            file_path (str): Path to save the image.
        """
        try:
            img.save(file_path)
        except Exception as e:
            print(f"Error saving image: {e}")
