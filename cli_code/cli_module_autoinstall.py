# -*- coding: utf-8 -*-
"""
Auto install missing package by scanning error message


conda create -y -n ztest  python=3.6.5
source activate Emptyconda

cd /home/ubuntu/aagit/aapackage/aapackage/

python cli_module_autoinstall.py  --folder_input  /home/ubuntu/aagit/aapackage/aapackage/batch


Using python in the PATH !!!

### tobe visible in jputer
conda install ipykernel 

"""

import glob
# from IPython.nbformat import current as nbformat
# from IPython.nbconvert import PythonExporter
# import nbformat
# from nbconvert import PythonExporter
# from tqdm import tqdm
from time import sleep

#### Not to install
white_lists = ["resnet", "mobilenet", "inception", "utils", "aapackage" "util", "task_config"]


def os_system(cmds, stdout_only=1):
    """
     Get print output from command line
  """
    import subprocess

    # cmds = cmds.split(" ")
    p = subprocess.Popen(cmds, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.stdout.read(), p.stderr.read()

    if stdout_only:
        return out
    return out, err


def scan(data_file):
    # note: I have checked os_file_listall, I think the following will be better
    files = glob.glob(data_file + "/**/*.py", recursive=True)
    # remove .ipynb_checkpoints
    files = [s for s in files if ".ipynb_checkpoints" not in s]

    print("scan files done ... ")
    return files


def get_packages(file):

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
                line = line[line.index("from") + 4 :].strip()
                if "." in line:
                    package = line[: min(line.index("."), line.index(" "))]
                else:
                    package = line[: line.index(" ")]
            else:
                if "." in line:
                    # import XX.XX
                    line = line[line.index("import") + 6 :].strip()
                    package = line[: line.index(".")]
                else:
                    # import XX
                    line = line[line.index("import") + 6 :].strip()
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
        except Exception as e:
            pass

    return packages


def get_missing(all_packages):
    # # form import XX,XX,XX
    # run_string = 'import '+ ','.join(all_packages)
    # # maybe cd to the dir

    miss_package = []
    for package in all_packages:
        run_string = "import " + package

        cmds = ["python -c ", "'import  %s '" % package]
        try:
            exec(run_string)
            # print(cmds)
            # out, err = os_system(cmds, stdout_only=0)
            # print("errro", err)

            # os.system('python -c "%s"'%run_string)
        except Exception as e:
            # print(e)
            miss_package.append(package)

    return miss_package


def load_arguments():
    """
       --param_file /zs3drive/config_batch.toml --param_mode test_launch
  """
    import argparse

    cur_path = os.path.dirname(os.path.realpath(__file__))
    config_file = os.path.join(cur_path, "config.toml")

    p = argparse.ArgumentParser()
    p.add_argument("--folder_input", default=config_file, help="Params File")
    p.add_argument("--mode", default="test", help=" test/ prod /uat")
    args = p.parse_args()
    return args


def write_requirements(source_files):
    # check packages
    need_to_install_package_list = []
    for file in source_files:
        all_packages = get_packages(file)
        miss_packages = get_missing(all_packages)

        need_to_install_package_list.extend(miss_packages)

        # if len(miss_packages):
        #     print('-'*10, file)
        #     print(miss_packages)

    need_to_install_package_set = list(set(need_to_install_package_list))
    # print(need_to_install_package_set)
    # print(len(need_to_install_package_set))

    need_to_install_package_set = [s for s in need_to_install_package_set if s]
    need_to_install_package_set = [
        s for s in need_to_install_package_set if not any([w in s for w in white_lists])
    ]
    need_to_install_package_set = list(set(need_to_install_package_set))

    print(need_to_install_package_set)
    print(len(need_to_install_package_set))

    with open("./require_before.txt", "w") as fp:
        fp.write("\n".join(need_to_install_package_set))

    return need_to_install_package_set


def Run():
    args = load_arguments()
    data_file = args.folder_input

    # if args.conda_env != "" :
    #  os.system('conda create --yes  -n %s  '%args.conda_env  )
    #  os.system('source activate  -n %s  '%args.conda_env  )

    # scan file recursively
    source_files = scan(data_file)
    print(len(source_files))

    # auto install conda install in Group
    need_to_install_package_set = write_requirements(source_files)
    # sys.exit()

    ss = ""
    for package in need_to_install_package_set:
        ss = ss + " " + package
    print("Install ALL", ss)
    os.system("conda install -y %s  " % ss)

    sleep(5)

    # auto install conda
    need_to_install_package_set = write_requirements(source_files)
    for package in need_to_install_package_set:
        os.system("conda install -y %s  " % package)

    """
    # auto install conda
    need_to_install_package_set  = write_requirements(source_files) 
    for package in need_to_install_package_set:
        os.system('conda install -y %s --no-deps '%package  )    
    """

    # auto install pip
    need_to_install_package_set = write_requirements(source_files)
    for package in need_to_install_package_set:
        # os.system('conda install %s'%package)
        os.system("pip install %s --no-deps " % package)

    # check again
    miss_packages = get_missing(need_to_install_package_set)
    with open("./require_after.txt", "w") as fp:
        fp.write("\n".join(miss_packages))

    os.system("conda list ")


if __name__ == "__main__":
    import os

    print(os)
    Run()
