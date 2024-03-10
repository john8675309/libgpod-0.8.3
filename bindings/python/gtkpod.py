import os
import struct
import hashlib

class ParseError(Exception):
    """Exception for parse errors."""
    pass

class SyncError(Exception):
    """Exception for sync errors."""
    pass

def sha1_hash(filename):
    """Return an SHA1 hash on the first 16k of a file."""
    hash_len = 4 * 4096
    hash = hashlib.sha1()
    size = os.path.getsize(filename)
    with open(filename, "rb") as f:
        hash.update(struct.pack("<L", size))
        hash.update(f.read(hash_len))
    return hash.hexdigest()

def write_pair(file, name, value):
    if not isinstance(value, str):
        value = str(value)
    file.write("=".join([name, value]) + '\n')

def write(filename, db, itunesdb_file):
    """Save extended info to a file."""
    with open(filename, "w") as file:
        write_pair(file, "itunesdb_hash", sha1_hash(itunesdb_file))
        write_pair(file, "version", "0.99.9")
        for track in db:
            write_pair(file, "id", track['id'])
            if not track['userdata']:
                track['userdata'] = {}
            for k, v in track['userdata'].items():
                write_pair(file, k, v)
        write_pair(file, "id", "xxx")

def parse(filename, db, itunesdb_file=None):
    """Load extended info from a file."""
    ext_hash_valid = False
    ext_data = {}

    with open(filename, "r") as file:
        for line in file:
            parts = line.strip().split("=", 1)
            if len(parts) != 2:
                print(parts)
            name, value = parts
            if name == "id":
                if value == 'xxx':
                    break
                id = int(value)
                ext_data[id] = {}
            elif name == "version":
                pass
            elif name == "itunesdb_hash":
                if itunesdb_file and sha1_hash(itunesdb_file) == value:
                    ext_hash_valid = True
            else:
                ext_data[id][name] = value

    if ext_hash_valid:
        for track in db:
            try:
                track['userdata'] = ext_data[track['id']]
            except KeyError:
                track['userdata'] = {}
    else:
        tracks_by_sha = {}
        for track in db:
            tracks_by_sha[sha1_hash(track.ipod_filename())] = track
        for ext_block in ext_data.values():
            try:
                if 'sha1_hash' in ext_block:
                    track = tracks_by_sha[ext_block['sha1_hash']]
                elif 'md5_hash' in ext_block:
                    track = tracks_by_sha[ext_block['md5_hash']]
            except KeyError:
                print("Failed to match hash from extended information file with one that we just calculated:")
                print(ext_block)
                continue
            track['userdata'] = ext_block
