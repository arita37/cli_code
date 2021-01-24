"""
Create python script to do this :
For a given github repo url:
   1) git clone
   2) Build conda env with packages
   3) Check if python code is running i.e., run main.py
   4) Generate signature docs of python source code

Goal is to automate code check using a python script

Example
https://github.com/zhangqianhui/vae-gan-tensorflow.git
"""

# Steps
#  1)  git clone repoURL
#  2)  Build conda env from source code parsing
#       https://github.com/arita37/cli_code/blob/master/cli_code/cli_module_autoinstall.py
#  3) cd repo
#  4) Launch all files in root (main.py) with subprocess to check if running
#  5) Log error messages on disk
#
#  6) Parse source code with  import inspect and generate signature for each functiom
#     Write on disk
#     https://github.com/arita37/cli_code/blob/master/cli_code/cli_module_analysis.py


import os
import sys
import errno
import re
import time
import argparse
import subprocess
import logging
import sys
import platform
import glob
import re
import logging

# TODO: use these to check the files
# from importlib import import_module
# import inspect


def get_logger():
    logfile = "repo_check_logs.txt"
    log_format = (
        '[%(asctime)s] %(levelname)-6s %(name)-12s %(message)s'
    )
    logging.basicConfig(
        level=logging.INFO,
        format=log_format,
        handlers=[
            logging.FileHandler(logfile),
            logging.StreamHandler(sys.stdout),
        ]
    )
    # get a logger
    logger = logging.getLogger(__name__)
    return logger


logger = get_logger()


def get_os():
    curr_os = "linux" if "Linux" in platform.platform() else "win"
    return curr_os


def os_system(cmds, stdout_only=True):
    """
    Executes system command and
    Get print output from command line
    :param cmds a list containing command and its arguments
    """
    import subprocess

    p = subprocess.Popen(cmds, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    errcode = p.returncode

    if stdout_only:
        return out, errcode
    return out, err, errcode


def scan_dir(folder):
    # note: I have checked os_file_listall, I think the following will be better
    files = glob.glob(folder + "**/*.py")
    # remove .ipynb_checkpoints
    files = [s for s in files if ".ipynb_checkpoints" not in s]

    # print("Scan of files done ..")
    return files


def git_clone(url, out_dir=None):
    """
    Clone a git repository from its url.
    """
    if out_dir != None:
        _, stderr, errcode = os_system(
            ["git", "clone", url, out_dir], stdout_only=False)
        if errcode != 0:
            logger.error(stderr.decode('UTF-8'))
            # to indicate our operation was not a success
            return False
        return True
    else:
        _, stderr, errcode = os_system(
            ["git", "clone", url], stdout_only=False)
        if errcode != 0:
            logger.error(stderr.decode('UTF-8'))
            # to indicate our operation was not a success
            return False
        return True


def repo_build_conda(in_folder, conda_env=None):
    """
    Auto-generate a conda environment for the files in a given repo.
    """
    from cli_code import cli_env_autoinstall

    if conda_env != None:
        cli_env_autoinstall.create_env(
            in_folder, conda_env
        )
    else:
        cli_env_autoinstall.create_env(
            in_folder, in_folder
        )


def repo_check_root_files(folder, conda_env):
    """
    Launch all files in root (main.py) with subprocess to check if running
    Log error messages on disk
    """
    # Only root file
    logger.info("Checking files in root of repo.")
    file_list = scan_dir(folder)

    for file in file_list:
        err_msg, ret_code = os_system(
            ["conda", "activate", conda_env, "&&", "python ", file]
        )
        if ret_code != 0:
            logger.error(err_msg.decode("utf-8"))


def repo_generate_signature(folder):
    """
    Generate signature from the code
    """
    from cli_code.cli_module_parser import findVariablesInDir, writeCSV
    variables = findVariablesInDir(folder)
    out_file = os.path.join(folder, "parsed_docs.csv")
    writeCSV(variables, out_file)
    logger.info(f"Parsing of files completed. See {out_file}")


def load_arguments():
    """
    Get arguments from command line.
    """
    # cur_path = os.path.dirname(os.path.realpath(__file__))
    p = argparse.ArgumentParser()
    p.add_argument("repo_url", help="Url of a git repository to clone")
    p.add_argument("--conda_env", "-n",
                   help="Name of conda environment to build for the repo, if not specified repo name will be used")
    p.add_argument("--python_version", "-py", default="3.6.7",
                   help="Python version to use in the conda environment")
    p.add_argument("--packages", "-p", nargs='?', default="numpy",
                   help="Custom/extra packages to install in new conda env")
    p.add_argument("--output", "-o", default=None,
                   help="Name of the output directory to clone the repo, if not specified repo name will be used")
    args = p.parse_args()

    return args


def main():
    args = load_arguments()

    # this will be used for the repo name if no name was specified
    reponame = args.repo_url.split("/")[-1].split(".")[0]

    # make sure cloning was done successfully
    if git_clone(args.repo_url, args.output):

        if args.output != None:
            repo_build_conda(args.output, args.conda_env)
            repo_check_root_files(args.output, args.conda_env)
            repo_generate_signature(args.output)
        else:
            repo_build_conda(reponame, reponame+"_env")
            repo_check_root_files(reponame, reponame+"_env")
            repo_generate_signature(reponame)
    else:
        exit(1)


if __name__ == '__main__':
    main()
