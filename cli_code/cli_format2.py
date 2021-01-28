import re
import glob
import fire
import os
import tqdm


def rule1(text="default"):
    # rules to detect fancy comments
    regex1 = r"^#{3,}$"
    regex2 = r"^#+ (\w+) .+#$"
    # if detected, replace with this
    subst1 = "#"*100

    def subst2(match_obj):
        return r'#### ' + match_obj.group(1) + ' ' + '#'*(100-6-len(match_obj.group(1)))

    # # some test strings
    # test_str1 = "#########"
    # test_str2 = "########## TEST ################"
    # print("comment which start with 3 or more # and have no text")
    # print(test_str1)
    # print(re.sub(regex1, subst1, test_str1, 0, re.MULTILINE))
    # print("comment which start with 3 or more # and have text in it")
    # print(test_str2)
    # print(re.sub(regex2, subst2, test_str2, 0, re.MULTILINE))

    text = re.sub(regex1, subst1, text, 0, re.MULTILINE)
    text = re.sub(regex2, subst2, text, 0, re.MULTILINE)
    # formatted text to return
    return text


def rule2(text="default"):
    # rule to find log statemets
    regex3 = r"log\(\"#+ (.*) #+\"\)"
    # substitution to replace the found log statements

    def subst3(match_obj):
        return r'log("#### ' + match_obj.group(1) + ' ' + '#'*(100-6-len(match_obj.group(1))) + '")'

    # # a test string for this case
    # test_str3 = 'log("#### Data preparation #########################################################")'
    # print("formatting log statements")
    # print(test_str3)
    # print(re.sub(regex3, subst3, test_str3, 0, re.MULTILINE))

    text = re.sub(regex3, subst3, text, 0, re.MULTILINE)
    # return formatted text
    return text


def rule3(text):
    # rule to find consective imports
    regex4 = r"^import[\s\w]+?(?=from|^\s*$)"
    # this subsitution will happen with a function

    def subst4(match_obj):
        pattern = r"import (\w+)"
        ind_imports = re.findall(pattern, match_obj.group(0))
        return r"import " + ", ".join(ind_imports) + "\n"

    # # a test string for this case
    # test_str4 = '''
    # import importlib
    # import json
    # import os
    # import sys

    # import argparse
    # import pandas
    # from run_preprocess import preprocess, preprocess_load
    # from util_feature import load, save_list, load_function_uri, save
    # import warnings
    # import numpy
    # from PIL import Image
    # '''
    # print("all consecitive imports are strung together")
    # print(test_str4)
    # print(re.sub(regex4, subst4, test_str4, 0, re.MULTILINE))

    text = re.sub(regex4, subst4, text, 0, re.MULTILINE)
    # return formatted text
    return text


def scan(in_dir):
    files = glob.glob(in_dir + "/**/*.py", recursive=True)
    # remove .ipynb_checkpoints
    files = [s for s in files if ".ipynb_checkpoints" not in s]
    # print("scan files done ... ")
    return files


def format_file(in_file, out_dir):
    # if input is a file and make sure it exits
    if os.path.isfile(in_file):
        with open(in_file) as f:
            text = f.read()

        text_f = rule1(text)
        text_f = rule2(text_f)
        text_f = rule3(text_f)

        file_path, file_name = os.path.split(in_file)
        if not os.path.exists(os.path.join(out_dir, file_path)):
            os.makedirs(os.path.join(out_dir, file_path))

        with open(os.path.join(out_dir, file_path, file_name), "w") as f:
            f.write(text_f)

    else:
        print("No such file exitst, make sure your path is correct")


def format_dir(in_dir, out_dir):
    src_file = scan(in_dir)

    for f in tqdm.tqdm(src_file):
        format_file(f, out_dir)


def main(in_file=None, in_dir=None, out_dir="formatted"):

    if in_file != None:
        format_file(in_file, out_dir)

    if in_dir != None:
        format_dir(in_dir, out_dir)


if __name__ == "__main__":
    fire.Fire(main)
