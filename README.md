This is a fork of the libgpod to focus on python3 bindings.
I just tested rudimentary things and so far so good.

---------------------------------------------------------------------

libgpod is a library meant to abstract access to an iPod content. It
provides an easy to use API to retrieve the list of files and playlist
stored on an iPod, to modify them and to save them back to the iPod.

This code was originally part of gtkpod (www.gtkpod.org). When the iPod
content parsing code was made to be self-contained with gtkpod 0.93,
we chose to put this code in a separate library so that other project
can benefit from it without duplicating code.

Currently (2010-03-23) libgpod supports writing to all "classic" iPod models,
all iPod Nanos, iPod Minis and iPhones and iPod Touch. iPod Nano 5th Gen. and
iPhone/iPod Touch support is "partial" in the sense that a database with at
least one song written by iTunes is needed the first time you use the iPod 
with libgpod. For these models, it's also highly recommended to get the
provided udev/hal callout to work for proper support. Older iPod Shuffle models
are supported, but the new button-less ones (3rd and 4th Gen.) are not. Please
get in touch if you want to hack on adding support for that.

For supported models, covert art and photos are supported in addition to
manipulating the music database.

If you decide to make improvements,  or have bug fixes to report or contribute,
just drop a mail to Gtkpod-devel@lists.sourceforge.net (due to too much spam,
the mailing list is unfortunately subscriber-only).

----------------------------------------------------------------------

Quick HOWTO use libgpod for audio

itdb_parse(): read the iTunesDB and ArtworkDB
itdb_write(): write the iTunesDB and ArtworkDB

itdb_parse() will return a Itdb_iTunesDB structure with GLists
containing all tracks (each track is represented by a Itdb_Track
structure) and the playlists (each playlist is represented by a
Itdb_Playlist structure).

A number of functions for adding, removing, duplicating tracks are
available. Please see itdb.h for details (itdb_track_*()).

In each Itdb_Playlist structure you can find a GList called 'members'
with listing all member tracks. Each track referenced in a playlist
must also be present in the tracks GList of the iTunesDB.

The iPod must contain one master playlist (MPL) containing all tracks
accessible on the iPod through the
Music->Tracks/Albums/Artists... menu. Besides the MPL there can be a
number of normal playlists accessible through the Music->Playlists
menu on the iPod. Tracks that are a member of one of these normal
playlists must also be a member of the MPL.

The Podcasts playlist is just another playlist with some internal
flags set differently. Also, member tracks in the Podcasts playlist
are not normally members of the MPL (so on the iPod they will only
show up under the Podcasts menu). All tracks referenced must be in the
tracklist of the Itdb_iTunesDB, however.

A number of functions to add/remove playlists, or add/remove tracks
are available. Please see itdb.h for details (itdb_playlist_*()).

Each track can have a thumbnail associated with it. You can retrieve a
GdkPixmap of the thumbnail using itdb_artwork_get_pixbuf().  You can
remove a thumbnail with itdb_track_remove_thumbnails(). And finally,
you can set a new thumbnail using itdb_track_set_thumbnails().

Please note that iTunes additionally stores the artwork as tags in the
original music file. That's also from where the data is read when
artwork is displayed in iTunes, and there can be more than one piece
of artwork. libgpod does not store the artwork as tags in the original
music file. As a consequence, if iTunes attempts to access the
artwork, it will find none, and remove libgpod's artwork. Luckily,
iTunes will only attempt to access the artwork if you select a track
in iTunes. (To work around this, gtkpod keeps a list of the original
filename of all artwork and silently adds the thumbnails if they were
'lost'. Your application might want to do something similar, or you
can supply patches for (optionally!) adding tags to the original music
files.)

The Itdb_iTunesDB, Itdb_Playlist and Itdb_Track structures each have a
userdata and a usertype field that can be used by the application to
store application-specific additional data. If userdata is a pointer
to an external structure, you can supply a ItdbUserDataDuplicateFunc
and a ItdbUserDataDestroyFunc so that this data can be duplicated
or freed automatically with a call to the library _duplicate()/_free()
functions.

For more information I would advice to have a look at gtkpod's source
code. You can also ask questions on the developer's mailing list:
gtkpod-devel at lists dot sourceforge dot net

Jörg Schuler (jcsjcs at users dot sourceforge dot net)

----------------------------------------------------------------------

Quick HOWTO use libgpod for photos

   itdb_photodb_parse():
       Read an existing PhotoDB.

   itdb_photodb_create():
       Create a new Itdb_PhotoDB structure. The Photo Library Album is
       (first album) is created automatically.

   itdb_photodb_add_photo(), itdb_photodb_add_photo_from_data():
       Add a photo to the PhotoDB (from file or from a chunk of
       memory). It is automatically added to the Photo Library Album
       (first album), which is created if it does not exist already.

   itdb_photodb_photoalbum_create():
       Create and add a new photoalbum.

   itdb_photodb_photoalbum_add_photo():
       Add a photo (Itdb_Artwork) to an existing photoalbum.

   itdb_photodb_photoalbum_remove():
       Remove an existing photoalbum. Pictures can be kept in the
       Photo Library or automatically removed as well.

   itdb_photodb_remove_photo():
       Remove a photo either from a photoalbum or completely from the database.

   itdb_photodb_write():
       Write out your PhotoDB.

   itdb_photodb_free():
       Free all memory taken by the PhotoDB.

   itdb_photodb_photoalbum_by_name():
       Find the first photoalbum with a given name or the Photo
       Library Album if called with no name.

If you cannot add photos because your iPod is not recognized, you may
have to set the iPod model by calling

itdb_device_set_sysinfo (db->device, "ModelNumStr", model);

For example, "MA450" would stand for an 80 GB 6th generation iPod
Video. See itdb_device.c for a list of supported models.

This information will be written to the iPod when the PhotoDB is saved
(itdb_device_write_sysinfo() is called).

Have a look at the following test-photos test program in the tests/
subdirectory for an example of how to use the interface.

Jörg Schuler (jcsjcs at users dot sourceforge dot net)

----------------------------------------------------------------------
