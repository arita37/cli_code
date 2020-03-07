#!/bin/sh

conda create -n testenv --yes  --file zbuild/py36.txt
source activate testenv
pip install arrow==0.10.0 attrdict==2.0.0 backports.shutil-get-terminal-size==1.0.0 configmy==0.14.87 github3.py==1.2.0 jwcrypto==0.6.0 kmodes==0.9 rope-py3k==0.9.4.post1 tables==3.3.0 tabulate==0.8.2 uritemplate==3.0.0


conda install -c conda-forge  pygmo  pagmo
pip install dcgpy    

