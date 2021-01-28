mkdir test_out

# check cli_convert_ipynb by converting a notebokk in test
python   cli_code/cli_convert_ipynb.py   --in_folder  test/  --out_folder  test_out/


# check cli_download by downloading from a link
python   cli_code/cli_download.py -u https://drive.google.com/file/d/1FPn4Q4PClobHgEU4DglyF2Xbs5Boe1r_/view?usp=sharing -o test_out/


# this one requires git and conda installed on runner
python   cli_code/cli_repo_check.py https://github.com/parul1931/walmart.git -n testing


# check cli_conda_merge by joining two test conda env files
python   cli_code/cli_conda_merge.py test/file0.yml test/file1.yml


# check cli_module_parser by parsing .py files in test dir
python   cli_code/cli_module_parser.py test/ -o test_out/module_parsed.csv


# check cli_env_autoinstall by creating an environemnt for test repo
python   cli_code/cli_env_autoinstall.py test/ -n notebook_cvt


# check cli_github_search by searching for some keywords
python   cli_code/cli_github_search.py amazon scraper -o test_out/

# check cli_doc_auto by parsing .py files in test dir
python cli_code/cli_doc_auto/main.py test/ -o test_out/docs.txt

# check cli_format2.py by parsing test/run_train.py file
python cli_code/cli_format2 --in_file=test/run_train.py --out_dir=test_out