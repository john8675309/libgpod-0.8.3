"""Manage tracks and playlists on an iPod.

The gpod module allows you to add and remove tracks, create and edit
playlists, and other iPod tasks.

"""
from .gpod import _Itdb_Track, _Itdb_Playlist, _Itdb_Artwork
from .gpod import *
from .ipod import *

__all__ = ["DatabaseException", "TrackException",
           "Database","Track","Playlist"]
