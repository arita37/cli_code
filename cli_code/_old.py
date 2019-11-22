
"""

Create python script to do this :

For a given github repo :

   1)   git clone
   2)  Build conda env with packages
   3)  check if python code is running
            main.py
  4) Generate signature docs of python source code


Goal is to automate code check using a python script


Example
https://github.com/zhangqianhui/vae-gan-tensorflow


"""




#    1)   git clone repoURL






# 2)  Build conda env from source code parsing
  # cd repo
#https://github.com/arita37/cli_code/blob/master/cli_code/cli_module_autoinstall.py
   
   
   

# 3) Launch all files in root (main.py) with subprocess to check if running
    # Log error messages on disk
 
 
 
 
 
 
 
# 4) Parse source code with  import inspect and generate signature for each functiom
  #  Write on disk
   # https://github.com/arita37/cli_code/blob/master/cli_code/cli_module_analysis.py

"""
File: cll_build_check_repo.py
Function: automate code check in repository
"""

######################################

######################################

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
from time import sleep
import re
import logging
from importlib import import_module
import inspect

logging.basicConfig(filename='test.log', level = logging.INFO)

sys.path.append(os.path.dirname(__file__))

white_lists = ["resnet", "mobilenet", "inception", "utils", "aapackage" "util", "task_config"]
curr_os = "linux" if "Linux" in platform.platform() else "win"


class AutoCodeCheck:

    def __init__(self):

        self.folder_path = None
        self.repo_url = None
        self.repo_path = None

    def scan(self, data_file):
        files = glob.glob(data_file + "/**/*.py", recursive=True)
        files = [s for s in files if ".ipynb_checkpoints" not in s]
        logging.debug("scan files done ... ")
        return files

    def get_packages(self, file):
        with open(file, "r") as fp:
            contents = fp.read()

        packages = []
        for line in contents.strip().split("\n"):
            line = line.strip()
            if not line:
                continue

            if line[0] == "#":
                continue
            if "import " not in line:
                continue

            try:
                package = None
                if "from" in line:
                    line = line[line.index("from") + 4:].strip()
                    if "." in line:
                        package = line[: min(line.index("."), line.index(" "))]
                    else:
                        package = line[: line.index(" ")]
                else:
                    if "." in line:
                        line = line[line.index("import") + 6:].strip()
                        package = line[: line.index(".")]
                    else:
                        line = line[line.index("import") + 6:].strip()
                        package = line

                if " as " in package:
                    package = package[: package.index(" as ")]
                if ";" in package:
                    package = package[: package.index(";")].strip()
                if "," in package:
                    for p in package.strip().split(","):
                        packages.append(p.strip())
                else:
                    packages.append(package)
            except Exception as e:
                pass

        return packages

    def get_missing(self, all_packages):

        miss_package = []
        for package in all_packages:
            run_string = "import " + package

            try:
                exec(run_string)

            except Exception as e:
                miss_package.append(package)

        return miss_package

    def write_requirements(self, source_files):
        # check packages
        need_to_install_package_list = []
        for file in source_files:
            all_packages = self.get_packages(file)
            miss_packages = self.get_missing(all_packages)

            need_to_install_package_list.extend(miss_packages)

        # Clean Up
        ll = []
        for t in need_to_install_package_list:
            t = t.replace('"', " ").strip()
            t = s = re.sub('[^0-9a-zA-Z]+', ' ', t).strip()
            if " " not in t and len(t) > 2:
                ll.append(t)

        package_list = list(set(ll))

        package_list = [s for s in package_list if s]
        package_list = [
            s for s in package_list if not any([w in s for w in white_lists])
        ]
        package_list = list(set(package_list))

        logging.debug(package_list)
        print(len(package_list))

        with open("./require_before.txt", "w") as fp:
            fp.write("\n".join(package_list))

        return package_list

    def clone(self, url):
        reponame = url.split("/")[-1]
        # os.system( " cd '{folder}'  &&  git clone {url} ")
        self.repo_url = url
        self.repo_path = str(os.getcwd()) + "\\{}".format(reponame)
        print(self.repo_path)
        gitc = subprocess.Popen(['git', 'clone', str('{}').format(self.repo_url)])
        gitc.wait()
        # os.system("git clone {}".format(self.repo_url))

        sleep(5)

    def build_env(self):
        pref = f" activate test && " if curr_os == "win" else f" source activate test && "
        condax = f"conda install -n test   "
        print(pref)

        ############# Scan file recursively  ########################################
        source_files = self.scan(str(self.repo_path))
        print("all packages", source_files, flush=True)
        packages = self.write_requirements(source_files)

        # if arg.conda_env != "":
        os.system(f"conda create --yes  -n test  python=3.6.7")
        os.system(f"{pref}  {condax} -y  {packages} ")

        ss = " ".join(packages)
        os.system(f"{pref}  {condax} -y {ss}  --no-update-deps ")
        sleep(5)

        package_list = self.write_requirements(source_files)
        miss_packages = self.get_missing(package_list)
        for package in miss_packages:
            os.system(f"{pref}  {condax}  -y {package}   --no-update-deps   ")

        package_list = self.write_requirements(source_files)
        miss_packages = self.get_missing(package_list)

        for package in miss_packages:
            os.system(f"{pref}  pip install {package} --no-deps ")

        miss_packages = self.get_missing(packages)
        with open("./require_after.txt", "w") as fp:
            fp.write("\n".join(miss_packages))

        os.system(f" {pref}  conda list ")

    def verify_code(self):
        os.system("cd {}".format(self.repo_path))
        os.system("python main.py")

    def analyze(self):
        source_files = scan(".")
        print(source_files)
        for fil in source_files:
            # import_module(fil)
            fil = fil.split("\\")[-1]
            fil = fil.split(".")[0]
            print(inspect.getsource(fil))


def load_arguments():
    cur_path = os.path.dirname(os.path.realpath(__file__))
    p = argparse.ArgumentParser()
    p.add_argument("--repo_url", default="", help=".git")
    arg = p.parse_args()
    return arg


def main():
    argv = load_arguments()

    codecheck = AutoCodeCheck()
    codecheck.clone(argv.repo_url)
    sleep(5)
    codecheck.build_env()
    # codecheck.verify_code()
    # codecheck.analyze()

    return 0


if __name__ == '__main__':
    retval = main()
    exit(retval)












