#!/usr/bin/env python3
import gpod
# Replace '/mnt/ipod' with the actual mount point of your iPod
ipod_mount = '/media/john/iPod'
# Specify the title of the track you want to remove
track_to_remove_title = ''

# Initialize the iPod database
itdb = gpod.Database(ipod_mount)

if itdb:
    found = False
    for track in itdb:
        # Check if this is the track we want to remove
        if track['title'] == track_to_remove_title:
            print(f"Removing track: {track['title']} by {track['artist']}")
            itdb.remove(track, ipod=True, quiet=True)  # Remove the track from the database and the iPod
            found = True
            break  # Exit after removing the first matching track

    if found:
        print("Database updated. Track removed.")
    else:
        print("Track not found.")

    itdb.close()
else:
    print("Failed to read the iPod database.")
