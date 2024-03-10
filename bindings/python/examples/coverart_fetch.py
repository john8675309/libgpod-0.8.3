#!/usr/bin/env python3

##  Copyright (C) 2005 Nick Piper <nick-gtkpod at nickpiper co uk>
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

##  $Id$

import os
import sys
import urllib.request
from optparse import OptionParser

# Assuming `gpod` and a Python 3 compatible `amazon` module are available
import gpod
# Update amazon module import according to its Python 3 version
import amazon

# For GTK, PyGObject is the successor to PyGTK for Python 3
from gi.repository import GdkPixbuf, GLib

parser = OptionParser()
parser.add_option("-m", "--mountpoint", dest="mountpoint",
                  default="/mnt/ipod",
                  help="use iPod at MOUNTPOINT", metavar="MOUNTPOINT")
(options, args) = parser.parse_args()

db = gpod.Database(options.mountpoint)

# Set your key here, or see amazon.py for a list of other places to store it.
amazon.setLicense('')

images = {}

for track in db:
    if track.get_coverart().thumbnails:
        # Skipping tracks that already have artwork
        continue

    print("%(artist)s, %(album)s, %(title)s" % track)

    if not (track['artist'] and track['album']):
        print(" Need an artist AND album name, skipping.")       
        continue
    
    if (track['album'], track['artist']) not in images:
        query = "%(album)s + %(artist)s" % track
        for term in ["Disk 1", "Disk 2", '12"', '12 "','"','&']:
            query = query.replace(term,"")
        print(" Searching for %s: " % query)
        try:
            # Update the amazon search function call as needed for the Python 3 version of the API client
            albums = amazon.searchByKeyword(query, type="lite", product_line="music")
        except amazon.AmazonError as e:
            print(e)
            albums = []
                
        if not albums:
            continue
        album = albums[0]

        try:
            image_data = urllib.request.urlopen(album.ImageUrlLarge).read()
        except Exception as e:
            print(" Failed to download from %s" % album.ImageUrlLarge)
            continue
        
        loader = GdkPixbuf.PixbufLoader()
        loader.write(image_data)
        loader.close()
        pixbuf = loader.get_pixbuf()
        if pixbuf.get_width() > 10 or pixbuf.get_height() > 10:
            print(" Fetched image")
            images[(track['album'], track['artist'])] = pixbuf

    try:
        track.set_coverart(images[(track['album'], track['artist'])].save_to_buffer("png"))
        print(" Added thumbnails")
    except KeyError:
        print(" No image available")

print("Saving database")
db.close()
print("Saved db")
