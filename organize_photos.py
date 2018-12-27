#!/usr/bin/env python

import argparse
import datetime
import exifread
import glob2
import os
import shutil
import sys
import time
import tqdm

def assure_path_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def find_files(folder):
    """ Find all image and video files under the folder folder 

    :param folder: folder to search
    :return: a list of video and images files
    """
    types = ['jpg', 'm2ts', 'JPG', 'MTS', 'png', 'm4v', 'mp4']
    files = []
    if not folder:
        folder = "./"

    # Use glob2 instead of glob to search files recursively. **/*.{} enable recursively search
    for type in types:
        files += glob2.glob(os.path.join(folder, "**/*.{}".format(type)))

    return files

def get_taken_date(photo_path):
    """ Get the photo taken time 
    
    :param photo_path: the path
    :return: truct_time 
    """
    with open(photo_path, 'rb') as fh:
        try:
            # Use exifread to read meta data of the image file
            # time.strptime parses the input string using the specified format
            # the return is struct_time, which is a named tuple
            tags = exifread.process_file(fh);
            return time.strptime(tags['Image DateTime'].values,"%Y:%m:%d %H:%M:%S")
        except KeyError:
            # Use time.gmtime to convert a timestamp to struct_time
            return time.gmtime(os.path.getmtime(photo_path))
        
def copy_photo(dest_root, photo_path):
    """ Copy a single file to year/month folder 
    :param dest_root: the root folder where you want to store the results
    :param photo_path: the path to the photo to be organized
    
    :return: the path to the result
    """
    imageDate = get_taken_date(photo_path)
    year = imageDate.tm_year
    month = imageDate.tm_mon
    parent = os.path.join(dest_root, str(year))
    child   = os.path.join(parent, str(month))
    assure_path_exists(child)
    
    file = os.path.basename(photo_path)
    dest = os.path.join(child, file)
    shutil.copyfile(photo_path, dest)
    return dest

def main(args):
    photos = find_files(args.source)
    if not args.dest:
        dest_root = os.getcwd()
    else:
        dest_root = args.dest

    # Use qtdm to print a progress bar. Use qtdm.write to output extra status information
    for photo_path in tqdm.tqdm(photos):
        dest = copy_photo(dest_root,photo_path)
        tqdm.tqdm.write("copy {} to {}".format(photo_path, dest))
        
if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="organize_photos.py", usage="%(prog)s Organize your photos (jpg, m2ts, mts, png) by copying them to monthly folders.")
    parser.add_argument('source',
                        help='the source directory')
    parser.add_argument('dest',
                        help='the target directory')

    args = parser.parse_args()
    main(args)
