"""
A simple python module to parse the code and format it based on some rules.
Some rules are:
rule 1 - change a line starting with 3 #'s into x #'s where x is 90 by default
         if no text was found else preserve text and fill the rest with #'s
rule 2 - normalize log statements in the file
rule 3 - put all consecutive imports on one line
rule 4 - align assignment operators

Usage:

cli_format -i /path/to/file or /path/to/dir --out_dir /path/to/output

"""
import re
import glob
import fire
import os
import tqdm
import datetime
##############################################################################################


def format_comments(text="default", line_size=90):
    """
    Takes a string of text and formats it based on rule 1 (see docs).
    """
    # rules to detect fancy comments, if not text
    regex1 = r"^ *?####*$"
    # rules to detect fancy comments, if text
    regex2 = r"^ *?####*([^#\n\r]+)#*"
    # if detected pattern 1, replace with this
    subst1 = "#"*line_size

    # if detected pattern 2, replace with this
    def subst2(match_obj):
        fix_pad = 4 + 2  # 4 hashes on left plus two spaces
        cap_group = match_obj.group(1).strip()
        return '#### ' + cap_group + ' ' + '#'*(line_size-fix_pad-len(cap_group))

    text = re.sub(regex1, subst1, text, 0, re.MULTILINE)
    text = re.sub(regex2, subst2, text, 0, re.MULTILINE)
    # formatted text to return
    return text


def format_logs(text="default", line_size=90):
    """
    Takes a string of text and formats it based on rule 2 (see docs).
    """
    # rule to find log statemets
    regex3 = r"log\(\"#+(.*?)#*(\".*)"

    # substitution to replace the found log statements
    def subst3(match_obj):
        fix_pad = 4 + 2  # 4 hashes on left plus two spaces
        cap_group = match_obj.group(1).strip()
        return r'log("#### ' + cap_group + ' ' + '#'*(line_size-fix_pad-len(cap_group)) + match_obj.group(2)

    text = re.sub(regex3, subst3, text, 0, re.MULTILINE)
    # return formatted text
    return text


def format_imports(text):
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
    skip_tokens = ['if', 'for', 'while', '(', ')', 'else']

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
            right = "= ".join(line.split("=")[1:] )

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


######################################################################################
def os_glob(in_dir):
    """
    os_glob a given directory for all .py files and returns a list of source files.
    """
    files = glob.glob(in_dir + "/**/*.py", recursive=True)
    # remove .ipynb_checkpoints
    files = [s for s in files if ".ipynb_checkpoints" not in s]
    # print("os_glob files done ... ")
    return files


def format_file(in_file, out_dir):
    # if input is a file and make sure it exits
    if os.path.isfile(in_file):
        with open(in_file) as f:
            text = f.read()

        text_f = format_comments(text)
        text_f = format_logs(text_f)
        text_f = format_imports(text_f)
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
    src_files = os_glob(in_dir)

    for f in tqdm.tqdm(src_files):
        if mod_period(f):
            format_file(f, out_dir)
        else:
            print(f"{f} is not modified within one week")


def mod_period(in_file):
    file_stats = os.stat(in_file)
    mod_date = datetime.datetime.fromtimestamp(file_stats.st_mtime)
    now = datetime.datetime.now()
    week_delta = datetime.timedelta(weeks=1)

    if now - mod_date < week_delta:
        return True     # file can be formatted
    else:
        return False


def load_arguments():
    """
    Parse the arguments
    """
    import argparse

    p = argparse.ArgumentParser(description="")
    p.add_argument("--dir_in", "-i", required='True',
                   default="test/run_train.py",  help="Source file path or path to a directory")
    p.add_argument("--dir_out", default="formatted",
                   help="Name of output directory to store results")

    arg = p.parse_args()
    return arg

# TODO: Add functions for formating functions and dictionaries


def main():
    args = load_arguments()

    _input = args.dir_in
    out_dir = args.dir_out

    if ".py" in _input:
        if mod_period(_input):
            format_file(_input, out_dir)
        else:
            print(f"{_input} is not modified within one week")
    else:
        format_dir(_input, out_dir)


if __name__ == "__main__":
    main()
