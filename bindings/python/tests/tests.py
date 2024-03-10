#!/usr/bin/env python3
import unittest
import shutil
import tempfile
import os
import datetime
import time

import gpod  # Assuming gpod is correctly installed and available in your Python 3 environment

class TestiPodFunctions(unittest.TestCase):
    def setUp(self):
        self.mp = tempfile.mkdtemp()
        control_dir = os.path.join(self.mp, 'iPod_Control')
        music_dir = os.path.join(control_dir, 'Music')
        shutil.copytree('resources', control_dir)
        os.mkdir(music_dir)
        for i in range(20):
            os.mkdir(os.path.join(music_dir, "f%02d" % i))
        self.db = gpod.Database(self.mp)

    def tearDown(self):
        shutil.rmtree(self.mp)

    def testClose(self):
        self.db.close()

    def testListPlaylists(self):
        list(self.db.Playlists)

    def testCreatePlaylist(self):
        self.assertEqual(len(self.db.Playlists), 2)
        pl = self.db.new_Playlist('my title')
        self.assertEqual(len(self.db.Playlists), 3)

    def testPopulatePlaylist(self):
        trackname = os.path.join(self.mp, 'iPod_Control', 'tiny.mp3')

        pl = self.db.new_Playlist('my title')
        self.assertEqual(len(pl), 0)
        t = self.db.new_Track(filename=trackname)
        pl.add(t)
        self.assertEqual(len(pl), 1)

    def testAddTrack(self):
        trackname = os.path.join(self.mp, 'iPod_Control', 'tiny.mp3')
        for n in range(1, 5):
            t = self.db.new_Track(filename=trackname)
            self.assertEqual(len(self.db), n)
        self.db.copy_delayed_files()
        for track in self.db:
            self.assertTrue(os.path.exists(track.ipod_filename()))

    def testAddRemoveTrack(self):
        self.testAddTrack()
        for n in range(4, 0, -1):
            track = self.db[0]
            track_file = track.ipod_filename()
            self.assertEqual(len(self.db), n)
            self.db.remove(track, ipod=True, quiet=True)
            self.assertFalse(os.path.exists(track_file))

    def testDatestampSetting(self):
        trackname = os.path.join(self.mp, 'iPod_Control', 'tiny.mp3')
        t = self.db.new_Track(filename=trackname)
        date = datetime.datetime.now()
        t['time_added'] = date
        self.assertEqual(date.year, t['time_added'].year)
        self.assertEqual(date.second, t['time_added'].second)
        
        date = datetime.datetime.now()
        t['time_added'] = time.mktime(date.timetuple())
        self.assertEqual(date.year, t['time_added'].year)
        self.assertEqual(date.second, t['time_added'].second)

    def testTrackContainerMethods(self):
        self.testAddTrack()
        track = self.db[0]
        self.assertIn('title', track)

    def testVersion(self):
        self.assertIsInstance(gpod.version_info, list)

class TestPhotoDatabase(unittest.TestCase):
    def setUp(self):
        # Set up code for TestPhotoDatabase
        self.mp = tempfile.mkdtemp()
        control_dir = os.path.join(self.mp, 'iPod_Control')
        photo_dir = os.path.join(control_dir, 'Photos')
        shutil.copytree('resources', control_dir)
        os.mkdir(photo_dir)
        self.db = gpod.PhotoDatabase(self.mp)
        # Example of setting a device property, adjust as needed
        gpod.itdb_device_set_sysinfo(self.db._itdb.device, "ModelNumStr", "MA450")

    def tearDown(self):
        # Tear down code for TestPhotoDatabase
        shutil.rmtree(self.mp)

    # Placeholder for an actual test method
    def test_dummy(self):
        # This is just a placeholder method. Replace or add actual test methods here.
        self.assertTrue(True, "Dummy test passes.")

    # Add your actual test methods here

if __name__ == '__main__':
    unittest.main()


if __name__ == '__main__':
    unittest.main()
