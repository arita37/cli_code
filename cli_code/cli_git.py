"""


cli_git.py --do git_pull

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

#logging.basicConfig(filename='test.log', level = logging.INFO)



curr_path= sys.path.append(os.path.dirname(__file__))
curr_os = "linux" if "Linux" in platform.platform() else "win"








#############################################################################################
#    1)   git clone repoURL   ###############################################################
def git_pull() :

  folder_list = [
    r"/_devs/Python01/gitdev/_rl_hoken",
    r"/_devs/Python01/gitdev/__generator",
    r"/_devs/Python01/gitdev/cli_code",
    r"/_devs/Python01/gitdev/mlmodels",
    r"/_devs/Python01/gitdev/json_api",



  ]
  for f in folder_list :
    # f = os.path.join(f, "")
    # print(f)
    # os.system(  r"cd /_devs/Python01/gitdev/cli_code/cli_code && git pull --all" ) 
    #os.system(  f"cd {f} " ) 
    cmd = f"d: && cd {f} && git pull --all"
    print(cmd)
    os.system(  cmd  ) 

















#############################################################################################
def load_arguments():
    cur_path = os.path.dirname(os.path.realpath(__file__))
    p = argparse.ArgumentParser()
    p.add_argument("--do", default="git_pull", help=".git")
    p.add_argument("--repo_name", default="", help=".git")
    p.add_argument("--folder", default="", help=".git")
    arg = p.parse_args()
    return arg




if __name__ == '__main__':
    arg = load_arguments()

    if arg.do == "git_pull" :
      git_pull()
 







