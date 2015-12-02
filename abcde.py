#!/usr/bin/python3

import glob
import io
import os
import shutil

# 1. copy albums from newCDs to extHD mp3, ogg, flac folders.
# 2. examine mp3, ogg, flac folders for missing albums.
# 3. examine extHD albums for duplicate tracks (varying track titles)
#    and let user choose which to keep.
# 4. (maybe) edit mp3 filenames to be Windows-compatible.
#        (removing special characters and/or converting to ASCII)

EXTS = ('flac', 'mp3', 'ogg')

class AlbumInstance(object):
    """
    Represents one music album in one location on disk.
    """

    def __init__(self, filepath):
        """
        Initialize the album given the path of the directory.
        """

        self.location = filepath
        # filelist does not include the path
        self.filelist = [os.path.split(s)[-1] for s in os.listdir(filepath)]

        self.list_by_ext = {}
        for ftype in EXTS:
            # don't include the file path
            self.list_by_ext[ftype] = [
                os.path.split(s)[-1]
                for s in glob.glob(os.path.join(filepath, '*.' + ftype))]
            self.has_ext[ftype] = bool(self.list_by_ext[ftype])

        self.misc_files = []
        for filename in os.listdir(filepath):
            pass
            if False:
                self.misc_files.append(filename)

        self.multidisk
        self.n_tracks

    def find_duplicate_tracks(self):
        """
        Examine album files for duplicate tracks with varied names.
        """

        pass
