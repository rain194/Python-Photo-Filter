"""
Manages the history of image states.
"""

from PIL import Image
from typing import List

class History:
    """
    Class to manage the history of image edits.
    """
    def __init__(self) -> None:
        self.history: List[Image.Image] = []
        self.index: int = -1

    def add_state(self, img: Image.Image) -> None:
        """
        Add a new image state to the history.

        Args:
            img (Image.Image): Image to add.
        """
        # Truncate any forward history
        self.history = self.history[:self.index + 1]
        self.history.append(img)
        self.index += 1

    def undo(self) -> Image.Image:
        """
        Undo the last action.

        Returns:
            Image.Image: The previous image state.
        """
        if self.can_undo():
            self.index -= 1
            return self.history[self.index]
        else:
            return self.history[self.index]

    def redo(self) -> Image.Image:
        """
        Redo the next action.

        Returns:
            Image.Image: The next image state.
        """
        if self.can_redo():
            self.index += 1
        return self.history[self.index]

    def can_undo(self) -> bool:
        """
        Check if undo is possible.

        Returns:
            bool: True if undo is possible, False otherwise.
        """
        return self.index > 0

    def can_redo(self) -> bool:
        """
        Check if redo is possible.

        Returns:
            bool: True if redo is possible, False otherwise.
        """
        return self.index < len(self.history) - 1

    def clear(self) -> None:
        """
        Clear the history.
        """
        self.history.clear()
        self.index = -1
