# -*- coding: utf-8 -*-
"""
 cli_codesource --do    --module jedi

 
--do  module_signature_write(arg.module)
--do module_unitest_write(module_name= arg.module)



"""
from __future__ import absolute_import, division, print_function, unicode_literals

import ast
import fnmatch
import inspect
import math
import operator
import os
import pydoc
import re
import sys
from builtins import int, open, range, str, zip
from collections import OrderedDict
from importlib import import_module
from pkgutil import walk_packages

import pandas as pd

import regex
####################################################################################################





#######Github Helpers ########################################################################################
def os_folder_create(directory):
    DIR0 = os.getcwd()
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.chdir(DIR0)


def code_search_github(
    keywords=None,
    outputfolder="",
    browser="",
    login="",
    password="",
    page_start=1,
    page_end=1,
    isreturn_df=0,
    iswrite_df=1,
    isdownload_file=1,
    isdebug=0,
    outputfile="df_github_codesearch_01.csv",
    FILTER=1,
    CFG=None,
):
    """  pip install selenium  --no-deps
 #df= github_search_source_code(keywords= ["import jedi",   "jedi.Script(" ], outputfolder= DIRCWD + "/tmp/", browser="",
  # page_num=1, isreturn_df=1)

 ### pip install attrdict
 """
    # from attrdict import AttrDict as dict2
    # CFG= dict2({ "github_login": "", "github_pass":   "",  "github_phantomjs": "D:/_devs/webserver/phantomjs-1.9.8/phantomjs.exe"})

    if keywords is None:
        keywords = ["import jedi", "jedi.Script("]
    CFG_phantomjs, CFG_github_login, CFG_github_pass = (
        CFG.phantomjs,
        CFG.github_login,
        CFG.github_pass,
    )

    from selenium import webdriver
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    from selenium.webdriver.common.keys import Keys
    from bs4 import BeautifulSoup

    # noinspection PyUnresolvedReferences
    import wget

    DesiredCapabilities.PHANTOMJS[
        "phantomjs.page.settings.userAgent"
    ] = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0) Gecko/20121026 Firefox/16.0"

    if browser == "firefox":
        driver = webdriver.Firefox()
    else:
        driver = webdriver.PhantomJS(
            CFG_phantomjs
        )  # r"D:/_devs/webserver/phantomjs-1.9.8/phantomjs.exe"

    driver.get("https://github.com/login")
    username = driver.find_element_by_id("login_field")
    password = driver.find_element_by_id("password")
    username.clear()
    username.send_keys(CFG_github_login)
    password.clear()
    password.send_keys(CFG_github_pass)
    # driver.find_element_by_name("commit").click()
    password.send_keys(Keys.ENTER)

    os_folder_create(outputfolder)

    # INSERT KEYWORDS
    kw_query = ""
    for kw in keywords:
        kw_query = kw_query + "%22" + kw + "%22+"

    print("Search results:", flush=True)
    box_id = 0
    list_of_dicts = []
    list_filename = []
    try:
        for page in range(page_start, page_end + 1):
            print("\nPage " + str(page) + ": ", end=" ", flush=True)

            base_url = (
                "https://github.com/search?l=Python&p="
                + str(page)
                + "&q="
                + kw_query
                + "&type=Code&utf8=%E2%9C%93"
            )
            driver.get(base_url)
            html1 = driver.page_source
            soup = BeautifulSoup(html1, "lxml")

            box_id = 0
            # Scraping
            for desc, blob in zip(
                soup.findAll("div", class_="d-inline-block col-10"),
                soup.findAll("div", class_="file-box blob-wrapper"),
            ):

                desc_text = desc.text.strip()
                box_filename = desc_text.split("\n      –\n      ")[1].split("\n")[0].strip()

                if (FILTER and (box_filename not in list_filename)) or (not FILTER):
                    box_id = box_id + 1
                    print(box_id, end=" ", flush=True)

                    dict1 = {
                        "keywords": keywords,
                        "language": "Python",
                        "box_id": "",
                        "box_date": "",
                        "box_text": "",
                        "box_reponame": "",
                        "box_repourl": "",
                        "box_filename": "",
                        "box_fileurl": "",
                    }

                    urls = desc.findAll("a")
                    dict1["box_repourl"] = "https://github.com" + urls[0]["href"]
                    dict1["box_fileurl"] = "https://github.com" + urls[1]["href"]
                    driver.get(dict1["box_fileurl"])

                    dict1["box_id"] = box_id
                    dict1["box_filename"] = box_filename
                    dict1["box_reponame"] = desc_text.split(" ")[0].split("/")[-1].strip("\n")
                    dict1["box_date"] = (
                        desc_text.split("\n      –\n      ")[1]
                        .split("\n")[3]
                        .strip("Last indexed on ")
                    )

                    ######### DOWNLOADING    #####################################################################
                    if isdownload_file:
                        outputfile2 = (
                            outputfolder
                            + "/"
                            + dict1["box_reponame"]
                            + "_"
                            + dict1["box_filename"]
                            + "_"
                            + str(box_id)
                            + ".py"
                        )
                        driver.find_element_by_xpath('//*[@id="raw-url"]').click()
                        if isdebug:
                            print(driver.current_url, flush=True)
                        wget.download(url=driver.current_url, out=outputfile2)

                    blob_code = """ """
                    for k in blob.findAll("td", class_="blob-code blob-code-inner"):
                        aux = k.text.rstrip()
                        if len(aux) > 1:
                            blob_code = blob_code + "\n" + aux
                    dict1["box_text"] = blob_code

                    list_of_dicts.append(dict1)
                    list_filename.append(box_filename)

    except Exception as e:
        print(e)
    driver.quit()

    df = pd.DataFrame(list_of_dicts)
    print("Nb elements:" + str(len(df)))

    if iswrite_df:
        df.to_csv(
            outputfolder + "/" + outputfile, sep=r"§", encoding="utf-8", index=False, mode="w"
        )
    if isreturn_df:
        return df


def code_search_usage(
    module_name="jedi", method="Script", outputfolder="", sep=r"§", page_end=8, from_source="github"
):
    """      
        "from jedi import Script"   "Script("
        "from jedi"       "Script(" 
        "import jedi    .Script("
   output folder :  zdocs/module_sample/jedi/  username_reponame_filename.py 
   """
    import random

    ll_pattern = [
        ["import " + module_name, "." + method + "(", "test"],
        ["from " + module_name + " ", method + "(", "test"],
        ["import " + module_name, "." + method + "("],
        ["from " + module_name + " ", method + "("],
    ]

    outputfolder += "/" + module_name + "/"
    os_folder_create(outputfolder)
    output_codefile = outputfolder + "/codefile/"
    os_folder_create(output_codefile)

    if from_source == "github":
        df_all = None
        for ii, x in enumerate(ll_pattern):
            df = code_search_github(
                keywords=x,
                outputfolder=output_codefile,
                browser="",
                page_start=1,
                page_end=page_end,
                isreturn_df=1,
                iswrite_df=0,
                isdownload_file=1,
                isdebug=0,
                outputfile="",
            )

            try:
                df_all = pd.concat((df_all, df))
            except:
                df_all = df
        df_all.drop_duplicates("box_fileurl", inplace=True)
        outputfile = (
            outputfolder
            + "/"
            + module_name
            + "_"
            + method
            + "_sample_"
            + str(random.randint(1000, 9999))
            + ".txt"
        )
        df_all.to_csv(outputfile, sep=sep, encoding="utf-8", index=False, mode="w")
        print(outputfile)


######################################################################################################
############## Code Search #################################################################################
def conda_path_get(subfolder="package/F:/"):
    if os.__file__.find("envs") > -1:
        DIRANA = os.__file__.split("envs")[0] + "/"  # Anaconda from linux
    else:
        DIRANA = os.__file__.split("Lib")[0] + "/"  # Anaconda from root

    os_name = sys.platform[:3]
    if subfolder == "package":
        DIR2 = None
        if os_name == "lin":
            DIR2 = DIRANA + "/Lib/site-packages/"
        elif os_name == "win":
            DIR2 = DIRANA + "/Lib/site-packages/"
        return DIR2


def os_file_listall(dir1, pattern="*.*", dirlevel=1, onlyfolder=0):
    """ dirpath, filename, fullpath
   # DIRCWD=r"D:\_devs\Python01\project"
   # aa= listallfile(DIRCWD, "*.*", 2)
   # aa[0][30];   aa[2][30]
  """
    matches = {}
    dir1 = dir1.rstrip(os.path.sep)
    num_sep = dir1.count(os.path.sep)
    matches["dirpath"] = []
    matches["filename"] = []
    matches["fullpath"] = []

    for root, dirs, files in os.walk(dir1):
        num_sep_this = root.count(os.path.sep)
        if num_sep + dirlevel <= num_sep_this:
            del dirs[:]
        for f in fnmatch.filter(files, pattern):
            matches["dirpath"].append(os.path.splitext(f)[0])
            matches["filename"].append(os.path.splitext(f)[1])
            matches["fullpath"].append(os.path.join(root, f))
    return matches


def os_file_search_fast(fname, texts=None, mode="regex/str"):
    if texts is None:
        texts = ["myword"]
    res = []  # url:   line_id, match start, line
    nb = 0
    error_flag = False
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
                        except:
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
                        except:
                            line_enc = line
                        res.append((text, fname, lineno + 1, found, line_enc))

        elif mode == "full":
            texts = [(text, text.encode(enc)) for text in texts]
            with open(fname, "rb") as f1:
                lines = f1.readlines()

            for lineno, line in enumerate(lines):
                for text, textc in texts:
                    found = line.find(textc)
                    if found > -1:
                        try:
                            line_enc = line.decode(enc)
                        except Exception:
                            line_enc = line
                        res.append((text, fname, lineno + 1, found, line_enc))

    except IOError as xxx_todo_changeme:
        (_errno, _strerror) = xxx_todo_changeme.args
        print("permission denied errors were encountered")

    except re.error:
        print("invalid regular expression")

    return res


def code_search_file(
    srch_pattern=None,
    mode="str/regex",
    module_name_in="",
    folder_in="",
    folder_excluder=None,
    file_pattern="*.py",
    output_file="",
    dirlevel=20,
):
    if srch_pattern is None:
        srch_pattern = ["word1", "word2"]
    if folder_excluder is None:
        folder_excluder = [""]
    if module_name_in != "":
        folder_in = conda_path_get(subfolder="package")
        folder_in += "/" + module_name_in + "/"
    print(folder_in)

    list_all = os_file_listall(folder_in, pattern=file_pattern, dirlevel=dirlevel)
    ll = []
    for f in list_all["fullpath"]:
        ll = ll + os_file_search_fast(f, texts=srch_pattern, mode=mode)

    df = pd.DataFrame(ll, columns=["search", "filename", "lineno", "pos", "line"])
    if output_file != "":
        df.to_csv(output_file, sep="§", encoding="utf-8", mode="w")
    return df
    # aa= code_search_file( srch_pattern=[ u"from ","import "], mode="str", dir1=DIRCWD, file_pattern="*.py", dirlevel=1)
    # aa= code_search_file( srch_pattern=[ u"from ","import "], mode="full", dir1=DIRCWD, file_pattern="*.py", dirlevel=1)


################################################################################################
def np_list_dropduplicate(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def np_list_flatten(l):
    if l is not None:
        if len(l) > 0:
            return [item for sublist in l for item in sublist]
    else:
        return []


def code_parse_line(li, pattern_type="import/import_externa"):
    """
    External Packages
  """
    ### Import pattern
    if pattern_type == "import":
        if li.find("from") > -1:
            l = li[li.find("from") + 4 : li.find("import")].strip().split(",")
        else:
            l = li.strip().split("import ")[1].strip().split(",")

        l = [x for x in l if x != ""]
        l = np_list_dropduplicate(l)
        return l

    # Only external
    if pattern_type == "import_extern":
        if li.find("from") > -1:
            l = li[li.find("from") + 4 : li.find("import")].strip().split(",")
        else:
            l = li.strip().split("import ")[1].strip().split(",")

        l = [x for x in l if x != ""]
        l = [x for x in l if x[0] != "."]
        l = [x.split(".")[0].split("as")[0].split("#")[0].strip() for x in l]
        l = np_list_dropduplicate(l)
        return l


def code_extract_pattern(
    pattern="import", module_name_in="conda", folder_in="", import_type1="extern/intern"
):

    if pattern == "import":
        df = code_search_file(
            srch_pattern=["import "],
            mode="str",
            module_name_in=module_name_in,
            folder_in=folder_in,
            folder_excluder=[""],
            file_pattern="*.py",
            output_file="",
            dirlevel=20,
        )

        df["module_list"] = df["line"].apply(lambda x: code_parse_line(x, "import"))
        df["module_list_extern"] = df["line"].apply(lambda x: code_parse_line(x, "import_extern"))
        lextern = np_list_dropduplicate(np_list_flatten(df["module_list_extern"].values))
        lall = np_list_dropduplicate(np_list_flatten(df["module_list"].values))
        return lextern, lall, df


# lextern, lall, df_import = code_search_pattern(pattern="import", module_name_in="conda", import_type1="extern/intern")
# print(lextern[:20], lall[:20], df_import.head(5))


def code_parse_file(filepattern="*.py", folder="", search_regex="", dirlevel=0):
    """
    Search into downloaded .py file using regex and put into nice tabular format
    for type inference.
      if module_name in file_i and  object_name_regex in line :
          High probability than object_name == our name
          --> Get the code string ---> Split into arguments -->
          --> for each argument, do testing of types
          
      
    """
    pass


######################################################################################################
######################################################################################################
IIX = 0


def pprint(a):
    global IIX
    IIX = IIX + 1
    print("\n--" + str(IIX) + ": " + a, flush=True)


def ztest():
    DIRCWD = "/home/ubuntu/ztest/"
    pprint("### Unit Tests")
    # os_folder_create("/ztest")

    pprint("module_doc_write")
    module_doc_write(module_name="jedi", outputfile="zz_doc_jedi.txt")

    pprint("module_signature_write")
    module_signature_write(module_name="json", isdebug=1)

    pprint("module_unitest_write")
    module_unitest_write(
        input_signature_csv_file="doc_json.csv", outputfile="zz_unitest_run_json.txt", isdebug=1
    )

    pprint("module_unitest_write: module name")
    module_unitest_write(module_name="json", outputfile="zz_unitest_run_json2.txt", isdebug=1)

    pprint("module_signature_compare: version between 2 docs.")
    df = module_signature_compare(
        "doc_json.csv", "doc_json.csv", export_csv="zz_json_compare.csv", return_df=1
    )
    print(df.head(5))
    """
    Might be tricky to get 2 version of numpy in same environnement....
      Need to generate in 2 different python envs  and get the csv
    """

    pprint("module Github Donwload")
    # df= github_code_search(keywords= ["import jedi",   "jedi.Script(" ], outputfolder= os.getcwd()+"/tmp/", browser="",
    #                       page_start=25, page_end= 25, isreturn_df=1, isdebug=1)
    # print( len(df), df.dtypes )

    pprint("code search")
    os_file_search_fast("codesource.py", texts=["from ", "import "], mode="str")
    aa = code_search_file(
        srch_pattern=["from ", "import "],
        mode="str",
        folder_in=DIRCWD,
        file_pattern="*.py",
        dirlevel=1,
    )
    aa.head(3)

    pprint("code search: import module conda")
    lextern, lall, df_import = code_extract_pattern(
        pattern="import", module_name_in="conda", import_type1="extern"
    )
    print(lextern[:20], lall[:20], df_import.head(5))


####################################################################################################
####################################################################################################
if __name__ == "__main__":
    import argparse

    ppa = argparse.ArgumentParser()
    ppa.add_argument("--do", type=str, default="", help=" unit_test")
    ppa.add_argument("--module", type=str, default="", help=" unit_test")
    arg = ppa.parse_args()

    if arg.do != "" and arg.module != "":
        print("Running Task")
        if arg.do == "module_signature_write":
            module_signature_write(arg.module)
        if arg.do == "module_unittestt_write":
            module_unitest_write(module_name=arg.module)
        else:
            globals()[arg.action](arg.module)  # Execute command

    if arg.do == "test":
        ztest()
