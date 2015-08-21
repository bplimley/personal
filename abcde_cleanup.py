# abcde_cleanup.py

import glob
import io
import os
import shutil

BASE_MUSIC_DIR = unicode("/home/plimley/Music")
NEW_MUSIC_DIR = os.path.join(BASE_MUSIC_DIR,"new CDs")
EXT_MUSIC_DIR = unicode("/media/plimley/MUSIC")
EXT_MUSIC_SUBDIR = unicode("CDs")
# AUDIO_TYPES = ("flac","mp3","ogg")
AUDIO_TYPES = ("flac",)
# flac, mp3, ogg folders are located in BASE_MUSIC_DIR

def identify_new_albums(audio_type):
    """
    Compare the albums in NEW_MUSIC_DIR to those in
    BASE_MUSIC_DIR/audio_type, and return a list of albums which are
    not in the latter.
    """

    old_music_dir = os.path.join(BASE_MUSIC_DIR,audio_type)
    old_music_dirlist = [album
        for album in os.listdir(old_music_dir)
        if os.path.isdir(os.path.join(old_music_dir,album))]
    new_music_dirlist = [album
        for album in os.listdir(NEW_MUSIC_DIR)
        if os.path.isdir(os.path.join(NEW_MUSIC_DIR,album))
        if album not in old_music_dirlist]
    return new_music_dirlist

def copy_album(album, audio_type, del_flag=False):
    """
    Copy the album named [album] from NEW_MUSIC_DIR to
    BASE_MUSIC_DIR/audio_type.

    If del_flag == True, then remove the files from NEW_MUSIC_DIR.
    """

    album = check_unicode(album)
    audio_type = check_unicode(audio_type)

    this_source_dir = os.path.join(NEW_MUSIC_DIR,album)
    this_dest_dir = os.path.join(BASE_MUSIC_DIR,audio_type,album)
    os.mkdir(this_dest_dir)
    filelist = glob.glob(os.path.join(
            this_source_dir,"*." + audio_type))
    # move all of the files from the album before removing any.
    # Thus, if any errors come up, all of the original files remain
    # in place.
    for f in filelist:
        shutil.copy2(f, this_dest_dir)
    if del_flag:
        for f in filelist:
            os.remove(f)

def check_unicode(input_string):
    try:
        output_string = input_string.decode('utf-8')
    except UnicodeEncodeError:
        output_string = input_string
    return output_string

def copy_all_albums(del_flag=True,verbose=1):
    """
    Local re-organization of audio files into folders by type.

    I.e. for all AUDIO_TYPES: identify_new_albums and copy_album(s).
    """

    album_list = identify_new_albums(audio_type).sort()
    for album in album_list:
        for audio_type in AUDIO_TYPES:
            if verbose>0:
                print "Copying " + audio_type + " from " + album + "..."
            copy_album(album, audio_type, del_flag)

def copy_to_ext(album, audio_type, del_flag=False):
    """
    Copy one audio type of a CLEANED-UP album to the external HD.

    By cleaned-up, I mean it has already been separated by audio type.
    """

    album = check_unicode(album)
    audio_type = check_unicode(audio_type)

    this_source_dir = os.path.join(BASE_MUSIC_DIR,audio_type,album)
    this_dest_dir = os.path.join(EXT_MUSIC_DIR,audio_type,
                                 EXT_MUSIC_SUBDIR,album)
    os.mkdir(this_dest_dir)
    filelist = os.listdir(this_source_dir).sort()
    for f in filelist:
        shutil.copy2(os.path.join(this_source_dir,f), this_dest_dir)
    if del_flag:
        for f in filelist:
            os.remove(os.path.join(this_source_dir,f))

def copy_all_to_ext(del_flag=False):
    """
    Copy all albums of all types to external HD, as needed.
    """



# use this for running from command line:
if __name__ == "__main__":
    import sys
    my_function(sys.argv[1])



