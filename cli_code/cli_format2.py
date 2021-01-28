"""
A simple python module to parse the code and format it based on some rules.
Some rules are:
rule 1 - change a line starting with 3 #'s into x #'s where x is 90 by default
         if no text was found else preserve text and fill the rest with #'s
rule 2 - normalize log statements in the file
rule 3 - put all consecutive imports on one line
rule 4 - align assignment operators

Usage:

cli_format --in_dir=/path/to/file or /path/to/dir --out_dir=/path/to/output

"""
import re
import glob
import fire
import os
import tqdm
##############################################################################################


def normalize_comments(text="default", line_size=90):
    """
    Takes a string of text and formats it based on rule 1 (see docs).
    """
    # rules to detect fancy comments, if not text
    regex1 = r"^#{3,}$"
    # rules to detect fancy comments, if text
    regex2 = r"^#+ (\w+) .+#$"
    # if detected pattern 1, replace with this
    subst1 = "#"*line_size

    # if detected pattern 2, replace with this
    def subst2(match_obj):
        return r'#### ' + match_obj.group(1) + ' ' + '#'*(line_size-6-len(match_obj.group(1)))

    text = re.sub(regex1, subst1, text, 0, re.MULTILINE)
    text = re.sub(regex2, subst2, text, 0, re.MULTILINE)
    # formatted text to return
    return text


def normalize_logs(text="default", line_size=90):
    """
    Takes a string of text and formats it based on rule 2 (see docs).
    """
    # rule to find log statemets
    regex3 = r"log\(\"#+ (.*) #+\"\)"

    # substitution to replace the found log statements
    def subst3(match_obj):
        return r'log("#### ' + match_obj.group(1) + ' ' + '#'*(line_size-6-len(match_obj.group(1))) + '")'

    text = re.sub(regex3, subst3, text, 0, re.MULTILINE)
    # return formatted text
    return text


def normalize_imports(text):
    """
    Takes a string of text and formats it based on rule 3 (see docs).
    """
    # rule to find consective imports
    regex4 = r"^import[\s\w]+?(?=from|^\s*$)"

    # this subsitution will happen with a function
    def subst4(match_obj):
        pattern = r"import (\w+)"
        ind_imports = re.findall(pattern, match_obj.group(0))
        return r"import " + ", ".join(ind_imports) + "\n"

    text = re.sub(regex4, subst4, text, 0, re.MULTILINE)
    # return formatted text
    return text


def format_assignments(text):
    """
    Aligns assignment statements in the source file and return a text.
    """
    lines = text.split("\n")

    # process text line by and store each line at its starting index
    formated_text = []
    a_block_left = []
    a_block_right = []

    # these statements may contain = too are not assignment
    skip_tokens = ['if', 'for', 'while', '(', ')']

    def format_assignment_block():
        """
        Process an assignment block, returns formatted list of 
        assignment lines in that block.   
        """
        max_left = max([len(left) for left in a_block_left])
        f_assignments = []
        for left, right in zip(a_block_left, a_block_right):
            new_line = left + ' '*(max_left-len(left)) + ' = ' + right
            f_assignments.append(new_line)
        return f_assignments

    for line in lines:
        # assignment should contain = and shouldn't contain anything from skip_tokens
        # empty list is considered false
        if "=" in line and not ["bad" for t in skip_tokens if t in line.split("=")[0]]:
            left = line.split("=")[0]
            right = line.split("=")[-1]

            # need to preserve spaces on left
            a_block_left.append(left.rstrip())
            a_block_right.append(right.strip())

        else:
            # if not assingment, process the block if not empty
            if len(a_block_left) != 0:
                f_assignments = format_assignment_block()
                formated_text.extend(f_assignments)
                a_block_left = []
                a_block_right = []
            # if not assingment, preserve the line
            formated_text.append(line)

    # check if the block is non empty at the end
    # because the else will not trigger if assignment lines are at the last
    if len(a_block_left) != 0:
        f_assignments = format_assignment_block()
        formated_text.extend(f_assignments)

    # join individual lines in list and returns as text string
    return '\n'.join(formated_text)


def test_rules(rules2test=1):
    """
    Test all rules based on these strings
    """
    rules2test = str(rules2test)
    if '1' in rules2test:
        # some test strings for rul1 case
        test_str1 = "#########"
        test_str2 = "########## TEST ################"
        print("comment which start with 3 or more # and have no text")
        print(test_str1)
        print(normalize_comments(test_str2))
        print("comment which start with 3 or more # and have text in it")
        print(test_str2)
        print(normalize_comments(test_str2))

    if '2' in rules2test:
        # a test string for rule 2 case
        test_str3 = 'log("#### Data preparation #########################################################")'
        print("formatting log statements")
        print(test_str3)
        print(normalize_logs(test_str3))

    if '3' in rules2test:
        # a test string for rule 3 case
        test_str4 = '''
        import importlib
        import json
        import os
        import sys

        import argparse
        import pandas
        from run_preprocess import preprocess, preprocess_load
        from util_feature import load, save_list, load_function_uri, save
        import warnings
        import numpy
        from PIL import Image
        '''
        print("all consecitive imports are strung together")
        print(test_str4)
        print(normalize_imports(test_str4))

    if '4' in rules2test:
        # a test string for rule 4
        test_str5 = """    
        keywords = args.keyword
        created = args.created
        pushed = args.pushed
        folder_name = args.output
        # print('Keyword to search GitHub: ' + keyword)
        # print('Created: ' + created)
        # print('Pushed: ' + pushed)

        df = pd.DataFrame()
        type = 'Repositories'
        if evl_cond(var="has_value", var2="no_value"):
            if response.status_code == 200:
                username = []
                repo_name, repo_url = [], []
                description = []
                update_info = []"""
        print("alignment of assignment lines")
        print(test_str5)
        print(format_assignments(test_str5))


######################################################################################
def scan(in_dir):
    """
    Scan a given directory for all .py files and returns a list of source files.
    """
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

        text_f = normalize_comments(text)
        text_f = normalize_logs(text_f)
        text_f = normalize_imports(text_f)
        text_f = format_assignments(text_f)

        # get the base directory of source file for makedirs function
        file_path, file_name = os.path.split(in_file)
        if not os.path.exists(os.path.join(out_dir, file_path)):
            os.makedirs(os.path.join(out_dir, file_path))

        with open(os.path.join(out_dir, file_path, file_name), "w") as f:
            f.write(text_f)

    else:
        print(f"No such file exists {in_file}, make sure your path is correct")


def format_dir(in_dir, out_dir):
    src_files = scan(in_dir)

    for f in tqdm.tqdm(src_files):
        format_file(f, out_dir)


def main(in_dir=None, out_dir="formatted"):

    if in_dir != None:
        if ".py" in in_dir:
            format_file(in_dir, out_dir)
        else:
            format_dir(in_dir, out_dir)
    else:
        print("No input specified")


###############################################################################################
def test():
    """
    Test a file in test folder. 
    (although we can also do this)
    python cli_code/cli_format2.py --in_dir=test\run_tain.py
    and remove this function
    """
    test_file = os.path.join("test", "run_train.py")
    main(in_dir=test_file)


if __name__ == "__main__":
    fire.Fire(main)
    # test_rules(4)
    # test()
