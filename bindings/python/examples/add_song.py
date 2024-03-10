#!/usr/bin/env python3

##  Copyright (C) 2006 Nick Piper <nick-gtkpod at nickpiper co uk>
##  Part of the gtkpod project.
 
##  URL: http://www.gtkpod.org/
##  URL: http://gtkpod.sourceforge.net/

##  The code contained in this file is free software; you can redistribute
##  it and/or modify it under the terms of the GNU Lesser General Public
##  License as published by the Free Software Foundation; either version
##  2.1 of the License, or (at your option) any later version.

##  This file is distributed in the hope that it will be useful,
##  but WITHOUT ANY WARRANTY; without even the implied warranty of
##  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
##  Lesser General Public License for more details.

##  You should have received a copy of the GNU Lesser General Public
##  License along with this code; if not, write to the Free Software
##  Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

# this file is just a little example to see how you could add music

import os
import sys
import urllib.request
import tempfile
import shutil
from optparse import OptionParser
from urllib.parse import urlparse
import gi
import gpod
#gi.require_version('Gpod', '1.0')
#from gi.repository import Gpod

def download(path):
    print("Downloading %s" % path)
    with urllib.request.urlopen(path) as remotefile:
        size = remotefile.length
        hndl, tempfilename = tempfile.mkstemp('.mp3')
        with open(tempfilename, "wb") as temp:
            fetched = 0
            while True:
                buf = remotefile.read(1024*20)
                if not buf:
                    break
                temp.write(buf)
                fetched += len(buf)
                if size:
                    sys.stdout.write("%.02f%% of %s Bytes\r" % (100*fetched / float(size), size))
                else:
                    sys.stdout.write(" Fetched %d bytes\r" % fetched)
                sys.stdout.flush()
        return tempfilename

parser = OptionParser()
parser.add_option("-m", "--mountpoint", dest="mountpoint",
                  default="/mnt/ipod",
                  help="use iPod at MOUNTPOINT", metavar="MOUNTPOINT")
parser.add_option("-l", "--playlist", dest="playlist",
                  help="add tracks to PLAYLIST", metavar="PLAYLIST")
parser.add_option("-p", "--podcast",
                  dest="ispodcast",
                  action="store_true",
                  default=False,
                  help="add to podcast playlist")
(options, args) = parser.parse_args()

if len(args) == 0:
    parser.error("Requires an mp3 to add.")

db = gpod.Database(options.mountpoint)

playlist = None
if options.playlist:
    for pl in db.Playlists:
        if pl.name == options.playlist:
            playlist = pl
    if not playlist:
        playlist = db.new_Playlist(title=options.playlist)
        print("Created new playlist %s" % playlist)

deleteWhenDone = []

for path in args:
    transport = urlparse(path)[0]
    if transport:
        path = download(path)
        deleteWhenDone.append(path)

    try:
        track = db.new_Track(filename=path, podcast=options.ispodcast)
    except gpod.TrackException as e:
        print("Exception handling %s: %s" % (path, e))
        continue  # skip this track

    print("Added %s to database" % track)

    if playlist:
        print(" adding to playlist %s" % playlist)
        playlist.add(track)

def print_progress(database, track, i, total):
    sys.stdout.write("Copying to iPod %04d/%d: %s\r" % (i,total,track))
    sys.stdout.flush()

print("Copying to iPod")
db.copy_delayed_files(callback=print_progress)

[os.unlink(f) for f in deleteWhenDone]

print("Saving database")
db.close()
print("Saved db")


