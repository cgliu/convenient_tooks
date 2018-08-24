import glob
import time
import datetime
import os, shutil
import sys
import argparse


def assure_path_exists(path):
    if not os.path.exists(path):
        os.makedirs(path)

def find_files(source):
    types = ['jpg', 'm2ts', 'JPG', 'MTS', 'png']
    files = []
    if not source:
        source = "./"
    for type in types:
        files += glob.glob(os.path.join(source, "*." + type))

    return files


def main(args):
    photos = find_files(args.source)
    if not args.dest:
        root = os.getcwd()
    else:
        root = args.dest

    for photo in photos:
        t = os.path.getmtime(photo)
        date = datetime.datetime.fromtimestamp(t)
        parent = os.path.join(root, str(date.year))
        child   = os.path.join(parent, str(date.month))

        assure_path_exists(child)

        file = os.path.basename(photo)
        dest = os.path.join(child, file)
        print "Copy " + photo + " to " + dest
        shutil.copyfile(photo, dest)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(prog="organize_photos.py", usage="%(prog)s Organize your photos (jpg, m2ts, mts, png) by copying them to monthly folders.")
    parser.add_argument('source',
                        help='the source directory')
    parser.add_argument('dest',
                        help='the target directory')

    args = parser.parse_args()
    main(args)
