```
Utilities to analyze python code
Tools for Python Doc Generation, Tool analysis, Package Auto Install, Converter


#### Install for usage
pip install cli_code


#### Install for dev
cd YourFolder
git clone  https://github.com/arita37/cli_code.git
cd cli_code
pip install -e .



############### CLI Command
    "cli_docs        =  cli_code/cli_doc_auto/main.py",    Auto generate Documentation fron source code    


    "cli_repo_docs        =  cli_code/cli_docs.py",    Auto generate Documentation fron source code    
    
    "cli_env_autoinstall  =  cli_code/cli_env_autoinstall.py",  Auto generate from parsing source code.

    "cli_convert_ipny     =  cli_code/cli_convert_ipny.py",     Convert a folder of notebook to python script

    "cli_repo_check       =  cli_code/cli_repo_check.py",       Check a repo.

    "cli_conda_merge      =  cli_code/cli_conda_merge.py",      Merge a repo.




############## cli_env_autoinstall   ########################################################
Auto-install environnment by parsing the code source "import "

cli_env_autoinstall 
      --folder_input  /home/ubuntu/aagit/aapackage/aapackage/batch  
      --python_version "3.6.7"
      --packages "tensorflow=1.14  scikit-learn numpy pandas scipy matplotlib"





############## cli_docs      ################################################################
Generate doc of a repo by parsing the code source string
cli_docs
    client/yakinoe/pyreg/dataset/requests/
    -vvv     : very verbose
    --tab    : 4    indendation
    --out    : docs.txt   output docs
    --filter : ".*?api.py"   Fitlering files


produces 3 files in the current folder
    1. documentation
    2. classes.json
    3. functions.json

usage:
    cli_docs D:\_devs\Python01\gitdev\cli_code -vvv --tab 4 --out docs.txt
    python main.py client/yakinoe/pyreg/dataset/requests/ -vvv --tab 4 --out docs.txt 











#### Tests:
  cd  cli_code\cli_code
  cli_code>python cli_docs.py --do test   







```




