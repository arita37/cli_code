# -*- coding: utf-8 -*-

"""
#---------Various Utilities function for Python--------------------------------------



"""
from __future__ import division, print_function

import copy
import datetime
import errno
import fnmatch
import gc
import glob
import importlib
import operator
import os
import pickle
import re
import shutil
import subprocess
import sys
import time
import zipfile


import IPython
import numpy as np
import pandas as pd
import pip
import psutil

# Date Manipulation
from dateutil import parser
# noinspection PyUnresolvedReferences
from future import standard_library


if sys.platform.find("win") > -1:
    print("")



DIRCWD = os.path.dirname(os.path.abspath(__file__))
# os.chdir(DIRCWD); sys.path.append(DIRCWD + '/aapackage')


__path__ = DIRCWD + "/aapackage/"
__version__ = "1.0.0"


# __file__=     "util.py"


# Serialize Python Session
def session_load_function(name="test_20160815"):
    import dill

    n1 = DIRCWD + "/aaserialize/session/" + name + ".pkl"

    dill.load_session(n1)
    print(n1)


def session_save_function(name="test"):
    t1 = date_now()
    n1 = DIRCWD + "/aaserialize/session/dill_session_" + name + "_" + t1 + ".pkl"

    dill.dump_session(n1)
    print(n1)



#  Import File
# runfile('D:/_devs/Python01/project27/stockMarket/google_intraday.py', wdir='D:/_devs/Python01/project27/stockMarket')


def aa_unicode_ascii_utf8_issue():
    """Take All csv in a folder and provide Table, Column Schema, type

 METHOD FOR Unicode / ASCII issue
1. Decode early
Decode to <type 'unicode'> ASAP
df['PREF_NAME']=       df['PREF_NAME'].apply(to_unicode)

2. Unicode everywhere


3. Encode late
# >>> f = open('/tmp/ivan_out.txt','w')
# >>> f.write(ivan_uni.encode('utf-8'))

Important methods
s.decode(encoding)  <type 'str'> to <type 'unicode'>
u.encode(encoding)  <type 'unicode'> to <type 'str'>

http://farmdev.com/talks/unicode/

   """


def isfloat(x):
    try:
        if x == np.inf:
            return False
        float(x)
        return True
    except ValueError:
        return False


def isint(x):
    return isinstance(x, (int, np.int, np.int64, np.int32))


def isanaconda():
    txt = sys.version
    if txt.find("Continuum") > 0:
        return True
    else:
        return False


def a_run_ipython(cmd1):
    """ Execute Ipython Command in python code
     run -i :  run including current interprete variable
 """
    IPython.get_ipython().magic(cmd1)


def py_autoreload():
    a_run_ipython("load_ext autoreload")
    a_run_ipython("autoreload 2")


def os_platform():
    return ""


def a_start_log(id1="", folder="aaserialize/log/"):
    a_run_ipython(
        "logstart -o -r -t "
        + folder
        + "log"
        + str(id1)
        + "_"
        + os_platform()
        + "_"
        + date_now()
        + " rotate"
    )


def a_cleanmemory():
    import gc

    gc.collect()


def a_info_conda_jupyter():
    s = """
 CONDA COMMAND :
  'roll back' an installation, downgrading
     conda list  --revisions
     conda install --revision [revision number]         #Roll back to this number

  conda update PackageName

  conda uninstall PackageName


 IPYPARALLEL :
    Enable tab in Jupyter:   ipcluster nbextension enable
    Disable :                ipcluster nbextension enable
    Start 3 clsuter          ipcluster start -n 3
        <Stop them           ipclsuter stop

 JUPYTER Notebook :
      jupyter notebook      :  Enable Jupyter Server
      Close : Ctrl + C
      %connect_info      : To get Connection Details of Ipytho notebook


 """
    print(s)


def a_run_cmd(cmd1):
    os_process_run(cmd1)


# cmd("ipconfig")


def a_help():
    help_str = r"""
  PYCHARM shortcut :
    Highlight the Text  +  Alt +G   : Google Search
    Atl+C :  Doc   Alt+X : Doc     Alt+W : Doc Internet
    Ctrl+W : Refactor Name
    Shift + Shift  : Search Everywhere
    TouchRigh of Altgr + TouchRigh of Altgr: Definition of method

  #Save Session       session_save('/kaggle/supermarket_02', globals())

  #Load Session       session_load('/kaggle/kaggle_supermarket_01')


 1) %load_ext autoreload     #Reload the packages
    %autoreload 2

 2) Install PIP:
     If Permission access,Exit Spyder,  Use CMD
       D:\WinPython-64-2710\scripts>pip install scikit-learn --upgrade -

     !pip install NAME --upgrade --no-deps  #NO dependencies installed.

     !pip install git+git://github.com/fchollet/keras.git --upgrade --no-deps
     !pip install https://github.com//pymc3/archive/master.zip
     !pip install  https://github.com/jpype-py3 /zipball/master  or  /tarball/master

     !pip install c:\this_is_here\numpy-1.10.4+mkl-cp27-cp27m-win_amd64.whl
     !pip freeze   to get the list of package isntall

     !pip install -h    Help on pip

 3) Windows CMD:
    a_run_cmd("ipconfig")

    A: [enter] Changes the default drive from C to A.
   cd \furniture\chairs.  Moves you to the directory  'FURNITURE'
   cd .. Moves you up one level in the path.
   cd \  Takes you back to the root directory (c: in this case).


 4) import sys
    reload(sys)
    sys.setdefaultencoding('utf8')
    sys.getdefaultencoding()

 5)
    !pip install packagename
    The ! prefix is a short-hand for the %sc command to run a shell command.

    You can also use the !! prefix which is a short-hand for the %sx command to execute a shell
    command and capture its output (saved into the _ variable by default).

  6) Compile a modified package
    1) Put into a folder
    2) Add the folder to the Python Path (Spyder Python path)


    3) Compile in Spyder using, (full directory)
       !!python D:\\_devs\\Python01\\project27\\scikit_learn\\sklearn\\setup.py install

    4) Project is built here:
      D:\_devs\Python01\project27\build\lib.win-amd64-2.7
      http://scikit-learn.org/dev/developers/contributing.html#git-repo
python setup.py develop

Convert Python 2 to Python 3
import lib2to3

!2to3 D:\_devs\Python01\project\aapackage\codeanalysis.py

D:\_devs\Python01\project\zjavajar

# os.system('cd D:\_app\visualstudio13\Common7\IDE') #Execute any command
# os.path.abspath('memo.txt') #get absolute path
# os.path.exists('memo.txt')
# os.path.exists('memo.txt')
# os.getenv('PATH')    #Get environ variable

# sitepackage= r'D:\_devs\Python01\WinPython-64-2710\python-2.7.10.amd64\Lib\site-packages/'


  """
    os_gui_popup_show(help_str)
    # print(help_str)


def a_info_system():
    import platform

    print((platform.platform() + "\n"))
    # conda install -c anaconda psutil=5.0.0
    # https://github.com/nicolargo/glances
    import sys

    print(("Python", sys.version))
    a_info_packagelist()


def a_info_packagelist():
    installed_packages = pip.get_installed_distributions()
    installed_packages_list = sorted(["%s==%s" % (i.key, i.version) for i in installed_packages])
    for p in installed_packages_list:
        print(p)
    # def aa_getlistofpackage() : np.__config__.show(); a_info_packagelist()


def a_get_pythonversion():
    return sys.version_info[0]


# Printers
def print_object(vv, txt=""):
    """ #Print Object Table  """
    print(("\n\n" + txt + "\n"))
    sh = np.shape(vv)
    kkmax, iimax = sh[0], sh[1]
    for k in range(0, kkmax):
        aux = ""
        for i in range(0, iimax):
            if vv[k, 0] is not None:
                aux += str(vv[k, i]) + ","

        if vv[k, 0] is not None:
            print(aux)


def print_object_tofile(vv, txt, file1="d:/regression_output.py"):
    """ #Print to file Object   Table   """
    with open(file1, mode="a") as file1:
        file1.write("\n\n" + txt + "\n")
        sh = np.shape(vv)
        kkmax, iimax = sh[0], sh[1]
        for k in range(0, kkmax):
            aux = ""
            for i in range(0, iimax):
                if vv[k, 0] is not None:
                    aux += str(vv[k, i]) + ","

            if vv[k, 0] is not None:
                # print (aux )
                file1.write(aux + "\n")


def print_progressbar(iteration, total, prefix="", suffix="", decimals=1, bar_length=100):
    """# Print iterations progress
     Call in a loop to create terminal progress bar
    @params:
        iteration   - Required  : current iteration (Int)
        total       - Required  : total iterations (Int)
        prefix      - Optional  : prefix string (Str)
        suffix      - Optional  : suffix string (Str)
        decimals    - Optional  : positive number of decimals in percent complete (Int)
        bar_length   - Optional  : character length of bar (Int)
    """
    format_str = "{0:." + str(decimals) + "f}"
    percent = format_str.format(100 * (iteration / float(total)))
    filled_length = int(round(bar_length * iteration / float(total)))
    bar = "#" * filled_length + "-" * (bar_length - filled_length)
    sys.stdout.write("\r%s |%s| %s%s %s" % (prefix, bar, percent, "%", suffix)),
    if iteration == total:
        sys.stdout.write("\n")
    sys.stdout.flush()
    """
    for item in items:
     # Do stuff...
     # Update Progress Bar
     i += 1
     printProgress(i, l, prefix = 'Progress:', suffix = 'Complete', bar_length = 50)
    """


# OS-
def os_zip_checkintegrity(filezip1):
    zip_file = zipfile.ZipFile(filezip1)
    try:
        ret = zip_file.testzip()
        if ret is not None:
            print("First bad file in zip: %s" % ret)
            return False
        else:
            return True
    except RuntimeError:
        return False


def os_zipfile(folderin, folderzipname, iscompress=True):
    compress = zipfile.ZIP_DEFLATED if iscompress else zipfile.ZIP_STORED
    zf = zipfile.ZipFile(folderzipname, "w", compress, allowZip64=True)

    for dirname, subdirs, files in os.walk(folderin):
        zf.write(dirname)
        for filename in files:
            zf.write(os.path.join(dirname, filename))
    zf.close()

    r = os_zip_checkintegrity(folderzipname)
    if r:
        return folderin, folderzipname
    else:
        print("Corrupt File")
        return folderin, False


def os_zipfolder(
    dir_tozip="/zdisks3/output", zipname="/zdisk3/output.zip", dir_prefix=True, iscompress=True
):
    """
 shutil.make_archive('/zdisks3/results/output', 'zip',
                     root_dir=/zdisks3/results/',
                     base_dir='output')
 os_zipfolder('zdisk/test/aapackage', 'zdisk/test/aapackage.zip', 'zdisk/test')"""
    import shutil

    _ = iscompress

    dir_tozip = dir_tozip if dir_tozip[-1] != "/" else dir_tozip[:-1]
    # dir_prefix= dir_prefix if dir_prefix[-1] != '/' else dir_prefix[:-1]

    if dir_prefix:
        dir_tozip, dir_prefix = "/".join(dir_tozip.split("/")[:-1]), dir_tozip.split("/")[-1]
    else:
        dir_tozip, dir_prefix = dir_tozip, "/"

    shutil.make_archive(zipname.replace(".zip", ""), "zip", dir_tozip, base_dir=dir_prefix)
    """
   shutil.make_archive(
      base_name, format[, root_dir[, base_dir[, verbose[, dry_run[, owner[, group[, logger]]]]]]])

   base_name is the name of the file to create, including the path, minus any format-specific
   extension. format is the archive format: one of "zip" (if the zlib module or external zip
   executable is available), "tar", "gztar" (if the zlib module is available), or "bztar"
   (if the bz2 module is available).
   root_dir is a directory that will be the root directory of the archive; ie. we typically chdir
   into root_dir before creating the archive.
   base_dir is the directory where we start archiving from; ie. base_dir will be the common
   prefix of all files and directories in the archive.
   root_dir and base_dir both default to the current directory.
   owner and group are used when creating a tar archive.

   import zipfile
   compress = zipfile.ZIP_DEFLATED if iscompress else  zipfile.ZIP_STORED
   zf= zipfile.ZipFile(zipname, "w", compress, allowZip64=True)
   for dirname, subdirs, files in os.walk(dir_tozip):
      zf.write(dirname)
      for filename in files:  zf.write(os.path.join(dirname, filename))
   zf.close()
 """
    r = os_zip_checkintegrity(zipname)
    if r:
        return zipname
    else:
        print("Corrupt File")
        return False


def os_zipextractall(filezip_or_dir="folder1/*.zip", tofolderextract="zdisk/test", isprint=1):
    """os_zipextractall( 'aapackage.zip','zdisk/test/'      )  """
    import zipfile

    _ = isprint

    if filezip_or_dir.find("*") > -1:  # Many Zip
        ziplist1 = os_file_listall(filezip_or_dir[: filezip_or_dir.find("*")], "*.zip")
        fileziplist_full = ziplist1[2]

    else:  # Only 1
        fileziplist_full = [filezip_or_dir]

    # if os.path.exists( foldernew2  ) :      #Either File or Folder exists
    #   print('Renaming Folder ' + foldernew + ' with _')
    #   # lastfolder, beforelast= tofolderextract.split('/')[]
    #   os_folder_copy(foldernew2,  foldernew2+'_' )

    isok = None
    for filezip in fileziplist_full:
        filezip_name = os_file_getname(filezip)
        zip_ref = zipfile.ZipFile(filezip, "r")
        zip_ref.extractall(tofolderextract)  # Will create the path
        zip_ref.close()
        isok = os.path.exists(tofolderextract)
        if not isok:
            print("Error: " + filezip_name)

    if isok is not None and isok:
        return tofolderextract
    else:
        return -1


def os_folder_copy(src, dst, symlinks=False, pattern1="*.py", fun_file_toignore=None):
    """
       callable(src, names) -> ignored_names
       'src' parameter, which is the directory being visited by copytree(), and
       'names' which is the list of `src` contents, as returned by os.listdir():

    Since copytree() is called recursively, the callable will be called once for each
    directory that is copied.
    It returns a  list of names relative to the `src` directory that should not be copied.
   """

    def _default_fun_file_toignore(src, names):
        _ = src

        pattern = "!" + pattern1
        file_toignore = fnmatch.filter(names, pattern)
        return file_toignore

    if fun_file_toignore is None:
        fun_file_toignore = _default_fun_file_toignore

    try:
        shutil.copytree(src, dst, symlinks=symlinks, ignore=fun_file_toignore)
    except OSError as exc:  # python >2.5
        if exc.errno == errno.ENOTDIR:
            shutil.copy(src, dst, follow_symlinks=False)
        else:
            raise


def os_folder_create(directory):
    dir0 = os.getcwd()
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.chdir(dir0)


def os_folder_robocopy(from_folder="", to_folder="", my_log="H:/robocopy_log.txt"):
    """
    Copy files to working directory
    robocopy <Source> <Destination> [<File>[ ...]] [<Options>]
    We want to copy the files to a fast SSD drive
    """

    if os.path.isdir(from_folder) & os.path.isdir(to_folder):
        subprocess.call(["robocopy", from_folder, to_folder, "/LOG:%s" % my_log])
    else:
        print("Paths not entered correctly")


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


def os_file_listall2(dir1, pattern="*.*", dirlevel=1, onlyfolder=0):
    r""" dirpath, filename, fullpath
   # DIRCWD=r"D:\_devs\Python01\project"
   # aa= listallfile(DIRCWD, "*.*", 2)
   # aa[0][30];   aa[2][30]
  """
    _ = onlyfolder

    matches = {}
    dir1 = dir1.rstrip(os.path.sep)
    num_sep = dir1.count(os.path.sep)

    for root, dirs, files in os.walk(dir1):
        num_sep_this = root.count(os.path.sep)
        if num_sep + dirlevel <= num_sep_this:
            del dirs[:]
        matches["dirpath"] = []
        matches["filename"] = []
        matches["fullpath"] = []
        for f in fnmatch.filter(files, pattern):
            matches["dirpath"].append(os.path.splitext(f)[0])
            matches["filename"].append(os.path.splitext(f)[1])
            matches["fullpath"].append(os.path.join(root, f))
    return matches


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
                        res.append((text, fname, lineno + 1, found.start(), line_enc))

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


# _os_file_search_fast(DIRCWD +"test.py", texts=[ u"from ","import "], mode="str")


def os_file_search_content(srch_pattern=None, mode="str", dir1="", file_pattern="*.*", dirlevel=1):
    if srch_pattern is None:
        srch_pattern = ["from ", "import "]

    list_all = os_file_listall(dir1, pattern=file_pattern, dirlevel=dirlevel)
    ll = []
    for f in list_all["fullpath"]:
        ll = ll + _os_file_search_fast(f, texts=srch_pattern, mode=mode)
    df = pd.DataFrame(ll, columns=["search", "filename", "lineno", "pos", "line"])
    return df


# aa= os_file_search_content(
#    srch_pattern=[ u"from ","import "], mode="str", dir1=DIRCWD, file_pattern="*.py", dirlevel=1)
# aa= os_file_search_content(
#    srch_pattern=[ u"from ","import "], mode="full", dir1=DIRCWD, file_pattern="*.py", dirlevel=1)


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


def os_gui_popup_show(txt):
    def os_gui_popup_show2(txt):
        from tkinter import Tk, Scrollbar, Text, mainloop, RIGHT, END, LEFT, Y

        root = Tk()
        scrollbar = Scrollbar(root)
        text = Text(root, height=50, width=90)
        scrollbar.pack(side=RIGHT, fill=Y)
        text.pack(side=LEFT, fill=Y)
        scrollbar.config(command=text.yview)
        text.config(yscrollcommand=scrollbar.set)
        text.insert(END, txt)
        root.attributes("-topmost", True)  # note - before topmost
        mainloop()

    os_gui_popup_show2(txt)
    # import _thread
    # _thread.start_new_thread(os_gui_popup_show2, (txt,))  #issues


def os_print_tofile(vv, file1, mode1="a"):  # print into a file='a
    """
    Here is a list of the different modes of opening a file:
r
Opens a file for reading only. The file pointer is placed at the beginning of the file.
This is the default mode.

rb

Opens a file for reading only in binary format. The file pointer is placed at the
beginning of the file. This is the default mode.
r+

Opens a file for both reading and writing. The file pointer will be at the beginning of the file.
rb+

Opens a file for both reading and writing in binary format. The file pointer will be at the
beginning of the file.
w

Opens a file for writing only. Overwrites the file if the file exists. If the file does not exist,
creates a new file for writing.
wb

Opens a file for writing only in binary format. Overwrites the file if the file exists.
If the file does not exist, creates a new file for writing.
w+

Opens a file for both writing and reading. Overwrites the existing file if the file exists.
If the file does not exist, creates a new file for reading and writing.
wb+

Opens a file for both writing and reading in binary format. Overwrites the existing file if
the file exists. If the file does not exist, creates a new file for reading and writing.
a

Opens a file for appending. The file pointer is at the end of the file if the file exists. That is,
the file is in the append mode. If the file does not exist, it creates a new file for writing.
ab

Opens a file for appending in binary format. The file pointer is at the end of the file if the file
exists. That is, the file is in the append mode. If the file does not exist, it creates a new file
for writing.
a+

Opens a file for both appending and reading. The file pointer is at the end of the file if the
file exists. The file opens in the append mode. If the file does not exist, it creates a new file
for reading and writing.
ab+

Opens a file for both appending and reading in binary format. The file pointer is at the end of
the file if the file exists. The file opens in the append mode. If the file does not exist,
it creates a new file for reading and writing.
To open a text file, use:
fh = open("hello.txt", "r")

To read a text file, use:
print fh.read()

To read one line at a time, use:
print fh.readline()

To read a list of lines use:
print fh.readlines()

To write to a file, use:
fh = open("hello.txt", "w")
lines_of_text = ["a line of text", "another line of text", "a third line"]
fh.writelines(lines_of_text)
fh.close()

To append to file, use:
fh = open("Hello.txt", "a")
fh.close()

    """
    with open(file1, mode1) as text_file:
        text_file.write(str(vv))


def os_path_norm(pth):  # Normalize path for Python directory
    r""" #r"D:\_devs\Python01\project\03-Connect_Java_CPP_Excel\PyBindGen\examples" """
    if a_get_pythonversion() == 2:
        ind = pth.find(":")
        if ind > -1:
            a, b = pth[:ind], pth[ind + 1 :].encode("string-escape").replace("\\x", "/")
            return "{}://{}".format(a, b.lstrip("\\//").replace("\\\\", "/"))
        else:
            return pth
    else:
        pth = pth.encode("unicode-escape").replace(b"\\x", b"/")
        return pth.replace(b"\\\\", b"/").decode("utf-8")


def os_path_change(path1):
    path1 = os_path_norm(path1)
    os.chdir(path1)  # Change Working directory path


def os_path_current():
    return os.getcwd()


def os_file_exist(file1):
    return os.path.exists(file1)


def os_file_size(file1):
    return os.path.getsize(file1)


def os_file_read(file1):
    fh = open(file1, "r")
    return fh.read()


def os_file_isame(file1, file2):
    import filecmp

    return filecmp.cmp(file1, file2)


def os_file_get_extension(file_path):
    """
    # >>> get_file_extension("/a/b/c")
    ''
    # >>> get_file_extension("/a/b/c.tar.xz")
    'xz'
    """
    _ext = os.path.splitext(file_path)[-1]
    if _ext:
        return _ext[1:] if _ext.startswith(".") else _ext

    return ""


def os_file_normpath(path):
    """Normalize path.
    - eliminating double slashes, etc. (os.path.normpath)
    - ensure paths contain ~[user]/ expanded.

    :param path: Path string :: str
    """
    return os.path.normpath(os.path.expanduser(path) if "~" in path else path)


def os_folder_is_path(path_or_stream):
    """
    Is given object `path_or_stream` a file path?
    :param path_or_stream: file path or stream, file/file-like object
    :return: True if `path_or_stream` is a file path
    """
    return isinstance(path_or_stream, str)


def os_file_get_path_from_stream(maybe_stream):
    """
    Try to get file path from given stream `stream`.

    :param maybe_stream: A file or file-like object
    :return: Path of given file or file-like object or None

    # >>> __file__ == get_path_from_stream(__file__)
    True
    # >>> __file__ == get_path_from_stream(open(__file__, 'r'))
    True
    # >>> strm = anyconfig.compat.StringIO()
    # >>> get_path_from_stream(strm) is None
    True
    """
    if os_folder_is_path(maybe_stream):
        return maybe_stream  # It's path.

    maybe_path = getattr(maybe_stream, "name", None)
    if maybe_path is not None:
        maybe_path = os.path.abspath(maybe_path)

    return maybe_path


def os_file_try_to_get_extension(path_or_strm):
    """
    Try to get file extension from given path or file object.
    :return: File extension or None
    """
    path = os_file_get_path_from_stream(path_or_strm)
    if path is None:
        return None

    return os_file_get_extension(path) or None


def os_file_are_same_file_types(paths):
    """
    Are given (maybe) file paths same type (extension) ?
    :param paths: A list of file path or file(-like) objects

    # >>> are_same_file_types([])
    False
    # >>> are_same_file_types(["a.conf"])
    True
    # >>> are_same_file_types(["a.yml", "b.json"])
    False
    # >>> strm = anyconfig.compat.StringIO()
    # >>> are_same_file_types(["a.yml", "b.yml", strm])
    False
    """
    if not paths:
        return False
    ext = os_file_try_to_get_extension(paths[0])
    if ext is None:
        return False

    return all(os_file_try_to_get_extension(p) == ext for p in paths[1:])


def os_file_norm_paths(paths, marker="*"):
    """
    :param paths:
        A glob path pattern string, or a list consists of path strings or glob
        path pattern strings or file objects
    :param marker: Glob marker character or string, e.g. '*'
    :return: List of path strings
    # >>> norm_paths([])
    []
    # >>> norm_paths("/usr/lib/a/b.conf /etc/a/b.conf /run/a/b.conf".split())
    ['/usr/lib/a/b.conf', '/etc/a/b.conf', '/run/a/b.conf']
    # >>> paths_s = os.path.join(os.path.dirname(__file__), "u*.py")
    # >>> ref = sglob(paths_s)
    # >>> ref = ["/etc/a.conf"] + ref
    # >>> assert norm_paths(["/etc/a.conf", paths_s]) == ref
    # >>> strm = anyconfig.compat.StringIO()
    # >>> assert norm_paths(["/etc/a.conf", strm]) == ["/etc/a.conf", strm]
    """

    def sglob(files_pattern):
        """
      glob.glob alternative of which results sorted always.
      """
        return sorted(glob.glob(files_pattern))

    def _norm_paths_itr(paths, marker="*"):
        """Iterator version of :func:`norm_paths`.
     """
        for path in paths:
            if os_folder_is_path(path):
                if marker in path:  # glob path pattern
                    for ppath in sglob(path):
                        yield ppath
                else:
                    yield path  # a simple file path
            else:  # A file or file-like object
                yield path

    if os_folder_is_path(paths) and marker in paths:
        return sglob(paths)

    return list(_norm_paths_itr(paths, marker=marker))


def os_file_mergeall(nfile, dir1, pattern1, deepness=2):
    ll = os_file_listall(dir1, pattern1, deepness)
    with open(nfile, mode="a", encoding="UTF-8") as nfile1:
        for l in ll[2]:
            txt = "\n\n\n\n" + os_file_gettext(l)
            nfile1.write(txt)
    nfile1.close()


def os_file_extracttext(output_file, dir1, pattern1="*.html", htmltag="p", deepness=2):
    """ Extract text from html """
    _ = deepness

    ll = os_file_listall(dir1, pattern1, 5)

    with open(output_file, mode="a", encoding="UTF-8") as output_file1:
        for l in ll[2]:
            page = os_file_gettext(l)
            soup = BeautifulSoup(page, "lxml")
            txt2 = " \n\n".join([p.text for p in soup.find_all(htmltag)])

        txt = "\n\n\n\n" + txt2.strip()
        output_file1.write(txt)


def os_path_append(p1, p2=None, p3=None, p4=None):
    sys.path.append(p1)
    if p2 is not None:
        sys.path.append(p2)
    if p3 is not None:
        sys.path.append(p3)
    if p4 is not None:
        sys.path.append(p4)


# WAIT BEFORE LAUNCH
def os_wait_cpu(priority=300, cpu_min=50):

    aux = psutil.cpu_percent()
    while aux > cpu_min:
        print("CPU:", aux, arrow.utcnow().to("Japan").format())
        time.sleep(priority)
        aux = psutil.cpu_percent()
        time.sleep(10)
        aux = 0.5 * (aux + psutil.cpu_percent())
    print("Starting script:", aux, arrow.utcnow().to("Japan").format())


def os_split_dir_file(dirfile):
    lkey = dirfile.split("/")
    if len(lkey) == 1:
        dir1 = ""
    else:
        dir1 = "/".join(lkey[:-1])
        dirfile = lkey[-1]
    return dir1, dirfile


def os_process_run(cmd_list, capture_output=False):
    """os_process_run
    
    Args:
         cmd_list: list ["program", "arg1", "arg2"]
         capture_output: bool
    """

    # cmd_list= os_path_norm(cmd_list)
    pipe = subprocess.PIPE
    stdout = subprocess.STDOUT
    proc = subprocess.Popen(
        cmd_list, stdout=pipe, stderr=stdout, shell=False
    )  # Always put to False

    if capture_output:
        stdout, stderr = proc.communicate()
        print("Console Msg: \n")
        print((str(stdout)))  # ,"utf-8"))
        print(("\nConsole Error: \n" + str(stderr)))
        #    return stdout, stderr, int(err_code)



# Python Interpreter
def py_importfromfile(modulename, dir1):
    # Import module from file:  (Although this has been deprecated in Python 3.4.)
    _ = modulename
    _ = dir1

    vv = a_get_pythonversion()
    if vv == 3:
        from importlib.machinery import SourceFileLoader

        foo = SourceFileLoader("module.name", "/path/to/file.py").load_module()
        foo.MyClass()
    elif vv == 2:
        foo = importlib.import_module("module.name", "/path/to/file.py")
        foo.MyClass()


def py_memorysize(o, ids, hint=" deep_getsizeof(df_pd, set()) "):
    """ deep_getsizeof(df_pd, set())
    Find the memory footprint of a Python object
    The sys.getsizeof function does a shallow size of only. It counts each
    object inside a container as pointer only regardless of how big it
    """
    from collections import Mapping, Container
    from sys import getsizeof

    _ = hint

    d = py_memorysize
    if id(o) in ids:
        return 0

    r = getsizeof(o)
    ids.add(id(o))

    if isinstance(o, str) or isinstance(0, str):
        r = r

    if isinstance(o, Mapping):
        r = r + sum(d(k, ids) + d(v, ids) for k, v in o.items())

    if isinstance(o, Container):
        r = r + sum(d(x, ids) for x in o)

    return r * 0.0000001


def save(obj, folder="/folder1/keyname", isabsolutpath=0):
    return py_save_obj(obj, folder=folder, isabsolutpath=isabsolutpath)


def load(folder="/folder1/keyname", isabsolutpath=0):
    return py_load_obj(folder=folder, isabsolutpath=isabsolutpath)



def py_save_obj(obj, folder="/folder1/keyname", isabsolutpath=0):
    if isabsolutpath == 0 and folder.find(".pkl") == -1:  # Local Path
        dir0, keyname = z_key_splitinto_dir_name(folder)
        os_folder_create(DIRCWD + "/aaserialize/" + dir0)
        dir1 = DIRCWD + "/aaserialize/" + dir0 + "/" + keyname + ".pkl"
    else:
        dir1 = folder

    with open(dir1, "wb") as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
    return dir1


def py_load_obj(folder="/folder1/keyname", isabsolutpath=0, encoding1="utf-8"):
    """def load_obj(name, encoding1='utf-8' ):
         with open('D:/_devs/Python01/aaserialize/' + name + '.pkl', 'rb') as f:
            return pickle.load(f, encoding=encoding1)
    """
    import pickle

    _ = encoding1

    if isabsolutpath == 0 and folder.find(".pkl") == -1:
        dir0, keyname = z_key_splitinto_dir_name(folder)
        os_folder_create(DIRCWD + "/aaserialize/" + dir0)
        dir1 = DIRCWD + "/aaserialize/" + dir0 + "/" + keyname + ".pkl"
    else:
        dir1 = folder

    with open(dir1, "rb") as f:
        return pickle.load(f)


def z_key_splitinto_dir_name(keyname):
    lkey = keyname.split("/")
    if len(lkey) == 1:
        dir1 = ""
    else:
        dir1 = "/".join(lkey[:-1])
        keyname = lkey[-1]
    return dir1, keyname


def os_config_setfile(dict_params, outfile, mode1="w+"):
    with open(outfile, mode=mode1) as f1:
        for key, item in dict_params.items():
            if isinstance(item, str) or isinstance(item, str):
                f1.write(str(key) + "= " + "'" + str(item) + "'" + " \n")
            else:
                f1.write(str(key) + "= " + str(item) + " \n")

    f1.close()
    print(outfile)


def os_config_getfile(file1):
    with open(file1, mode="r") as f1:
        ll = f1.readlines()

    for x in ll:
        print(x, end=" ")


# STRING-
def find_fuzzy(xstring, list_string):
    """ if xstring matches partially, add to the list   """
    return [xi for xi in list_string if xi.find(xstring) > -1]


def str_match_fuzzy(xstring, list_string):
    """ if any of list_strinf elt matches partially xstring """
    for xi in list_string:
        if xstring.find(xi) > -1:
            return True
    return False


def str_parse_stringcalendar(cal):
    """----------Parse Calendar  --------"""
    cal2 = cal.split("\n")
    cal3 = [x for x in cal2 if x != ""]
    import dateutil

    cal4 = []
    for x in cal3:
        i0 = x.find(":")
        cal4.append([datetime_toint(dateutil.parser.parse(x[:i0])), x[i0 + 1 :]])
    cal4 = np.array(cal4)
    cal5 = np.array(np_sortcol(cal4, 0), dtype=str)
    for x in cal5:
        print(x[0], ":", x[1].strip())
    return cal5


def str_make_unicode(input_str, errors="replace"):
    ttype = type(input_str)
    if ttype != str:
        input_str = input_str.decode("utf-8", errors=errors)
        return input_str
    else:
        return input_str


def str_empty_string_array(x, y=1):
    if y == 1:
        return ["" for _ in range(x)]
    else:
        return [["" for _ in range(0, x)] for _ in range(0, y)]


def str_empty_string_array_numpy(nx, ny=1):
    arr = np.empty((nx, ny), dtype=object)
    arr[:, :] = ""
    return arr


def str_isfloat(value):
    try:
        float(value)
        return True
    except ValueError:
        return False


def str_is_azchar(x):
    try:
        float(x)
        return True
    except ValueError:
        return False


def str_is_az09char(x):
    try:
        float(x)
        return True
    except ValueError:
        return False


def str_reindent(s, num_spaces):  # change indentation of multine string
    """
   if args:
       aux= name1+'.'+obj.__name__ +'('+ str(args) +')  \n' + str(inspect.getdoc(obj))
       aux= aux.replace('\n', '\n       ')
       aux= aux.rstrip()
       aux= aux + ' \n'
       wi( aux)
    """
    s = s.split("\n")
    s = [(num_spaces * " ") + line.lstrip() for line in s]
    s = "\n".join(s)
    return s


def str_split2(delimiters, string, maxsplit=0):  # Split into Sub-Sentence
    import re

    regex_pattern = "|".join(map(re.escape, delimiters))
    return re.split(regex_pattern, string, maxsplit)


def str_split_pattern(sep2, ll, maxsplit=0):  # Find Sentence Pattern
    import re

    _ = maxsplit

    regex_pat = "|".join(sep2)
    regex3 = re.compile("(" + regex_pat + r")|(?:(?!" + regex_pat + ").)*", re.S)
    # re.compile(r'(word1|word2|word3)|(?:(?!word1|word2|word3).)*', re.S)
    ll = regex3.sub(lambda m: m.group(1) if m.group(1) else "P", ll)
    return ll


def pd_str_isascii(x):
    try:
        x.decode("ascii")
        return True
    except UnicodeError:
        return False


def str_to_utf8(x):
    """ Do it before saving/output to external printer """
    return x.encode("utf-8")


def str_to_unicode(x, encoding="utf-8"):
    """ Do it First after Loading some text """
    if isinstance(x, str):
        if not isinstance(x, str):
            return str(x, encoding)
    else:
        return x


# LIST UTIL / Array
def np_minimize(fun_obj, x0=None, argext=(0, 0), bounds1=None, method="Powell"):
    if x0 is None:
        x0 = [0.0]

    if bounds1 is None:
        bounds1 = [(0.03, 0.20), (10, 150)]

    def penalty(vv):  # Constraints Penalty
        penalty = 0.0
        for i, x in enumerate(vv):
            penalty += 5000000 * (-min(x - bounds1[i][0], 0.0) + max(x - bounds1[i][1], 0.0))
        return penalty

    def loss(vv, argext):
        return fun_obj(vv, argext) + penalty(vv)

    res = sci.optimize.minimize(loss, x0, args=argext, method=method, bounds=bounds1, tol=0.001)
    return res



def np_remove_na_inf_2d(x):
    im, jm = np.shape(x)
    for i in range(0, im):
        for j in range(0, jm):
            if np.isnan(x[i, j]) or np.isinf(x[i, j]):
                x[i, j] = x[i - 1, j]
    return x


def np_addcolumn(arr, nbcol):
    sh = np.shape(arr)
    vv = np.zeros((sh[0], nbcol))
    arr2 = np.column_stack((arr, vv))
    return arr2


def np_addrow(arr, nbrow):
    sh = np.shape(arr)
    if len(sh) > 1:
        vv = np.zeros((nbrow, sh[1]))
        arr2 = np.row_stack((arr, vv))
        return arr2
    else:
        return np.append(arr, np.zeros(nbrow))


def np_int_tostr(i):
    if i < 10:
        return "00" + str(i)
    elif i < 100:
        return "0" + str(i)
    else:
        return str(i)


def np_dictordered_create():
    from collections import OrderedDict

    return OrderedDict()


def np_list_unique(seq):
    return list(set(seq))


def np_list_tofreqdict(l1, wweight=None):
    if wweight is None:
        wweight = []

    # Get list frequency
    dd = dict()
    if len(wweight) == 0:
        for x in l1:
            try:
                dd[x] += 1
            except IndexError:
                dd[x] = 1
        return dd
    else:
        for ii, x in enumerate(l1):
            try:
                dd[x] += wweight[ii]
            except IndexError:
                dd[x] = wweight[ii]
        return dd


# used to flatten a list or tupel [1,2[3,4],[5,[6,7]]] -> [1,2,3,4,5,6,7]
def np_list_flatten(seq):
    ret = []
    for elt in seq:
        t = type(elt)
        if t is tuple or t is list:
            for elt2 in np_list_flatten(elt):
                ret.append(elt2)
        else:
            ret.append(elt)
    return ret


def np_dict_tolist(dd, withkey=0):
    if withkey:
        return [[key, val] for key, val in list(dd.items())]
    else:
        return [val for _, val in list(dd.items())]


def np_dict_tostr_val(dd):
    return ",".join([str(val) for _, val in list(dd.items())])


def np_dict_tostr_key(dd):
    return ",".join([str(key) for key, _ in list(dd.items())])


def np_removelist(x0, xremove=None):
    if xremove is None:
        xremove = []

    xnew = []
    for x in x0:
        if np_findfirst(x, xremove) < 0:
            xnew.append(x)
    return xnew


def np_transform2d_int_1d(m2d, onlyhalf=False):
    _ = onlyhalf

    imax, jmax = np.shape(m2d)
    v1d = np.zeros((imax * jmax, 4))
    k = 0
    for i in range(0, imax):
        for j in range(i + 1, jmax):
            v1d[k, 0] = i
            v1d[k, 1] = j
            v1d[k, 2] = m2d[i, j]
            v1d[k, 3] = np.abs(m2d[i, j])
            k += 1
    v1d = v1d[v1d[:, 2] != 0]
    return np_sortbycol(v1d, 3, asc=False)


def np_mergelist(x0, x1):
    xnew = list(x0)
    for x in x1:
        xnew.append(x)
    return list(xnew)


def np_enumerate2(vec_1d):
    v2 = np.empty((len(vec_1d), 2))
    for k, x in enumerate(vec_1d):
        v2[k, 0] = k
        v2[k, 1] = x
    return v2


# Pivot Table from List data
def np_pivottable_count(mylist):
    mydict = {}.fromkeys(mylist, 0)
    for e in mylist:
        mydict[e] = mydict[e] + 1  # Map Reduce function
    ll2 = np_dict_tolist(mydict)
    ll2 = sorted(ll2, key=lambda x: int(x[1]), reverse=True)
    return ll2


def np_nan_helper(y):
    """ Input:  - y, 1d numpy array with possible NaNs
        Output - nans, logical indices of NaNs - index, a function, with signature
              indices= index(logical_indices),
              to convert logical indices of NaNs to 'equivalent' indices
    """
    return np.isnan(y), lambda z: z.nonzero()[0]


def np_interpolate_nan(y):
    nans, x = np_nan_helper(y)
    y[nans] = np.interp(x(nans), x(~nans), y[~nans])
    return y


def np_and1(x, y, x3=None, x4=None, x5=None, x6=None, x7=None, x8=None):
    if x8 is not None:
        return np.logical_and.reduce((x8, x7, x6, x5, x4, x3, x, y))
    if x7 is not None:
        return np.logical_and.reduce((x7, x6, x5, x4, x3, x, y))
    if x6 is not None:
        return np.logical_and.reduce((x6, x5, x4, x3, x, y))
    if x5 is not None:
        return np.logical_and.reduce((x5, x4, x3, x, y))
    if x4 is not None:
        return np.logical_and.reduce((x4, x3, x, y))
    if x3 is not None:
        return np.logical_and.reduce((x3, x, y))


def np_sortcol(arr, colid, asc=1):
    """ df.sort(['A', 'B'], ascending=[1, 0])  """
    df = pd.DataFrame(arr)
    arr = df.sort_values(colid, ascending=asc)
    return arr.values


def np_ma(vv, n):
    """Moving average """
    return np.convolve(vv, np.ones((n,)) / n)[(n - 1) :]


@jit(float32[:, :](float32[:, :]))
def np_cleanmatrix(m):
    m = np.nan_to_num(m)
    imax, jmax = np.shape(m)
    for i in range(0, imax):
        for j in range(0, jmax):
            if abs(m[i, j]) > 300000.0:
                m[i, j] = 0.0
    return m


def np_torecarray(arr, colname):
    return np.core.records.fromarrays(
        arr.T, names=",".join(colname), formats=",".join(["f8"] * np.shape(arr)[1])
    )


def np_sortbycolumn(arr, colid, asc=True):
    df = pd.DataFrame(arr)
    arr = df.sort_values(colid, ascending=asc)
    return arr.values


def np_sortbycol(arr, colid, asc=True):
    if len(np.shape(arr)) > 1:
        df = pd.DataFrame(arr)
        arr = df.sort_values(colid, ascending=asc)
        return arr.values
    else:
        return np.reshape(arr, (1, len(arr)))


# if colid==0 : return arr[np.argsort(arr[:])]
# else : return arr[np.argsort(arr[:, colid])]


def np_min_kpos(arr, kth):
    """ return kth mininimun """
    return np.partition(arr, kth - 1)[kth - 1]


def np_max_kpos(arr, kth):
    """ return kth mininimun """
    n = len(arr)
    return np.partition(arr, n - kth + 1)[n - kth + 1 - 1]



def find(item, vec):
    """return the index of the first occurence of item in vec"""
    for i in range(len(vec)):
        if item == vec[i]:
            return i
    return -1


def findnone(vec):
    """return the index of the first occurence of item in vec"""
    for i in range(len(vec)):
        if vec[i] is None:
            return i
    return -1


def findx(item, vec):
    """return the index of the first occurence of item in vec"""
    try:
        if type(vec) == list:
            i2 = vec.index(item)
        else:
            i = np.where(vec == item)[0]
            i2 = i[0] if len(i) > 0 else -1
    except IndexError:
        i2 = -1
    return i2


def finds(itemlist, vec):
    """return the index of the first occurence of item in vec"""
    idlist = []
    for x in itemlist:
        ix = -1
        for i in range(len(vec)):
            if x == vec[i]:
                idlist.append(i)
                ix = i
        if ix == -1:
            idlist.append(-1)
    if not idlist:
        return -1
    else:
        return idlist


def findhigher(x, vec):
    """return the index of the first occurence of item in vec"""
    for i in range(len(vec)):
        if vec[i] > x:
            return i
    return -1


def findlower(x, vec):
    """return the index of the first occurence of item in vec"""
    for i in range(len(vec)):
        if vec[i] < x:
            return i
    return -1


def np_find_minpos(values):
    min_index, min_value = min(enumerate(values), key=operator.itemgetter(1))
    return min_index, min_value


def np_find_maxpos(values):
    max_index, max_value = max(enumerate(values), key=operator.itemgetter(1))
    return max_index, max_value


def np_find_maxpos_2nd(numbers):
    count = 0
    m1 = m2 = float("-inf")
    i2 = None
    for i, x in enumerate(numbers):
        count += 1
        if x > m2:
            if x >= m1:
                m1, m2 = x, m1
            else:
                m2 = x
                i2 = i
    return i2, m2 if count >= 2 else None




def np_findlocalmin2(v, trig):
    n = len(v)
    v2 = np.zeros((n, 8))
    tmin, _ = np_find_minpos(v)
    if n < 3:
        max_index, max_value = np_find_minpos(v)
        v2 = [[max_index, max_value]]
        return v2
    else:
        for i, x in enumerate(v):
            if 0 < i < n - 1:
                if x < v[i - 1] and x < v[i + 1]:
                    v2[i, 0] = i
                    v2[i, 1] = x
        v2 = np_sortbycolumn(v2, 1, asc=False)

        # Classification of the Local min
        for k in range(0, len(v2)):
            if v2[k, 1] != 0.0:
                kmin = v2[k, 0]
                kminl = findlower(v2[k, 1], v[:kmin][::-1])  # Find same level of min
                kminr = findlower(v2[k, 1], v[kmin + 1 :])

                kminl = 0 if kminl == -1 else kmin - kminl
                kminr = n if kminr == -1 else kminr + kmin

                v2[k, 2] = np.abs(kminr - kminl)  # Range
                v2[k, 3] = np.abs(kmin - tmin)  # Range of the min After
                v2[k, 4] = 0  # Range of the min After
                v2[k, 5] = kmin - kminl
                v2[k, 6] = kminr - kmin
    v2 = v2[np.logical_and(v2[:, 5] > trig, v2[:, 6] > trig)]
    v2 = np_sortbycolumn(v2, 0, asc=True)
    return v2


def np_findlocalmax(v):
    n = len(v)
    v2 = np.zeros((n, 2))
    if n > 2:
        for i, x in enumerate(v):
            if 0 < i < n - 1:
                if x > v[i - 1] and x > v[i + 1]:
                    v2[i, 0] = i
                    v2[i, 1] = x
        v2 = np_sortbycolumn(v2, 1, asc=False)
        return v2
    else:
        max_index, max_value = np_find_maxpos(v)
        return [[max_index, max_value]]


def np_findlocalmin(v):
    n = len(v)
    v2 = np.zeros((n, 2))
    if n > 2:
        for i, x in enumerate(v):
            if 0 < i < n - 1:
                if x < v[i - 1] and x < v[i + 1]:
                    v2[i, 0] = i
                    v2[i, 1] = x

        v2 = np_sortbycolumn(v2, 0, asc=True)
        return v2
    else:

        max_index, max_value = np_find_minpos(v)
        return [[max_index, max_value]]


def np_stack(v1, v2=None, v3=None, v4=None, v5=None):
    sh = np.shape(v1)
    if sh[0] < sh[1]:
        v1 = np.row_stack((v1, v2))
        if v3 is not None:
            v1 = np.row_stack((v1, v3))
        if v4 is not None:
            v1 = np.row_stack((v1, v4))
        if v5 is not None:
            v1 = np.row_stack((v1, v5))
    else:
        v1 = np.column_stack((v1, v2))
        if v3 is not None:
            v1 = np.column_stack((v1, v3))
        if v4 is not None:
            v1 = np.column_stack((v1, v4))
        if v5 is not None:
            v1 = np.column_stack((v1, v5))

    return v1


def np_uniquerows(a):
    a = np.ascontiguousarray(a)
    unique_a = np.unique(a.view([("", a.dtype)] * a.shape[1]))
    return unique_a.view(a.dtype).reshape((unique_a.shape[0], a.shape[1]))


def np_remove_zeros(vv, axis1=1):
    return vv[~np.all(vv == 0, axis=axis1)]


def np_sort(vv):
    return vv[np.lexsort(np.transpose(vv)[::-1])]  # Sort the array by different column


def np_memory_array_adress(x):
    # This function returns the memory block address of an array.# b = a.copy(); id(b) == aid
    return x.__array_interface__["data"][0]


def np_pivotable_create(table, left, top, value):
    """
    Creates a cross-tab or pivot table from a normalised input table. Use this
    function to 'denormalize' a table of normalized records.

    * The table argument can be a list of dictionaries or a Table object.
    (http://aspn.activestate.com/ASPN/Cookbook/Python/Recipe/334621)
    * The left argument is a tuple of headings which are displayed down the
    left side of the new table.
    * The top argument is a tuple of headings which are displayed across the
    top of the new table.
    Tuples are used so that multiple element headings and columns can be used.

    E.g. To transform the list (listOfDicts):

    Name,   Year,  Value
    -----------------------
    'Simon', 2004, 32
    'Simon', 2005, 128
    'Russel', 2004, 64
    'Eric', 2004, 52
    'Russel', 2005, 32

    into the new list:

    'Name',   2004, 2005
    ------------------------
    'Simon',  32,     128
    'Russel',  64,     32
    'Eric',   52,     NA

    you would call pivot with the arguments:

    newList = pivot(listOfDicts, ('Name',), ('Year',), 'Value')

    """
    rs = {}
    ysort = []
    xsort = []
    for row in table:
        yaxis = tuple([row[c] for c in left])  # e.g. yaxis = ('Simon',)
        if yaxis not in ysort:
            ysort.append(yaxis)
        xaxis = tuple([row[c] for c in top])  # e.g. xaxis = ('2004',)
        if xaxis not in xsort:
            xsort.append(xaxis)
        try:
            rs[yaxis]
        except KeyError:
            rs[yaxis] = {}
        if xaxis not in rs[yaxis]:
            rs[yaxis][xaxis] = 0
        rs[yaxis][xaxis] += row[value]

    # In the following loop we take care of missing data,
    # e.g 'Eric' has a value in 2004 but not in 2005
    for key in rs:
        if len(rs[key]) > len(xsort):
            for var in xsort:
                if var not in list(rs[key].keys()):
                    rs[key][var] = ""

    headings = list(left)
    xsort.sort()
    headings.extend(xsort)

    t = []

    # The lists 'sortedkeys' and 'sortedvalues' make sure that
    # even if the field 'top' is unordered, data will be transposed correctly.
    # E.g. in the example above the table rows are not ordered by the year
    for left in ysort:
        row = list(left)
        sortedkeys = list(rs[left].keys())
        sortedkeys.sort()
        sortedvalues = list(map(rs[left].get, sortedkeys))
        row.extend(sortedvalues)
        t.append(dict(list(zip(headings, row))))
    return t


# PANDA UTIL


def pd_info(df, doreturn=1):
    df.info()
    dtype0 = df.dtypes.to_dict()
    for i in df.columns:
        print(i, dtype0[i], type(df[i].values[0]), df[i].values[0])
    if doreturn:
        return dtype0


def pd_info_memsize(df, memusage=0):
    df.info(memory_usage="deep")
    pd_info(df)
    if memusage == 1:
        return df.memory_usage().sum()


def pd_row_findlast(df, colid=0, emptyrowid=None):
    for ii, rr in df.iterrows():
        if rr[colid] is emptyrowid:
            return ii


# selection
def pd_row_select(df, **conditions):
    """Select rows from a df according to conditions
    pdselect(data, a=2, b__lt=3) __gt __ge __lte  __in  __not_in
    will select all rows where 'a' is 2 and 'b' is less than 3
    """
    if type(df) == pd.Series:
        df = pd.DataFrame({"value": df})
    for c, value in list(conditions.items()):
        if c in df.columns:
            c = df[c] == value
        elif c.endswith("__neq") or c.endswith("__not_eq"):
            if c.endswith("__neq"):
                c = c[: -len("__neq")]
            elif c.endswith("__not_eq"):
                c = c[: -len("__not_eq")]
            c = df[c] != value
        elif c.endswith("__gt"):
            c = c[: -len("__gt")]
            c = df[c] > value
        elif c.endswith("__ge"):
            c = c[: -len("__ge")]
            c = df[c] >= value
        elif c.endswith("__gte"):
            c = c[: -len("__gte")]
            c = df[c] >= value
        elif c.endswith("__lt"):
            c = c[: -len("__lt")]
            c = df[c] < value
        elif c.endswith("__le"):
            c = c[: -len("__le")]
            c = df[c] <= value
        elif c.endswith("__lte"):
            c = c[: -len("__lte")]
            c = df[c] <= value
        elif c.endswith("__in"):
            c = c[: -len("__in")]
            c = np.in1d(df[c], value)
        elif c.endswith("__not_in"):
            c = c[: -len("__not_in")]
            c = np.in1d(df[c], value, invert=True)
        else:
            raise ValueError("Cannot process condition '{}'".format(c))
        df = df[c]
    return df


def pd_csv_randomread(filename, nsample=10000, filemaxline=-1, dtype=None):
    if filemaxline == -1:
        n = sum(1 for _ in open(filename)) - 1  # number of records in file (excludes header)
    else:
        n = filemaxline
    skip = np.sort(
        np.random.randint(1, n + 1, n - nsample)
    )  # the 0-indexed header will not be included in the skip list
    df = pd.read_csv(filename, skiprows=skip, dtype=dtype)
    return df


# Creation
def pd_array_todataframe(array, colname=None, index1=None, dotranspose=False):
    sh = np.shape(array)
    if len(sh) > 1:
        if sh[0] < sh[1] and dotranspose:  # masset x time , need Transpose
            return pd.DataFrame(data=array.T, index=index1, columns=colname)
        else:
            return pd.DataFrame(data=array, index=index1, columns=colname)
    else:  # 1d vector
        return pd.DataFrame(data=np.array(array).reshape(-1, 1), index=index1, columns=colname)


def pd_dataframe_toarray(df):
    col1 = df.index
    array1 = df.reset_index().values[1:, :]
    column_name = df.columns
    return column_name, col1, array1


def pd_createdf(array1, col1=None, idx1=None):
    return pd.DataFrame(data=array1, index=idx1, columns=col1)


def pd_create_colmapdict_nametoint(df):
    """ 'close' ---> 5    """
    col = df.columns.values
    dict1 = {}
    for k, x in enumerate(col):
        dict1[x] = k
    return dict1


# Extract
def pd_extract_col_idx_val(df):
    return df.columns.values, df.index.values, df.values


def pd_extract_col_uniquevalue_tocsv(df, colname="", csvfile=""):
    """ Write one column into a file   """
    a = df[colname].unique()
    a = np.array(a)
    pd.DataFrame(a, columns=[colname]).to_csv(csvfile)
    print(csvfile)


def pd_split_col_idx_val(df):
    return df.columns.values, df.index.values, df.values


def pd_splitdf_inlist(df, colid, type1="dict"):
    """ Split df into dictionnary of dict/list """
    unique_names = df.sym.unique()
    if type1 == "dict":
        df_dict = {elem: pd.DataFrame for elem in unique_names}
        for key in list(df_dict.keys()):
            df_dict[key] = df[df[colid] == key]
        return df_dict

    if type1 == "list":
        l1 = []
        for key in unique_names:
            l1.append(df[df[colid] == key])
        return l1


def pd_find(df, regex_pattern="*", col_restrict=None, isnumeric=False, doreturnposition=False):
    """ Find string / numeric values inside df columns, return position where found
     col_restrict : restrict to these columns """
    if col_restrict is None:
        col_restrict = []

    dtype0 = df.dtypes.to_dict()
    col0 = df.columns if col_restrict == [] else col_restrict

    mask = None
    if not isnumeric:  # object string columns
        colx = [col for col in col0 if str(dtype0[col]) == "object"]
        print(("Searching Cols: " + str(colx)))
        for i, coli in enumerate(colx):
            dfm = df[coli].str.contains(regex_pattern, na=False, regex=True)
            if i == 0:
                mask = dfm
            else:
                mask = np.column_stack((mask, dfm))

    else:
        numval = regex_pattern
        colx = [
            col
            for col in col0
            if str(dtype0[col]).find("float") > -1 or str(dtype0[col]).find("int") > -1
        ]
        print(("Searching Cols: " + str(colx)))
        for i, coli in enumerate(colx):
            dfm = (df[coli] == numval).values  # df[col].loc[ df[col]== numval  ]
            if i == 0:
                mask = dfm
            else:
                mask = np.column_stack((mask, dfm))

    # print mask
    if len(mask.shape) < 2:
        mask = mask.values.reshape(-1, 1)

    gc.collect()
    if doreturnposition:
        locate = np_dictordered_create()  # Position in Dict_Column --> Indice_j
        for j in range(0, mask.shape[1]):
            pos_tempj = np.array([i for i in range(0, mask.shape[0]) if mask[i, j]], dtype=np.int32)
            locate[colx[j]] = pos_tempj

        # locate= np.array([ (colx[j], i) for i in xrange(0,mask.shape[0]) for j in
        #     xrange(0, mask.shape[1])  if mask[i,j] ])
        return df.loc[mask.any(axis=1)], locate
    else:
        return df.loc[mask.any(axis=1)]


# dtypes
"""
def pd_dtypes_tocategory(df, columns=[], targetype='category'):
   for col in columns : df[col]= df[col].astype(targetype)
   return df
"""


def pd_dtypes_totype2(df, columns=(), targetype="category"):
    for col in columns:
        df[col] = df[col].astype(targetype)
    return df


def pd_dtypes(df, returnasdict=0):
    from collections import OrderedDict

    dtype0 = OrderedDict(df.dtypes.apply(lambda x: x.name))
    ss = """{ """
    for i, col in enumerate(df.columns.values):
        ss += "'" + col + "':" + "'" + dtype0[col] + "', "
        if i % 3 == 0 and i > -1:
            ss += "\n"
    ss = ss[0:-2] + " }"

    if returnasdict:
        return eval(ss)
    print(ss)
    print(
        """\n df.astype(typedict)  Pandas 'object' : 'category', 'unicode' , 'str'  'boolean',
        float16, float32, int8, int16, int32,uint8, uint16, uint32 """
    )


def pd_df_todict2(df, colkey="table", excludekey=("",), onlyfirstelt=True):
    df = df.drop_duplicates(colkey).reset_index(level=0, drop=True)
    dict0 = {}
    for i in range(0, len(df)):
        id0 = df.iloc[i, 0]
        val0 = df.iloc[i, 1]
        if id0 not in excludekey:
            dict0.setdefault(id0, [])
            if onlyfirstelt:
                dict0[id0] = val0
            else:
                dict0[id0].append(val0)
    return dict0


def pd_df_todict(df, colkey="machine_code", colval="adress"):
    dict0 = {}
    for ii, row in df.iterrows():
        try:
            dict0[row[colkey]] = row[colval]
        except IndexError:
            pass

    return dict0


def pd_col_addfrom_dfmap(
    df, dfmap, colkey, colval, df_colused, df_colnew, exceptval=-1, inplace=True
):
    """ Add new columns based on df_map:  In Place Modification of df
    df:     Dataframe of transactions.
    dfmap:  FSMaster Dataframe
      colkey: colum used for dict key.  machine_code
      colval: colum used for dict val.  adress

    df_colused  :     "machine_code"
    exception val:  -1 or ''
  """
    map_dict = pd_df_todict(dfmap, colkey=colkey, colval=colval)

    def map_dict_fun(rowi):
        try:
            return map_dict[rowi[df_colused]]
        except KeyError:
            return exceptval

    df[df_colnew] = df.apply(lambda x: map_dict_fun(x), axis=1)

    if inplace:
        return None
    else:
        return df


"""
def pd_dtypes_getdict(df=None, csvfile=None) :
   if df is not None :   return df.dtypes.to_dict()
   elif csvfile is not None :
      df= pd.read_csv(csvfile, nrows= 1000)
      return df.dtypes.to_dict()


def pd_dtypes_getblaze(df1) :
 from collections import OrderedDict
 x= str(OrderedDict(df1.dtypes.apply(lambda x: x.name)))
 x=x.replace("',", "':")
 x=x.replace("(", "")
 x=x.replace(")", "")
 x=x.replace("OrderedDict[", "{")
 x=x.replace("]", "}")
 print(" string 5char: |S5 object in Pandas,  object_bool, string_, unicode
    float16, float32, float64, int8, int16, int32, int64, uint8, uint16, uint32, uint64")
 return x
"""

"""
 # return df1.dtypes.apply(lambda x: x.name).to_dict()
 from collections import OrderedDict
 ds=OrderedDict()
 for i,x in enumerate(df1.columns.values) :
   ds[x]=  df1.dtypes[i].name
 print ds
"""


# Apply / Transform df
def pd_applyfun_col(df, newcol, ff, use_colname="all/[colname]"):
    """ use all Columns to compute values """
    if use_colname == "all/[colname]":
        df[newcol] = ff(df.values)
    else:
        df[newcol] = ff(df[use_colname].values)
    return df


"""
def pd_cleanquote(q):
 col= q.columns.values
 for kid in col:
   if kid not in ['date', 'day','month','year'] :
      q[kid]= pd.to_numeric(q[kid], errors='coerce').values  #Put NA on string

 q= q.fillna(method='pad')
 return q
"""


def pd_date_intersection(qlist):
    date0 = set(qlist[0]["date"].values)
    for qi in qlist:
        qs = set(qi["date"].values)
        date0 = set.intersection(date0, qs)
    date0 = list(date0)
    date0 = sorted(date0)
    return date0


def pd_is_categorical(z):
    if isinstance(z, pd.Categorical):
        return True
    try:
        return isinstance(z.values, pd.Categorical)
    except TypeError:
        return False


def pd_str_encoding_change(df, cols, fromenc="iso-8859-1", toenc="utf-8"):
    #  Western European: 'cp1252'
    for col in cols:
        df[col] = df[col].str.decode(fromenc).str.encode(toenc)
    return df


def pd_str_unicode_tostr(df, targetype=str):
    """
 https://www.azavea.com/blog/2014/03/24/solving-unicode-problems-in-python-2-7/
 Nearly every Unicode problem can be solved by the proper application of these tools;
 they will help you build an airlock to keep the inside of your code nice and clean:

encode(): Gets you from Unicode -> bytes
decode(): Gets you from bytes -> Unicode
codecs.open(encoding="utf-8"): Read and write files directly to/from Unicode (you can use any
encoding,
 not just utf-8, but utf-8 is most common).
u": Makes your string literals into Unicode objects rather than byte sequences.
Warning: Don't use encode() on bytes or decode() on Unicode objects

# >>> uni_greeting % utf8_name
Traceback (most recent call last):
 File "<stdin>", line 1, in <module>
UnicodeDecodeError: 'ascii' codec can't decode byte 0xc3 in position 3: ordinal not in range(128)
# Solution:
# >>> uni_greeting % utf8_name.decode('utf-8')
u'Hi, my name is Josxe9.'

 """
    _ = targetype

    return pd_dtypes_type1_totype2(df, fromtype=str, targetype=str)


def pd_dtypes_type1_totype2(df, fromtype=str, targetype=str):
    for ii in df.columns:
        if isinstance(df[ii].values[0], fromtype):
            df[ii] = df[ii].astype(targetype)
    return df


# ----Insert/update col row  -----------------------------------------
def pd_resetindex(df):
    df.index = list(np.arange(0, len(df.index)))
    return df


def pd_insertdatecol(df, col, format1="%Y-%m-%d %H:%M:%S:%f"):
    df[col] = df[col].apply(lambda x: date_nowtime(x, format1=format1))
    return df


def pd_replacevalues(df, matrix):
    """ Matrix replaces df.values  """
    imax, jmax = np.shape(matrix)
    colname = df.columns.values
    for j in jmax:
        df.loc[colname[j]] = matrix[:, j]

    return df


def pd_removerow(df, row_list_index=(23, 45)):
    return df.drop(row_list_index)


def pd_removecol(df1, name1):
    return df1.drop(name1, axis=1)


def pd_insertrow(df, rowval, index1=None, isreset=1):
    _ = isreset

    df2 = pd_array_todataframe(rowval, df.columns.values, index1)
    df = df.append(df2, ignore_index=True)
    # if isreset : df.reset_index(inplace=True)
    return df


# ---- h5 In / Out  ------------------------------------------------
def pd_h5_cleanbeforesave(df):
    """Clean Column type before Saving in HDFS: Unicode, Datetime  """
    # Unicode String :
    df = pd_resetindex(df)  # Reset Index 0 to 100000
    df = pd_str_unicode_tostr(df, targetype=str)

    """
   for col in  ['date'] :
   # df_pd[col] = df_pd[col].astype(str)
   df_pd[col] = df_pd[col].apply(lambda x: x.encode('utf-8').strip())

   df_pd.to_hdf('test.h5','df',format='table',mode='w',data_columns=True,encoding='latin1')

   """
    return df


def pd_h5_addtable(df, tablename, dbfile="F:\temp_pandas.h5"):
    store = pd.HDFStore(dbfile)
    if find(tablename, list(store.keys())) > 0:
        # tablename=tablename + '_1';
        print("Table Exist, change table name")
    else:
        store.append(tablename, df)
        store.close()


def pd_h5_tableinfo(filenameh5, table):
    store = pd.HDFStore(filenameh5)
    return store.get_storer(table).table


def pd_h5_dumpinfo(dbfile=r"E:\_data\stock\intraday_google.h5"):
    store = pd.HDFStore(dbfile)
    extract = []
    errsym = []
    for symbol in list(store.keys()):
        try:
            df = pd.DataFrame(pd.read_hdf(dbfile, symbol))
            extract.append(
                [
                    symbol[1:],
                    df.shape[1],
                    df.shape[0],
                    datetime_tostring(df.index.values[0]),
                    datetime_tostring(df.index.values[-1]),
                ]
            )

        except IndexError:
            errsym.append(symbol)
    return np.array(extract), errsym


def pd_h5_save(df, filenameh5="E:/_data/_data_outlier.h5", key="data"):
    """ File is release after saving it"""
    store = pd.HDFStore(filenameh5)
    store.append(key, df)
    store.close()


def pd_h5_load(
    filenameh5="E:/_data/_data_outlier.h5",
    table_id="data",
    exportype="pandas",
    rowstart=-1,
    rowend=-1,
    cols=(),
):
    _ = cols

    if rowend == -1:
        df = pd.read_hdf(filenameh5, table_id)
    else:
        df = pd.DataFrame(pd.read_hdf(filenameh5, table_id, start=rowstart, end=rowend))
    if exportype == "pandas":
        return df
    elif exportype == "numpy":
        return df.values


def pd_h5_fromcsv_tohdfs(
    dircsv="dir1/dir2/",
    filepattern="*.csv",
    tofilehdfs="file1.h5",
    tablename="df",
    col_category=(),
    dtype0=None,
    encoding="utf-8",
    chunksize=2000000,
    mode="a",
    form="table",
    complib=None,
):
    _ = encoding

    csvlist = os_file_listall(dircsv, filepattern)
    csvlist = csvlist[2]  # 2: Full_path + filename

    store = pd.HDFStore(tofilehdfs)
    for ii, tablei_file in enumerate(csvlist):

        # Inference of Type, String size from top 1000 records......
        if ii == 0:
            if dtype0 is None:
                df_i = pd.read_csv(
                    tablei_file, nrows=1000, sep=","
                )  # Use Top 1000 to estimate size....
                dtype0 = df_i.dtypes.to_dict()
                # col_list = []
                # for col, x  in dtype0.items():
                #   if x == np.dtype('O') :    #Object == date, string, need to convert to
                #                              #string....
                #      col_list.append(col)
                # df_i[col] =    df_i[col].map(lambda x:  str(str(x).encode(encoding)))
                # max_size[col]= max(15, df_i[col].str.len().max())

        # ISSUE: DO NOT USE encoding='utf-8' when reading the Japanese Character.....
        list01 = pd.read_csv(
            tablei_file, chunksize=chunksize, dtype=dtype0, sep=","
        )  # , encoding=encoding)
        for k, df_i in enumerate(list01):
            print(".", end=" ")
            for col in col_category:
                df_i[col] = df_i[col].astype("category")

            # for col in col_list :
            # df_i[col] = df_i[col].map(lambda x:  str(str(x).encode(encoding)))
            store.append(
                tablename, df_i, mode=mode, format=form, complib=complib
            )  # ,  min_itemsize=max_size)

    store.close()
    del store
    print("\n")
    return os_file_exist(tofilehdfs)


def pd_np_toh5file(numpyarr, fileout="file.h5", table1="data"):
    pddf = pd.DataFrame(numpyarr)
    st = pd.HDFStore(fileout)
    st.append(table1, pddf)
    del pddf


def date_allinfo():
    """

https://aboutsimon.com/blog/2016/08/04/datetime-vs-Arrow-vs-Pendulum-vs-Delorean-vs-udatetime.html


   """


def datetime_tostring(datelist1):
    if isinstance(datelist1, datetime.date):
        return datelist1.strftime("%Y%m%d")
    if isinstance(datelist1, np.datetime64):
        t = pd.to_datetime(str(datelist1))
        return t.strftime("%Y%m%d")

    date2 = []
    for t in datelist1:
        date2.append(t.strftime("%Y%m%d"))
    return date2


def date_remove_bdays(from_date, add_days):
    isint1 = isint(from_date)
    if isint1:
        from_date = dateint_todatetime(from_date)
    business_days_to_add = add_days
    current_date = from_date
    while business_days_to_add < 0:
        current_date += datetime.timedelta(days=-1)
        weekday = current_date.weekday()
        if weekday >= 5:  # sunday = 6
            continue
        business_days_to_add += 1
    if isint1:
        return datetime_toint(current_date)
    else:
        return current_date


def date_add_bdays(from_date, add_days):
    isint1 = isint(from_date)
    if isint1:
        from_date = dateint_todatetime(from_date)
    business_days_to_add = add_days
    current_date = from_date
    while business_days_to_add > 0:
        current_date += datetime.timedelta(days=1)
        weekday = current_date.weekday()
        if weekday >= 5:  # sunday = 6
            continue
        business_days_to_add -= 1
    if isint1:
        return datetime_toint(current_date)
    else:
        return current_date


def datenumpy_todatetime(tt, islocaltime=True):
    #  http://stackoverflow.com/questions/29753060/how-to-convert-numpy-datetime64-into-datetime
    if type(tt) == np.datetime64:
        if islocaltime:
            return datetime.datetime.fromtimestamp(tt.astype("O") / 1e9)
        else:
            return datetime.datetime.utcfromtimestamp(tt.astype("O") / 1e9)
    elif type(tt[0]) == np.datetime64:
        if islocaltime:
            v = [datetime.datetime.fromtimestamp(t.astype("O") / 1e9) for t in tt]
        else:
            v = [datetime.datetime.utcfromtimestamp(t.astype("O") / 1e9) for t in tt]
        return v
    else:
        return tt  # datetime case


def datetime_tonumpydate(t, islocaltime=True):
    #  http://stackoverflow.com/questions/29753060/how-to-convert-numpy-datetime64-into-datetime
    _ = islocaltime
    return np.datetime64(t)


def datestring_todatetime(datelist1, format1="%Y%m%d"):
    _ = format1

    if isinstance(datelist1, str):
        return parser.parse(datelist1)
    date2 = []
    for s in datelist1:
        date2.append(parser.parse(s))
        # date2.append(datetime.datetime.strptime(s, format1))
    return date2


def datetime_toint(datelist1):
    if isinstance(datelist1, datetime.date):
        return int(datelist1.strftime("%Y%m%d"))
    date2 = []
    for t in datelist1:
        date2.append(int(t.strftime("%Y%m%d")))
    return date2


def date_holiday():
    """
   https://jakevdp.github.io/blog/2015/07/23/learning-seattles-work-habits-from-bicycle-counts/

from pandas.tseries.holiday import USFederalHolidayCalendar
cal = USFederalHolidayCalendar()
holidays = cal.holidays('2012', '2016', return_name=True)
holidays.head()

holidays_all = pd.concat([holidays, "Day Before " + holidays.shift(-1, 'D'),  "Day After "
+ holidays.shift(1, 'D')])
holidays_all = holidays_all.sort_index()
holidays_all.head()

from pandas.tseries.offsets import CustomBusinessDay
from pandas.tseries.holiday import USFederalHolidayCalendar
bday_us = CustomBusinessDay(calendar=USFederalHolidayCalendar())
dateref[-1] - bday_us- bday_us

   """


def date_add_bday(dint, nbday, country="us"):
    d = dateint_todatetime(dint)

    if country == "us":
        from pandas.tseries.offsets import CustomBusinessDay
        from pandas.tseries.holiday import USFederalHolidayCalendar

        bday_us = CustomBusinessDay(calendar=USFederalHolidayCalendar())
        d = d + bday_us * nbday
    else:
        d = d + pd.tseries.offsets.BDay(nbday)

    return datetime_toint(d)


def dateint_todatetime(datelist1):
    if isinstance(datelist1, int):
        return parser.parse(str(datelist1))
    date2 = []
    for s in datelist1:
        date2.append(parser.parse(str(s)))
        # date2.append(datetime.datetime.strptime(s, format1))
    return date2


def date_diffinday(intdate1, intdate2):
    dt = dateint_todatetime(intdate2) - dateint_todatetime(intdate1)
    return dt.days


def date_diffinbday(intd2, intd1):
    d1 = dateint_todatetime(intd1)
    d2 = dateint_todatetime(intd2)
    d1 = d1.date()
    d2 = d2.date()

    return np.busday_count(d1, d2)


def date_gencalendar(start="2010-01-01", end="2010-01-15", country="us"):
    from pandas.tseries.holiday import USFederalHolidayCalendar
    from pandas.tseries.offsets import CustomBusinessDay

    _ = country

    us_bd = CustomBusinessDay(calendar=USFederalHolidayCalendar())
    return np.array(pd.DatetimeIndex(start=start, end=end, freq=us_bd))


def date_finddateid(date1, dateref):
    i = np_findfirst(date1, dateref)
    if i == -1:
        i = np_findfirst(date1 + 1, dateref)
    if i == -1:
        i = np_findfirst(date1 - 1, dateref)
    if i == -1:
        i = np_findfirst(date1 + 2, dateref)
    if i == -1:
        i = np_findfirst(date1 - 2, dateref)
    if i == -1:
        i = np_findfirst(date1 + 3, dateref)
    if i == -1:
        i = np_findfirst(date1 - 3, dateref)
    if i == -1:
        i = np_findfirst(date1 + 5, dateref)
    if i == -1:
        i = np_findfirst(date1 - 5, dateref)
    if i == -1:
        i = np_findfirst(date1 + 7, dateref)
    if i == -1:
        i = np_findfirst(date1 - 7, dateref)
    return i


def datestring_toint(datelist1):
    if isinstance(datelist1, str):
        return int(datelist1)
    date2 = []
    for s in datelist1:
        date2.append(int(s))
    return date2


def date_now(i=0):
    from datetime import datetime

    d = datetime.now()
    if i > 0:
        d = date_add_bdays(d, i)
    else:
        d = date_remove_bdays(d, i)
    return str(datetime_toint(d))


def date_nowtime(type1="str", format1="%Y-%m-%d %H:%M:%S:%f"):
    """ str / stamp /  """
    from datetime import datetime

    # d= datetime.now()
    d = datetime.today()  # today = datetime.today().strftime('%Y%m%d_%H%M%S%f')
    if type1 == "str":
        return d.strftime(format1)
    elif type1 == "stamp":
        return d.strftime("%Y%m%d_%H%M%S%f")
    else:
        return d


def date_generatedatetime(start="20100101", nbday=10, end=""):
    from dateutil.rrule import DAILY, rrule, MO, TU, WE, TH, FR

    start = datestring_todatetime(start)
    if end == "":
        end = date_add_bdays(start, nbday - 1)  # + datetime.timedelta(days=nbday)
    date_list = list(rrule(DAILY, dtstart=start, until=end, byweekday=(MO, TU, WE, TH, FR)))

    return np.array(date_list)


# Utilities for Numerical Calc
def np_numexpr_vec_calc(
    filename, expr, i0=0, imax=1000, fileout=r"E:\_data\_QUASI_SOBOL_gaussian_xx3.h5"
):
    r""" New= xx*xx  over very large series
 #numexpr_vect_calc(filename, 0, imax=16384*4096, "xx*xx", 'E:\_data\_QUASI_SOBOL_gaussian_xx3.h5'):
"""
    pdframe = pd.DataFrame(pd.read_hdf(filename, "data", start=i0, stop=imax))  # from file
    del pdframe  # to numpy vector
    xx = ne.evaluate(expr)
    pdf = pd.DataFrame(xx)
    del xx
    # filexx3=   'E:\_data\_QUASI_SOBOL_gaussian_xx3.h5'
    store = pd.HDFStore(fileout)
    store.append("data", pdf)
    del pdf


def np_numexpr_tohdfs(
    filename, expr, i0=0, imax=1000, fileout=r"E:\_data\_QUASI_SOBOL_gaussian_xx3.h5"
):
    pdframe = pd.DataFrame(pd.read_hdf(filename, "data", start=i0, stop=imax))  # from file
    del pdframe
    xx = ne.evaluate(expr)
    pdf = pd.DataFrame(xx)
    del xx  # filexx3=   'E:\_data\_QUASI_SOBOL_gaussian_xx3.h5'
    store = pd.HDFStore(fileout)
    store.append("data", pdf)
    del pdf


# numexpr_vect_calc(filename, 0, imax=16384*4096, "xx*xx", 'E:\_data\_QUASI_SOBOL_gaussian_xx3.h5'):


# yy1= getrandom_tonumpy('E:\_data\_QUASI_SOBOL_gaussian_xx2.h5', 16384, 4096)
# ----------------------------------------------------------------------------


# Statistics
def np_comoment(xx, yy, nsample, kx, ky):
    #   cx= ne.evaluate("sum(xx)") /  (nsample);   cy= ne.evaluate("sum( yy)")  /  (nsample)
    #   cxy= ne.evaluate("sum((xx-cx)**kx * (yy-cy)**ky)") / (nsample)
    _ = xx
    _ = yy
    _ = kx
    _ = ky

    cxy = ne.evaluate("sum((xx)**kx * (yy)**ky)") / nsample
    return cxy


def np_acf(data):
    # Autocorrelation
    n = len(data)
    mean = np.mean(data)
    c0 = np.sum((data - mean) ** 2) / float(n)

    def r(h):
        acf_lag = ((data[: n - h] - mean) * (data[h:] - mean)).sum() / float(n) / c0
        return acf_lag

    x = np.arange(n)  # Avoiding lag 0 calculation
    acf_coeffs = np.asarray(list(map(r, x)))
    return acf_coeffs



def date_getspecificdate(
    datelist,
    datetype1="yearend",
    outputype1="intdate",
    includelastdate=True,
    includefirstdate=False,
):
    _ = includefirstdate

    vec2 = []

    if isint(datelist[0]):
        datelist = dateint_todatetime(datelist)

    t0 = datelist[0]
    if datetype1 == "monthend":
        for i, t in enumerate(datelist):
            #      print(datetime_tostring([t0, t]))
            if t.month != t0.month:
                vec2.append([i - 1, t0])
                # month has change
            t0 = t

    if datetype1 == "2monthend":
        for i, t in enumerate(datelist):
            if t.month != t0.month and np.mod(t0.month, 2) == 0:
                vec2.append([i - 1, t0])
                # month has change
            t0 = t

    if datetype1 == "3monthend":
        for i, t in enumerate(datelist):
            if t.month != t0.month and np.mod(t0.month, 3) == 0:
                vec2.append([i - 1, t0])
                # month has change
            t0 = t

    if datetype1 == "4monthend":
        for i, t in enumerate(datelist):
            if t.month != t0.month and np.mod(t0.month, 4) == 0:
                vec2.append([i - 1, t0])
                # month has change
            t0 = t

    if datetype1 == "6monthend":
        for i, t in enumerate(datelist):
            if t.month != t0.month and np.mod(t0.month, 6) == 0:
                vec2.append([i - 1, t0])
                # month has change
            t0 = t

    if datetype1 == "monthstart":
        for i, t in enumerate(datelist):
            if t.month != t0.month:
                vec2.append([i, t])
                # month has change
            t0 = t

    if datetype1 == "yearstart":
        vec2.append([0, t0])
        for i, t in enumerate(datelist):
            if t.year != t0.year:
                vec2.append([i, t])
                # month has change
            t0 = t

    if datetype1 == "yearend":
        for i, t in enumerate(datelist):
            if t.year != t0.year:
                vec2.append([i - 1, t0])
                # month has change
            t0 = t

    if includelastdate:
        vec2.append([len(datelist) - 3, datelist[-1]])

    if outputype1 == "intdate":
        vec2 = np.array(vec2)
        vec2 = np.array(vec2[:, 0], dtype="int")
        return vec2
    else:
        return np.array(vec2)


def py_exception_print():
    import linecache

    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    lineno = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, lineno, f.f_globals)
    print('EXCEPTION IN ({}, LINE {} "{}"): {}'.format(filename, lineno, line.strip(), exc_obj))


def py_log_write(logfile, prefix):
    ###########################################################################
    # logfile =     DIRCWD + '/aapackage/'+ 'ztest_all.txt';
    print(logfile)
    datenow = arrow.utcnow().to("Japan").format("YYYYMMDDHHmm")
    unique_id = (
        prefix + "_" + datenow + "_" + str(np.random.randint(10 ** 5, 10 ** 6, dtype="int64"))
    )
    sys.stdout = open(logfile, "a")
    print(
        "\n\n"
        + unique_id
        + " ###################### Start:"
        + arrow.utcnow().to("Japan").format()
        + "###########################"
    )
    sys.stdout.flush()
    print(os)
    return unique_id
    ##############################################################################


# UNIT TEST
if __name__ == "__main__":
    import argparse

    ppa = argparse.ArgumentParser()  # Command Line input
    ppa.add_argument("--do", type=str, default="action", help="test / test02")
    arg = ppa.parse_args()

    if arg.do == "test":
        print(__file__, DIRCWD)
        try:
            unique_id = py_log_write(DIRCWD + "/aapackage/ztest_log_all.txt", "util")

            #############################################################################

            print("")
            # a_info_system()
            isanaconda()
            date_allinfo()

            vv = np.random.rand(1, 10)
            mm = np.random.rand(100, 5)
            df1 = pd.DataFrame(mm, columns=["aa", "bb", "c", "d", "e"])

            # pd_createdf(mm, ["aa", "bb", 'c', 'd', 'e'],  )
            print(np_sort(vv))

            save(df1, "ztest_df")
            df2 = load("ztest_df")

            #############################################################################
            print(
                "\n\n"
                + unique_id
                + " ###################### end:"
                + arrow.utcnow().to("japan").format()
                + "###########################"
            )
            sys.stdout.flush()
        except Exception as e:
            print(e)
