# -*- coding: utf-8 -*-
"""
Auto install missing package by scanning error message


conda create -y -n ztest  python=3.6.5
source activate Emptyconda




python cli_module_autoinstall.py  --folder_input  /home/ubuntu/aagit/aapackage/aapackage/batch  ----packages "tensorflow=1.14  scikit-learn numpy pandas scipy matplotlib"



### tobe visible in jputer
conda install ipykernel 


"""

import sys, os
import glob
# from IPython.nbformat import current as nbformat
# from IPython.nbconvert import PythonExporter
# import nbformat
# from nbconvert import PythonExporter
# from tqdm import tqdm
from time import sleep
import re

import platform

#### Not to install
white_lists = ["resnet", "mobilenet", "inception", "utils", "aapackage" "util", "task_config"]
curr_os = "linux" if "Linux" in platform.platform() else "win"






def setup_env(folder, url) :
    reponame = url.split("/")[-1]
    os.system( " cd '{folder}'  &&  git clone {url} ")
    foldert = folder + "/" + reponame 
    
    ll  = []
    for x in  ["requirements.txt", "requirement.txt"] :
      try :  
        with open(foldert + "/" +x , mode="r" ) as f :
           ll = f.readlines()
      except : pass

    pkgs = " ".join(ll) ll is not None else  " pandas "
    

    arg = { "folder_input" : foldert
      ,"conda_env" : "ztest" 
      ,"python_version" :  "3.6.7" 
      ,"packages" : pkgs
    }


    os.system( " conda remove -n ztest" )    

    run(arg)

    os.system( " conda export -n ztest" )    
    os.system( " conda export -n ztest" )    




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



def scan(data_file):
    # note: I have checked os_file_listall, I think the following will be better
    files = glob.glob(data_file + "/**/*.py", recursive=True)
    # remove .ipynb_checkpoints
    files = [s for s in files if ".ipynb_checkpoints" not in s]

    print("scan files done ... ")
    return files



def get_packages(file):
    ### get package name from python code source
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



def get_missing(all_packages ):
    # # form import XX,XX,XX
    # run_string = 'import '+ ','.join(all_packages)
    # # maybe cd to the dir

    miss_package = []
    for package in all_packages:
        run_string = "import " + package

        #cmds = [ f"{prefix}  python -c ", "'import  %s '" % package]
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

    #### Clean Up
    ll = []
    for t in need_to_install_package_list :
        t = t.replace('"', " ").strip()
        t = s = re.sub('[^0-9a-zA-Z]+', ' ', t).strip()
        if " " not in t and len(t) > 2 :
          ll.append(t)


    package_list = list(set(ll))
    # print(package_list)
    # print(len(package_list))

    package_list = [s for s in package_list if s]
    package_list = [
        s for s in package_list if not any([w in s for w in white_lists])
    ]
    package_list = list(set(package_list))

    print(package_list)
    print(len(package_list))

    with open("./require_before.txt", "w") as fp:
        fp.write("\n".join(package_list))

    return package_list



def os_exec(x) :
    print(x)
    os.system(x)



####################################################################################
def load_arguments():
    """
       --param_file /zs3drive/config_batch.toml --param_mode test_launch
  """
    import argparse

    cur_path = os.path.dirname(os.path.realpath(__file__))
    config_file = os.path.join(cur_path, "config.toml")

    p = argparse.ArgumentParser()
    p.add_argument("--folder_input", default="D:/_devs/Python01/gitdev/cli_code/cli_code/", help="Params File")
    p.add_argument("--conda_env", default="test", help="Params File")
    p.add_argument("--python_version", default="3.6.7", help="Params File")
    p.add_argument("--packages", default="tensorflow=1.14  scikit-learn numpy pandas scipy matplotlib", help="Params File")

    p.add_argument("--mode", default="test", help=" test/ prod /uat")
    arg = p.parse_args()
    return arg



def Run(arg):

    pref = f" activate {arg.conda_env} && " if curr_os == "win" else f" source activate {arg.conda_env} && "
    condax = f"conda install -n {arg.conda_env}   "
    print(pref)


    ############# Scan file recursively  ########################################
    source_files = scan(arg.folder_input)
    print("all packages", source_files, flush=True)
    print( write_requirements(source_files), flush=True )



    ############# Conda Env  ####################################################
    if arg.conda_env != "" :
       os_exec( f"conda create --yes  -n {arg.conda_env}  python={arg.python_version}"  )


    ############# Conda Default #################################################
    os_exec( f"{pref}  {condax} -y {arg.packages}  " )



    ############# Auto install conda install in Group   #########################
    package_list = write_requirements(source_files )
    ss =  " ".join(package_list)
    os_exec( f"{pref}  {condax} -y {ss}  --no-update-deps " )
    sleep(5)


    ########### Auto install conda individually  ################################
    #package_list = write_requirements(source_files)
    miss_packages = get_missing(package_list )
    for package in miss_packages :
        os_exec( f"{pref}  {condax}  -y {package}   --no-update-deps   " )



    ########### Auto install pip  ###############################################
    # package_list = write_requirements(source_files)
    miss_packages = get_missing(package_list )

    for package in miss_packages :
        os_exec( f"{pref}  pip install {package} --no-deps " )


    # check again   #############################################################
    miss_packages = get_missing(package_list )
    with open("./require_after.txt", "w") as fp:
        fp.write("\n".join(miss_packages))

    os_exec( f" {pref}  conda list ")



def main():
    print(os)
    print(curr_os)
    arg = load_arguments()
    Run(arg)


#################################################################################
#################################################################################
if __name__ == "__main__":
   main()




