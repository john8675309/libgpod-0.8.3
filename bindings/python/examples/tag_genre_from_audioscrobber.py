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
import gpod
import urllib.request
import urllib.parse
import xml.etree.ElementTree as ET

TRUST_LIMIT = 10
dbname = os.path.join(os.environ['HOME'], ".gtkpod/local_0.itdb")

itdb = gpod.itdb_parse_file(dbname, None)
if not itdb:
    print("Failed to read %s" % dbname)
    sys.exit(2)
    
cache = {}
for track in gpod.sw_get_tracks(itdb):
    if track.artist is None:
        continue

    key = track.artist.upper()
    if key not in cache:
        url = "http://ws.audioscrobbler.com/1.0/artist/%s/toptags.xml" % urllib.parse.quote(track.artist)
        
        try:
            with urllib.request.urlopen(url) as response:
                reply = response.read()
            xmlreply = ET.fromstring(reply)
            tags = xmlreply.findall('.//tag')
            if tags:
                top_tag = tags[0]
                tag_name = top_tag.find('name').text
                tag_count = int(top_tag.find('count').text)
                if tag_name and tag_count > TRUST_LIMIT:
                    cache[key] = tag_name.title()  # No unicode conversion needed in Python 3
        except urllib.error.HTTPError as e:
            pass  # Optionally print an error message
        except ET.ParseError as e:
            print("Failed to parse,", e)
            print(reply)

    if key in cache:
        track.genre = cache[key]
        print("%-25s %-20s %-20s --> %s" % (track.title, track.album, track.artist, track.genre))
    else:
        print("%-25s %-20s %-20s === %s" % (track.title, track.album, track.artist, "Unknown"))

gpod.itdb_write_file(itdb, dbname, None)
