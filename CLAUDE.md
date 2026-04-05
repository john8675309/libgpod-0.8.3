# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Overview

libgpod is a C library for reading and writing Apple iPod content databases (iTunesDB, iTunesCDB, SQLite). It supports iPod Classic, Nano, Shuffle, Mini, Touch, and iPhone. This fork adds Python 3 support.

## Build Commands

```bash
# Standard build
./configure
make

# Build with Python bindings and docs
./configure --enable-python --enable-gtk-doc
make

# Run C tests
make check

# Run Python tests
cd bindings/python && make test

# Install
make install
```

Key optional `./configure` flags:
- `--enable-python` — Python 3 bindings via SWIG
- `--with-gdk-pixbuf` — Artwork/thumbnail support
- `--with-libimobiledevice` — iPhone/iPod Touch support
- `--without-hal` — Disable deprecated HAL backend

## Architecture

### Core Data Model (`src/itdb.h`)

The central header defines all public structures:

- **`Itdb_iTunesDB`** — Root database object; owns lists of `Itdb_Track` and `Itdb_Playlist`
- **`Itdb_Track`** — All metadata for a single song/video/podcast
- **`Itdb_Playlist`** — Ordered list of track references; first playlist is always the Master Playlist
- **`Itdb_PhotoDB`** — Separate photo database with `Itdb_Artwork` items
- **`Itdb_Device`** — Device capabilities, model info, filesystem mount point

### Database Format Handling

The library supports multiple on-disk formats depending on iPod generation:

| Format | Files | Used by |
|--------|-------|---------|
| Binary iTunesDB | `iPod_Control/iTunes/iTunesDB` | Classic, Nano 1–4G |
| Compressed iTunesCDB | same path | Nano 5G, iPhone/Touch |
| SQLite | `iTunes/iTunes Library.itlp/` | iPhone OS 3.x+, Nano 5G |

Key source files by concern:
- `src/itdb_itunesdb.c` — Binary iTunesDB parser/writer (~8500 lines; the heart of the library)
- `src/itdb_sqlite.c` — SQLite database support for newer devices
- `src/itdb_device.c` — Device detection, model identification, SysInfo parsing
- `src/itdb_artwork.c`, `src/db-artwork-parser.c`, `src/db-artwork-writer.c` — Artwork/thumbnail pipeline
- `src/itdb_hash58.c`, `src/itdb_hash72.c`, `src/itdb_hashAB.c` — Integrity hash algorithms per device generation
- `src/rijndael.c` — AES used for protected content

### Python Bindings (`bindings/python/`)

Two layers:

1. **SWIG-generated low-level bindings** (`gpod.i` → `_gpod.so`) — Direct C API access with `gpod.itdb_*` functions and `gpod.sw_*` helper wrappers
2. **Pythonic high-level API** (`ipod.py`) — Object-oriented `Database`, `Track`, `Playlist`, `PhotoDatabase` classes built on top of SWIG bindings

Typical usage pattern:
```python
import gpod
db = gpod.Database('/mnt/ipod')
for track in db:
    print(track['title'])
db.close()
```

The `bindings/python/examples/` directory has 10 working example scripts covering common operations (add song, add photo, list tracks, copy tracks, etc.).

### Tools (`tools/`)

Standalone programs for device management separate from the library:
- `generic-callout.c` — iPod detect/init helper called by udev
- `udev-backend.c` / `hal-backend.c` — System integration backends
- `ipod-usb.c`, `ipod-scsi.c`, `ipod-lockdown.c` — Low-level device communication

## Key Documentation Files

- `README.overview` — Device architecture, hash scheme matrix (hash58/hash72/hashAB by model), feature support table
- `README.sqlite` — SQLite database structure for Nano 5G / iPhone OS 3+
- `README.SysInfo` — SysInfoExtended XML parsing and device identification
