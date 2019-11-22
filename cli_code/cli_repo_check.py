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


#  1)   git clone repoURL
#  2)  Build conda env from source code parsing
   # cd repo
# https://github.com/arita37/cli_code/blob/master/cli_code/cli_module_autoinstall.py
   
   
# 3) Launch all files in root (main.py) with subprocess to check if running
    # Log error messages on disk
 
# 4) Parse source code with  import inspect and generate signature for each functiom
  #  Write on disk
   # https://github.com/arita37/cli_code/blob/master/cli_code/cli_module_analysis.py

File: cll_build_check_repo.py
Function: automate code check in repository


"""


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

#sys.path.append(os.path.dirname(__file__))

white_lists = ["resnet", "mobilenet", "inception", "utils", "aapackage" "util", "task_config"]
curr_os = "linux" if "Linux" in platform.platform() else "win"




##################################################################################
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



def os_scan(folder, recursive=True):
    # note: I have checked os_file_listall, I think the following will be better
    files = glob.glob(folder + "/**/*.py", recursive=recursive)
    # remove .ipynb_checkpoints
    files = [s for s in files if ".ipynb_checkpoints" not in s]

    # print("scan files done ... ")
    return files







#############################################################################################
#    1)   git clone repoURL   ###############################################################
def git_clone(url, folder) :
	print( os_system(  ["git", "clone", "folder"] ) )










#############################################################################################
# 2)  Build conda env from source code parsing   ############################################
def repo_build_conda(folder) :
  """
  # cd repo
  # https://github.com/arita37/cli_code/blob/master/cli_code/cli_module_autoinstall.py
   cli_module_autoinstall.py


  """	
   
   
 








#############################################################################################
def repo_check_root_files(folder) :
  """
  # 3) Launch all files in root (main.py) with subprocess to check if running
    # Log error messages on disk
   



  """
  #Only root file
  file_list = os_scan(folder, recursive=False)

  for file in file_list :
  	msg = os_system(["python ", file ])
    if "error" in msg :
       print(msg)







def repo_generate_signature(folder) :
   """
     Generate signature from the code


   """
   msg = os_system(["python ", "cli_module_generate_docs.py ",  "args" ])





#############################################################################################
def load_arguments():
    cur_path = os.path.dirname(os.path.realpath(__file__))
    p = argparse.ArgumentParser()
    p.add_argument("--repo_url", default="", help=".git")
    p.add_argument("--repo_name", default="", help=".git")
    p.add_argument("--folder", default="", help=".git")
    arg = p.parse_args()
    return arg




if __name__ == '__main__':
    arg = load_arguments()

    reponame  = arg.url_repo.split("/")[-1]
    folder = arg.folder + "/" + arg.repo_name

    git_clone(arg.url, arg.folder, reponame)


    repo_build_conda(folder)


    repo_check_root_files(folder)


    repo_generate_signature(folder)











