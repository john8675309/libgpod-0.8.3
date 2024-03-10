#!/usr/bin/env python3
import gpod

# Replace '/mnt/ipod' with the actual mount point of your iPod
ipod_mount = '/media/john/iPod'

# Initialize the iPod database
itdb = gpod.Database(ipod_mount)

if itdb:
    print("Playlists on the iPod:")
    for playlist in itdb.Playlists:
        print(f"- {playlist.name}")
        for track in playlist:
            # Access attributes using item access syntax
            title = track['title'] if 'title' in track else 'Unknown Title'
            artist = track['artist'] if 'artist' in track else 'Unknown Artist'
            print(f"{title} by {artist}")

    print("\nTracks on the iPod:")
    for track in itdb:
        # Access attributes using item access syntax
        title = track['title'] if 'title' in track else 'Unknown Title'
        artist = track['artist'] if 'artist' in track else 'Unknown Artist'
        print(f"{title} by {artist}")

    itdb.close()
else:
    print("Failed to read the iPod database.")
