# -*- coding: utf-8 -*-
"""

Format the code source based on rules


"""


import time
import gc
from collections import defaultdict
from attrdict import AttrDict as dict2
import copy
import util
import re
import numpy as np
import _pickle as cPickle
import os
import sys
import platform
import arrow
import pandas as pd


DIRCWD = r'C:/aacredit/'
os.chdir(DIRCWD)
sys.path.append(DIRCWD + '/aapackage')  # print(DIRCWD, CFG)
# print(os.environ)

####  tab character :     '	'   #####################################################
#####################################################################################
dir_training = r'C:data/'


#####################################################################################
path1 = r'gitcode/scores/'
win = 'deepctr'
wout = 'scores'

oklist = ['py', 'txt', 'ini', 'yaml', 'sql', 'sh']


regex = re.compile(re.escape(win), re.IGNORECASE)


# All Files
aa = util.os_file_listall(path1, pattern='*', dirlevel=10, onlyfolder=0)
for x in aa[2]:
    p = x[:x.rfind('\\')+1]
    f = x[x.rfind('\\')+1:]

    f2 = regex.sub(wout, f)
    os.rename(p + f, p + f2)


# Folder recursive
aa = util.os_file_listall(path1, pattern='*', dirlevel=1, onlyfolder=1)
for x in aa[2]:
    p = x[:x.rfind('\\')+1]
    f = x[x.rfind('\\')+1:]

    f2 = regex.sub(wout, f)
    os.rename(p + f, p + f2)

aa = util.os_file_listall(path1, pattern='*', dirlevel=2, onlyfolder=1)
for x in aa[2]:
    p = x[:x.rfind('\\')+1]
    f = x[x.rfind('\\')+1:]

    f2 = regex.sub(wout, f)
    os.rename(p + f, p + f2)

aa = util.os_file_listall(path1, pattern='*', dirlevel=3, onlyfolder=1)
for x in aa[2]:
    p = x[:x.rfind('\\')+1]
    f = x[x.rfind('\\')+1:]

    f2 = regex.sub(wout, f)
    os.rename(p + f, p + f2)


def os_file_rename(some_dir, pattern="*.*", pattern2="", dirlevel=1):
    import fnmatch
    import os
    import numpy as np
    import re

    matches = []
    some_dir = some_dir.rstrip(os.path.sep)
    assert os.path.exists(some_dir)
    num_sep = some_dir.count(os.path.sep)
    for root, dirs, files in os.walk(some_dir):
        num_sep_this = root.count(os.path.sep)
        if num_sep + dirlevel <= num_sep_this:
            del dirs[:]
        matches.append([])
        matches.append([])
        matches.append([])
        # Filename, DirName
        for inner_files in fnmatch.filter(files, pattern):
            # replace pattern by pattern2
            nfile = re.sub(pattern, pattern2, inner_files)
            os.path.abspath(root)
            os.rename(inner_files, nfile)

            matches[0].append(os.path.splitext(nfile)[0])
            matches[1].append(os.path.splitext(nfile)[1])
            matches[2].append(os.path.join(root, nfile))
    return np.array(matches).T


#####################################################################################
### In file replacement  ############################################################
aa = util.os_file_listall(path1, pattern='*', dirlevel=100, onlyfolder=0)
for x in aa[2]:
    if x[x.rfind('.')+1:] in oklist:
        with open(x, 'r') as file:
            filedata = file.read()

        filedata = regex.sub(wout, filedata)

        # Write the file out again
        with open(x, 'w') as file:
            file.write(filedata)

#####################################################################################
#####################################################################################


def _os_file_search_fast(fname, texts=None, mode="regex/str"):
    if texts is None:
        texts = ["myword"]

    res = []  # url:   line_id, match start, line
    enc = "utf-8"
    fname = os.path.abspath(fname)
    try:
        if mode == "regex":
            texts = [(text, re.compile(text.encode(enc))) for text in texts]
            for lineno, line in enumerate(open(fname, "rb")):
                for text, textc in texts:
                    found = re.search(textc, line)
                    if found is not None:
                        try:
                            line_enc = line.decode(enc)
                        except UnicodeError:
                            line_enc = line
                        res.append((text, fname, lineno + 1,
                                    found.start(), line_enc))

        elif mode == "str":
            texts = [(text, text.encode(enc)) for text in texts]
            for lineno, line in enumerate(open(fname, "rb")):
                for text, textc in texts:
                    found = line.find(textc)
                    if found > -1:
                        try:
                            line_enc = line.decode(enc)
                        except UnicodeError:
                            line_enc = line
                        res.append((text, fname, lineno + 1, found, line_enc))

    except IOError as xxx_todo_changeme:
        (_errno, _strerror) = xxx_todo_changeme.args
        print("permission denied errors were encountered")

    except re.error:
        print("invalid regular expression")

    return res


def os_file_replace(source_file_path, pattern, substring):
    from tempfile import mkstemp
    from shutil import move
    from os import remove

    fh, target_file_path = mkstemp()
    with open(target_file_path, "w") as target_file:
        with open(source_file_path, "r") as source_file:
            for line in source_file:
                target_file.write(line.replace(pattern, substring))
    remove(source_file_path)
    move(target_file_path, source_file_path)


def os_file_replacestring1(find_str, rep_str, file_path):
    """replaces all find_str by rep_str in file file_path"""
    import fileinput

    file1 = fileinput.FileInput(file_path, inplace=True, backup=".bak")
    for line in file1:
        line = line.replace(find_str, rep_str)
        sys.stdout.write(line)
    file1.close()
    print(("OK: " + format(file_path)))


def os_file_replacestring2(findstr, replacestr, some_dir, pattern="*.*", dirlevel=1):
    """ #fil_replacestring_files("logo.png", "logonew.png", r"D:/__Alpaca__details/aiportfolio",
    pattern="*.html", dirlevel=5  )
  """
    list_file = os_file_listall(some_dir, pattern=pattern, dirlevel=dirlevel)
    list_file = list_file[2]
    for file1 in list_file:
        os_file_replacestring1(findstr, replacestr, file1)


def os_file_getname(path):
    import ntpath

    head, tail = ntpath.split(path)
    return tail or ntpath.basename(head)


def os_file_getpath(path):
    import ntpath

    head, tail = ntpath.split(path)
    return head


def os_file_gettext(file1):
    with open(file1, "r", encoding="UTF-8") as f:
        return f.read()
    # def os_file_listall(some_dir, pattern="*.*", dirlevel=1):
    #  return listallfile(some_dir, pattern=pattern, dirlevel=dirlevel)


def os_file_listall(dir1, pattern="*.*", dirlevel=1, onlyfolder=0):
    r"""
   # DIRCWD=r"D:\_devs\Python01\project"
   # aa= listallfile(DIRCWD, "*.*", 2)
   # aa[0][30];   aa[2][30]
  """
    import fnmatch
    import os
    import numpy as np

    matches = []
    dir1 = dir1.rstrip(os.path.sep)
    num_sep = dir1.count(os.path.sep)

    if onlyfolder:
        for root, dirs, files in os.walk(dir1):
            num_sep_this = root.count(os.path.sep)
            if num_sep + dirlevel <= num_sep_this:
                del dirs[:]
            matches.append([])
            matches.append([])
            matches.append([])
            # Filename, DirName
            for inner_dirs in fnmatch.filter(dirs, pattern):
                matches[0].append(os.path.splitext(inner_dirs)[0])
                matches[1].append(os.path.splitext(root)[0])
                matches[2].append(os.path.join(root, inner_dirs))
        return np.array(matches)

    for root, dirs, files in os.walk(dir1):
        num_sep_this = root.count(os.path.sep)
        if num_sep + dirlevel <= num_sep_this:
            del dirs[:]
        matches.append([])
        matches.append([])
        matches.append([])
        # Filename, DirName
        for inner_files in fnmatch.filter(files, pattern):
            matches[0].append(os.path.splitext(inner_files)[0])
            matches[1].append(os.path.splitext(inner_files)[1])
            matches[2].append(os.path.join(root, inner_files))
    return np.array(matches)


#####################################################################################
path1 = r'C:git_test/tfquantize_/'
win = 'fm_'
wout = 'qt_'

regex = re.compile(re.escape(win), re.IGNORECASE)


### All Files  ######################################################################
aa = util.os_file_listall(path1, pattern='*', dirlevel=10, onlyfolder=0)
for x in aa[2]:
    p = x[:x.rfind('\\')+1]
    f = x[x.rfind('\\')+1:]

    f2 = regex.sub(wout, f)
    os.rename(p + f, p + f2)


#### Folder recursive    ############################################################
aa = util.os_file_listall(path1, pattern='*', dirlevel=1, onlyfolder=1)
for x in aa[2]:
    p = x[:x.rfind('\\')+1]
    f = x[x.rfind('\\')+1:]

    f2 = regex.sub(wout, f)
    os.rename(p + f, p + f2)

aa = util.os_file_listall(path1, pattern='*', dirlevel=2, onlyfolder=1)
for x in aa[2]:
    p = x[:x.rfind('\\')+1]
    f = x[x.rfind('\\')+1:]

    f2 = regex.sub(wout, f)
    os.rename(p + f, p + f2)

aa = util.os_file_listall(path1, pattern='*', dirlevel=3, onlyfolder=1)
for x in aa[2]:
    p = x[:x.rfind('\\')+1]
    f = x[x.rfind('\\')+1:]

    f2 = regex.sub(wout, f)
    os.rename(p + f, p + f2)


### In file replacement     #########################################################
aa = util.os_file_listall(path1, pattern='*', dirlevel=100, onlyfolder=0)
for x in aa[2]:
    if x[x.rfind('.')+1:] in ['py', 'txt', 'ini', 'yaml']:
        with open(x, 'r') as file:
            filedata = file.read()

        filedata = regex.sub(wout, filedata)

        # Write the file out again
        with open(x, 'w') as file:
            file.write(filedata)
