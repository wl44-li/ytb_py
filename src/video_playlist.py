"""A video playlist class."""


class Playlist:
    """A class used to represent a Playlist."""

    def __init__ (self, name: str):
        self._name = name
        self._listed_vids = []


    @property
    def name(self) -> str:
        """Returns the name of a playlist."""
        return self._name
