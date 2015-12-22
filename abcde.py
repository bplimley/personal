#!/usr/bin/python3

import glob
import io
import os
import shutil
import datetime

# 1. copy albums from newCDs to extHD mp3, ogg, flac folders.
# 2. examine mp3, ogg, flac folders for missing albums.
# 3. examine extHD albums for duplicate tracks (varying track titles)
#    and let user choose which to keep.
# 4. (maybe) edit mp3 filenames to be Windows-compatible.
#        (removing special characters and/or converting to ASCII)

EXTS = ('flac', 'mp3', 'ogg')


def main():
    # tests
    albumdir = '/home/plimley/Music/new CDs/Sara Bareilles - Little Voice'
    a = AlbumInstance(albumdir)


class FileInstance(object):
    """
    Represents one file in one location on disk.
    """

    def __init__(self, filepath):
        """
        """
        self.path, self.filename = os.path.split(filepath)
        self.name, ext = os.path.splitext(self.filename)
        self.ext = ext[1:]

        self.stat = os.stat(filepath)

        self.is_music = (self.ext in EXTS)

        if self.is_music:
            num_str, name_str = self.name.split(sep=' - ', maxsplit=1)
            self.track_num = int(num_str)
            self.track_name = name_str
            self.bytes = self.stat.st_size
            self.mtime = datetime.datetime.fromtimestamp(self.stat.st_mtime)


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
        self.filelist = [FileInstance(os.path.join(filepath, s))
                         for s in os.listdir(filepath)]
        self.musiclist = [f for f in self.filelist if f.is_music]

        self.list_by_ext = {}
        self.has_ext = {}
        for ftype in EXTS:
            self.list_by_ext[ftype] = [
                f for f in self.musiclist if f.ext == ftype]
            self.has_ext[ftype] = bool(self.list_by_ext[ftype])

        self.misc_files = [f for f in self.filelist if not f.is_music]

        if any(self.has_ext.values()):
            self.multidisc = self.musiclist[0].track_num > 99

            self.track_nums = set([f.track_num for f in self.musiclist])
            self.n_tracks = len(self.track_nums)

    def find_duplicate_tracks(self):
        """
        Examine album files for duplicate tracks with varied names.
        """

        pass


if __name__ == '__main__':
    main()
