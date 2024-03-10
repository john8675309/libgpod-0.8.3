#!/usr/bin/env python3

##  Copyright (C) 2007 Nick Piper <nick-gtkpod at nickpiper co uk>
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

# this file is just a little example to see how you could read photos

import gi
gi.require_version('GdkPixbuf', '2.0')
gi.require_version('Gio', '2.0')
from gi.repository import GdkPixbuf, Gio

def save_pixbuf(pixbuf, filepath):
    # Create a Gio.File object from the filepath
    gfile = Gio.File.new_for_path(filepath)
    # Replace the existing file, create a new file if it doesn't exist, and open it for writing
    stream = gfile.replace(None, False, Gio.FileCreateFlags.NONE, None)
    # Save the pixbuf to the file stream
    pixbuf.save_to_streamv(stream, 'png', [], [], None)
    # Make sure to close the stream when done
    stream.close(None)

# Your existing code to obtain the pixbuf
import gpod

if not hasattr(gpod.Photo, 'get_pixbuf'):
    print('Sorry, gpod was built without pixbuf support.')
    raise SystemExit

photodb = gpod.PhotoDatabase("/media/john/iPod")

print(photodb)
for album in photodb.PhotoAlbums:
    print(" ", album)
    for photo in album:
        print("  ", photo)
        for w, h, s in ((0, 0, 'small'), (-1, -1, 'large')):
            pixbuf = photo.get_pixbuf(w, h)
            # Construct the filepath
            filepath = f"/tmp/{photo['id']}-{s}.png"
            # Save the pixbuf using the new method
            save_pixbuf(pixbuf, filepath)

photodb.close()
