# -*- coding: utf-8 -*-
"""
convert all IPython notebooks inside a directory to python scripts and save them to another directory. 
This also tests python scripts for potential syntax errors.

Usage:

`cli_convert_jupyter -i /path/to/notebooks -o path/to/python-scripts`

`-i` or `--dir_in`  argument is requiredand and specify the folder containing IPython notebooks
`-o` or `--dir_out` optional argument for output directory (default results will be saved in `py-scripts` directory)
"""
import ast
import glob
import os
import shutil
import sys

import nbformat
from nbconvert import PythonExporter
from tqdm import tqdm
#import pypandoc as pdoc


def scan(data_file):
    # note: I have checked os_file_listall, I think the following will be better
    files = glob.glob(data_file + "/**/*.ipynb", recursive=True)
    # remove .ipynb_checkpoints
    files = [s for s in files if ".ipynb_checkpoints" not in s]
    # print("scan files done ... ")
    return files


def convert2python(source_files, data_file, out_dir):
    dst_files = []
    for filepath in tqdm(source_files):
        # export_path = '%s/%s.py'%(out_dir, os.path.basename(filepath[:-6]))
        export_path = filepath.replace(data_file, out_dir)
        export_path = export_path[:-6] + ".py"
        # print(export_path)

        with open(filepath) as fh:
            nb = nbformat.reads(fh.read(), nbformat.NO_CONVERT)

        exporter = PythonExporter()
        source, _ = exporter.from_notebook_node(nb)

        with open(export_path, "w+") as fh:
            fh.writelines(source)
            # fh.writelines(source.encode('utf-8'))

        dst_files.append(export_path)

    print("convert to python file done ...")
    return dst_files


def check(file_list, dump=False):
    print("Checking results...")
    error_list = []
    error_msgs = []
    for f in file_list:
        with open(f, "r") as f1:
            codesource = f1.read()
        try:
            ast.parse(codesource)
        except Exception as e:
            # print('-'*30)
            # print(f, str(e))
            # print('-'*30)

            # error_list.append(f)
            error_list.append(os.path.abspath(f))
            error_msgs.append(str(e))

    if dump:
        with open("./issue_files.csv", "w") as fp:
            fp.write("file,error_info\n")
            for file, error in zip(error_list, error_msgs):
                fp.write("%s,%s\n" % (file, error))
    print("Checking completed. See issue_files.csv")
    return error_list

# TODO: Check why this is here
# def convert_ipynb_to_gallery(file_name):
#     """Convert jupyter notebook to sphinx gallery notebook styled examples.
#     Usage: python ipynb_to_gallery.py <notebook.ipynb>
#     Dependencies:
#     pypandoc: install using `pip install pypandoc`
#     """

#     python_file = ""
#     nb_dict = json.load(open(file_name))
#     cells = nb_dict["cells"]

#     for i, cell in enumerate(cells):
#         if i == 0:
#             assert cell["cell_type"] == "markdown", "First cell has to be markdown"

#             md_source = "".join(cell["source"])
#             rst_source = pdoc.convert_text(md_source, "rst", "md")
#             python_file = '"""\n' + rst_source + '\n"""'
#         else:
#             if cell["cell_type"] == "markdown":
#                 md_source = "".join(cell["source"])
#                 rst_source = pdoc.convert_text(md_source, "rst", "md")
#                 commented_source = "\n".join(
#                     ["# " + x for x in rst_source.split("\n")])
#                 python_file = python_file + "\n\n\n" + "#" * 70 + "\n" + commented_source
#             elif cell["cell_type"] == "code":
#                 source = "".join(cell["source"])
#                 python_file = python_file + "\n" * 2 + source

#     open(file_name.replace(".ipynb", ".py"), "w").write(python_file)


def load_arguments():
    import argparse

    parser = argparse.ArgumentParser(
        description='Converts an IPython notebook to python script.')
    parser.add_argument("-i", "--dir_in", required=True, default="",
                        help="Directory containing IPython notebook(s).")
    parser.add_argument("-o", "--dir_out", default="py-scripts",
                        help="Directory to put converted python scripts.")
    options = parser.parse_args()
    return options


def main():
    args = load_arguments()
    data_file, out_dir = args.dir_in, args.dir_out

    # scan file recursively
    source_files = scan(data_file)
    # print(source_files)

    # make some dirs in dst fold
    if os.path.exists(out_dir):
        inp = input("output dir exists, delete to re-generate? (y/n): ")
        if inp == "y":
            shutil.rmtree(out_dir)
        else:
            sys.exit(0)
    # TODO: this is copying whole source dir to target, fix this
    shutil.copytree(data_file, out_dir)
    dst_files_to_delete = scan(out_dir)
    for s in dst_files_to_delete:
        os.remove(s)

    # convert all files
    dst_files = convert2python(source_files, data_file, out_dir)

    # check converted script file are runnable
    # dump log file, default to the current fold
    error_list = check(dst_files, dump=True)

    # clean error file
    for s in error_list:
        os.remove(s)
    print(
        "%d were converted successfully, %d cause error"
        % (len(dst_files) - len(error_list), len(error_list))
    )


if __name__ == "__main__":
    main()
