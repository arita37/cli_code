"""
Goal is to automate code check using a python script. This scripts do the following
For a given github repo url:

- Clone the repo with `git clone` and assign either a user specified name or repo's default name
- Build a conda env with packages required to use the repo
- Check if python code is running i.e., run main.py
- Generate signature docs of python source code

Usage:

`cli_repo_check https://www.github.com/{username}/{reponame}.git -n testing_env`

`-o` or `--dir_out` specify the name of target directory to clone the repo (default is {reponame})
`-n` or `--conda_env` specify name of our conda environment (if not specified, `{reponame}_env` will be used)
`-py` or `--python_version` specify the python version of the target environment (default is 3.6)
`-p` or `--packages` specify any extra packages in addition to required ones to install (default is numpy)

"""


######################################
import os
import argparse
import sys
import platform
import glob
import logging

# TODO: use these to check the files
# from importlib import import_module
# import inspect


def get_logger():
    """
    Instantiate a logger for this module
    """
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
    return logging.getLogger(__name__)


logger = get_logger()


def get_os():
    """
    Get the operating system information for the machine running this script.
    """
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
    logger.info("Parsing of files completed. See {}".format(out_file))


def load_arguments():
    """
    Get arguments from command line.
    """
    # cur_path = os.path.dirname(os.path.realpath(__file__))
    p = argparse.ArgumentParser()
    p.add_argument("repo_url", help="Url of a git repository to clone")
    p.add_argument("--conda_env", "-n", default=None,
                   help="Name of conda environment to build for the repo, if not specified repo name will be used")
    p.add_argument("--python_version", "-py", default="3.6.7",
                   help="Python version to use in the conda environment")
    p.add_argument("--packages", "-p", nargs='?', default="numpy",
                   help="Custom/extra packages to install in new conda env")
    p.add_argument("--dir_out", "-o", default=None,
                   help="Name of the output directory to clone the repo, if not specified repo name will be used")
    args = p.parse_args()

    return args


def main():
    args = load_arguments()
    # this will be used for the repo name if no name was specified
    reponame = args.repo_url.split("/")[-1].split(".")[0]

    # make sure cloning was done successfully
    if git_clone(args.repo_url, args.dir_out):

        if args.dir_out != None and args.conda_env != None:
            # if out dir and conda env name are specified
            repo_build_conda(args.dir_out, args.conda_env)
            repo_check_root_files(args.dir_out, args.conda_env)
            repo_generate_signature(args.dir_out)
        elif args.dir_out != None:
            # if only dir_out is specified
            print(
                f"No conda environment specified, creating {args.dir_out}_env")
            repo_build_conda(args.dir_out, args.dir_out + "_env")
            repo_check_root_files(args.dir_out, args.dir_out + "_env")
            repo_generate_signature(args.dir_out)

        else:
            print(f"No conda environment specified, creating {reponame}_env")
            repo_build_conda(reponame, reponame+"_env")
            repo_check_root_files(reponame, reponame+"_env")
            repo_generate_signature(reponame)
    else:
        sys.exit(1)


if __name__ == '__main__':
    main()
