#!/usr/bin/env python3
import gpod

def add_photo_to_ipod(device_mount_point, photo_path, album_name="My Photos"):
    # Connect to the iPod
    db = gpod.PhotoDatabase(device_mount_point)
    
    # Create a new photo album if it doesn't exist
    for album in db.PhotoAlbums:
        if album.name == album_name:
            break
    #else:
    #    album = db.add_PhotoAlbum(name=album_name)

    # Add the photo to the album
    photo = db.new_Photo(filename=photo_path)
    album.add(photo)

    # Write changes back to the iPod
    db.write()
    db.close()

# Example usage
device_mount_point = '/media/john/iPod'  # Adjust this path to where your iPod is mounted
photo_path = '/home/john/Desktop/itunes3.png'  # Adjust this to the path of your photo
add_photo_to_ipod(device_mount_point, photo_path)

