# -*- coding: utf-8 -*-
"""
Auto install missing package by scanning error message

conda create -y -n ztest  python=3.6.5
source activate ztest
python cli_module_autoinstall.py  --folder_input  /home/ubuntu/aagit/aapackage/aapackage/batch  --packages "tensorflow=1.14 scikit-learn numpy pandas scipy matplotlib"

"""

import sys
import os
import glob
# from IPython.nbformat import current as nbformat
# from IPython.nbconvert import PythonExporter
# import nbformat
# from nbconvert import PythonExporter
# from tqdm import tqdm
from time import sleep
import re

import platform


# NOTE: not used in the main
# def setup_env(folder, url):
#     reponame = url.split("/")[-1]
#     os.system(" cd '{folder}'  &&  git clone {url} ")
#     foldert = folder + "/" + reponame
#     ll = []
#     for x in ["requirements.txt", "
# requirement.txt"]:
#         try:
#             with open(foldert + "/" + x, mode="r") as f:
#                 ll = f.readlines()
#         except:
#             pass
#     pkgs = " ".join(ll) if ll is not None else " pandas "
#     arg = {"folder_input": foldert, "conda_env": "ztest", "python_version":  "3.6.7", "packages": pkgs
#            }
#     os.system(" conda remove -n ztest")
#     run(arg)
#     os.system(" conda export -n ztest")
#     os.system(" conda export -n ztest")


##################################################################################

# # NOTE: not used in the main
# def os_system(cmds, stdout_only=True):
#     """
#     Get print output from command line
#     """
#     import subprocess

#     p = subprocess.Popen(cmds, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
#     out, err = p.communicate()
#     errcode = p.returncode
#     print(err, errcode)
#     if stdout_only:
#         return out, errcode
#     return out, err, errcode
# ######################################################################################


def get_os():
    curr_os = "linux" if "Linux" in platform.platform() else "win"
    return curr_os


def os_exec(x):
    ret_value = os.system(x)
    return ret_value


def scan(data_file):
    # note: I have checked os_file_listall, I think the following will be better
    files = glob.glob(data_file + "/**/*.py", recursive=True)
    # remove .ipynb_checkpoints
    files = [s for s in files if ".ipynb_checkpoints" not in s]

    # print("scan files done ... ")
    return files


def get_packages(file):
    """
    Get all required packages to run a given module,
    both from standard library and from 3rd party.
    """
    with open(file, "r") as fp:
        contents = fp.read()

    packages = []
    for line in contents.strip().split("\n"):
        line = line.strip()
        if not line:
            continue
        # if this is commented
        if line[0] == "#":
            continue
        if "import " not in line:
            continue

        try:
            package = None
            if "from" in line:
                # from XX.XX import XX
                # from XX import XX
                line = line[line.index("from") + 4:].strip()
                if "." in line:
                    package = line[: min(line.index("."), line.index(" "))]
                else:
                    package = line[: line.index(" ")]
            else:
                if "." in line:
                    # import XX.XX
                    line = line[line.index("import") + 6:].strip()
                    package = line[: line.index(".")]
                else:
                    # import XX
                    line = line[line.index("import") + 6:].strip()
                    package = line

            # XX as XX
            if " as " in package:
                package = package[: package.index(" as ")]
            # XX ; XX
            if ";" in package:
                package = package[: package.index(";")].strip()
            # import XX,XX
            if "," in package:
                for p in package.strip().split(","):
                    packages.append(p.strip())
            else:
                packages.append(package)
        except:  # Exception as e:
            pass

    return packages


def get_missing(all_packages, env_name="test"):
    """
    Take a list of packages that are required, try to import packages
    one by one and if any package throws an error, it will mark it missing.
    Finally returns the list of missing packages.
    """
    conda_env = env_name
    # # form import XX,XX,XX
    # run_string = 'import '+ ','.join(all_packages)
    # # maybe cd to the dir

    # we want to test in target environment not in our current env
    conda_activate = f"activate {conda_env} &&" if get_os(
    ) == "win" else f"source activate {conda_env} &&"

    miss_package = []
    for package in all_packages:
        #run_string = "import " + package

        try:
            # print(run_string)
            # NOTE: This check packages in current environment not the target environment
            # exec(run_string)
            run_string = f"conda.bat {conda_activate} python -c \"import {package}\""
            ret = os_exec(run_string)
            if ret != 0:
                miss_package.append(package)
        except:  # Exception as e:
            # print(e)
            # miss_package.append(package)
            pass

    return miss_package


def get_required_packages(source_files, conda_env="test"):
    """
    Takes a list of python modules and calls get_packages function
    on each module, get missing packages using get_missing function,
    removes the white listed packages and finally returns a list of packages
    that are needed to be installed in our environment.
    """
    # Not to install
    white_lists = ["resnet", "mobilenet", "inception",
                   "utils", "aapackage" "util", "task_config"]
    # check packages
    need_to_install_package_list = []
    for file in source_files:
        all_packages = get_packages(file)
        miss_packages = get_missing(all_packages, conda_env)

        need_to_install_package_list.extend(miss_packages)

    # Clean Up
    ll = []
    for t in need_to_install_package_list:
        t = t.replace('"', " ").strip()
        t = s = re.sub('[^0-9a-zA-Z]+', ' ', t).strip()
        if " " not in t and len(t) > 2:
            ll.append(t)

    package_list = list(set(ll))
    package_list = [
        s for s in package_list if not any([w in s for w in white_lists])
    ]
    package_list = list(set(package_list))

    # print(package_list)
    # print(len(package_list))

    # with open("./require_before.txt", "w") as fp:
    #     fp.write("\n".join(package_list))

    return package_list


def load_arguments():
    """
    Parse the arguments for the cli_env_autoinstall.py module.
    """
    import argparse

    # cur_path = os.path.dirname(os.path.realpath(__file__))
    # config_file = os.path.join(cur_path, "config.toml")

    p = argparse.ArgumentParser(
        description="Create a new conda environment for a repo and installs its dependencies.")
    p.add_argument(
        "folder_input", default="", help="Folder containing the source files")
    p.add_argument("--conda_env", "-n", default="test",
                   help="Name of conda environment to create")
    p.add_argument("--python_version", "-py", default="3.6.7",
                   help="Python version to use in the conda environment")
    p.add_argument("--packages", "-p", default="numpy",
                   help="Custom/extra packages to install in conda env, e.g., \"numpy tensorflow\"")

    p.add_argument("--mode", default="test",
                   help="conda environment mode which can be test/ prod /uat")
    arg = p.parse_args()
    return arg


def create_env(folder_input, conda_env, python_version='3.6', packages='numpy'):

    # get conda activate handle, depending on os
    # TODO: check if to use conda.bat activate or only activate
    conda_activate = f"activate {conda_env} &&" if get_os(
    ) == "win" else f"source activate {conda_env} &&"
    # conda install command
    conda_install = f"conda install -n {conda_env}"

    # Scan file recursively, to get all python modules in directory
    source_files = scan(folder_input)

    # TODO: check if the environment is already present or not
    # Create a new conda env if specified
    if conda_env != "test":
        os_exec(
            f"conda create -y -n {conda_env} python={python_version}")

    # Install default+user specified packages packages in the environment
    os_exec(f"{conda_activate} {conda_install} -y {packages}")

    # Install required packages for the given repo
    # TODO: improve it to handle the situation when import name
    # is different from the package name like python-opencv is
    # imported as cv2
    package_list = get_required_packages(source_files, conda_env)
    print(package_list)
    if len(package_list) != 0:
        ss = " ".join(package_list)
        print(f"{conda_activate} {conda_install} -y {ss} --no-update-deps ")
        os_exec(f"{conda_activate} {conda_install} -y {ss} --no-update-deps ")
        sleep(5)

    # Auto install conda individually (NOTE: no need for now)
    # miss_packages = get_missing(package_list)
    # for package in miss_packages:
    #     print(
    #         f"{conda_activate}  {conda_install}  -y {package}   --no-update-deps")

    # # Auto install pip (NOTE: no need for now)
    # miss_packages = get_missing(package_list)
    # for package in miss_packages:
    #     print(f"{conda_activate}  pip install {package} --no-deps")

    # check again (NOTE: __this will not work as it checks in the current env__ fixed)
    # miss_packages = get_missing(package_list)
    # with open("./require_after.txt", "w") as fp:
    #     fp.write("\n".join(miss_packages))

    os_exec(f"{conda_activate} conda env list")


def main():
    args = load_arguments()
    create_env(
        args.folder_input, args.conda_env,
        args.python_version, args.packages
    )


if __name__ == "__main__":
    main()
