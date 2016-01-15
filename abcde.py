#!/usr/bin/python3

import glob
import io
import os
import shutil
import datetime
import pdb

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

    album_list = get_album_list('/home/plimley/Music/new CDs')


class FileInstance(object):
    """
    Represents one file in one location on disk.
    """

    def __init__(self, filepath):
        """
        """
        self.fullpath = filepath
        self.path, self.filename = os.path.split(filepath)
        self.name, ext = os.path.splitext(self.filename)
        self.ext = ext[1:]      # drop the .

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
        self.get_name()

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

    def get_name(self):
        head, tail = os.path.split(self.location)
        if tail == '':
            _, tail = os.path.split(head)
        self.name = tail

    def copy(self, target_dir, ext=None, overwrite=False, rm_original=False):
        """
        Copy the album dir into target_dir.
        if ext is not None, only copy files of this ext.
        """

        if ext not in EXTS:
            ext = None

        if not os.path.isdir(target_dir):
            os.mkdir(target_dir)

        dest_dir = os.path.join(target_dir, self.name)
        if os.path.isdir(dest_dir) and overwrite:
            print('Warning: {} already exists, proceeding anyway'.format(
                dest_dir))
        elif os.path.isdir(dest_dir):
            return None
        else:
            os.mkdir(dest_dir)

        if ext is None:
            filelist = self.filelist
        else:
            filelist = self.list_by_ext[ext]

        for f in filelist:
            shutil.copy2(f.fullpath,
                         os.path.join(dest_dir, f.filename))

        if rm_original:
            while filelist:
                self.del_file(filelist.pop())

    def split_exts(self, target_dir, overwrite=False, rm_original=False):
        """
        For album located in src_dir/album_dir:
          copy src_dir/album_dir/*.mp3 to target_dir/mp3/album_dir/*.mp3
        and similarly for each extension type.
        """

        if not all(self.has_ext.values()):
            raise AbcdeException('File types not found')

        for ftype in EXTS:
            this_dest_dir = os.path.join(target_dir, ftype)
            self.copy(this_dest_dir, ext=ftype,
                      overwrite=overwrite, rm_original=rm_original)

    def del_file(self, file_obj):
        """
        Remove file file_obj, also removing references in the album lists.
        file_obj is a FileInstance object.
        """

        if file_obj not in self.filelist:
            raise AbcdeException('Cannot delete file: file object not found')

        self.filelist.remove(file_obj)
        for ftype in EXTS:
            if file_obj in self.list_by_ext[ftype]:
                self.list_by_ext[ftype].remove(file_obj)
        os.remove(file_obj.fullpath)

    def find_duplicate_tracks(self):
        """
        Examine album files for duplicate tracks with varied names.
        """

        pass

    def __str__(self):
        return self.location


def get_album_list(dirname):
    """
    Return a list of albums from the contents of directory, dirname.
    """

    album_dir_list = [os.path.join(dirname, d) for d in os.listdir(dirname)]
    album_dir_list.sort()

    album_list = [AlbumInstance(a) for a in album_dir_list]

    return album_list


def split_albums(source_dir, target_dir,
                 overwrite=False, rm_original=False, verbosity=1):
    """
    Split all albums in source_dir according to extensions, to
    target_dir/mp3/album-name/ (for example)
    """

    albumlist = get_album_list(source_dir)

    for album in albumlist:
        try:
            album.split_exts(
                target_dir, overwrite=overwrite, rm_original=rm_original)
            if verbosity > 0:
                print('Completed ' + album.name)
        except AbcdeException:
            if verbosity > 0:
                print(' Error on ' + album.name)

class AbcdeException(Exception):
    pass


if __name__ == '__main__':
    main()