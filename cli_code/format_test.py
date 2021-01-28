import re

regex1 = r"^#{3,}$"
regex2 = r"^#+ (\w+) .+#$"
regex3 = r"log\(\"#+ (.*) #+\"\)"
regex4 = r"^import[\s\w]+?(?=from|^\s*$)"

test_str1 = "#########"
test_str2 = "########## TEST ################"
test_str3 = 'log("#### Data preparation #########################################################")'
test_str4 = '''
import importlib
import json
import os
import sys

import argparse
import pandas
from run_preprocess import preprocess, preprocess_load
from util_feature import load, save_list, load_function_uri, save
import warnings
import numpy
from PIL import Image
'''

subst1 = "#"*100
res2 = re.search(regex2, test_str2)
subst2 = r'#### \g<1> ' + '#'*(100-6-len(res2.group(1)))
res3 = re.search(regex3, test_str3)
subst3 = r'log("#### \g<1> ' + '#'*(100-6-len(res3.group(1))) + '")'
res4 = re.findall(regex4, test_str4, re.MULTILINE)
print(res4)
# for imp_group in res4:
#     pattern = r"import (\w+)"
#     ind_imports = re.findall(pattern, imp_group)
#     subst4 = r"import " + ", ".join(ind_imports)


def subst4(match_obj):
    pattern = r"import (\w+)"
    ind_imports = re.findall(pattern, match_obj.group(0))
    return r"import " + ", ".join(ind_imports) + "\n"


print("comment which start with 3 or more # and have no text")
print(test_str1)
print(re.sub(regex1, subst1, test_str1, 0, re.MULTILINE))
print("comment which start with 3 or more # and have text in it")
print(test_str2)
print(re.sub(regex2, subst2, test_str2, 0, re.MULTILINE))
print("formatting log statements")
print(test_str3)
print(re.sub(regex3, subst3, test_str3, 0, re.MULTILINE))
print("each of the three result above generates total 100 characters including text")
print(test_str4)
print(re.sub(regex4, subst4, test_str4, 0, re.MULTILINE))
