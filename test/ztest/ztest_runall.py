# -*- coding: utf-8 -*-
from __future__ import division, print_function

import os
import sys

import numpy as np
import pandas as pd
import scipy as sci

from attrdict import AttrDict as dict2

# CFG   = {'plat': sys.platform[:3]+"-"+os.path.expanduser('~').split("\\")[-1].split("/")[-1], "ver": sys.version_info.major}
# DIRCWD= {'win-asus1': 'D:/_devs/Python01/project27/', 'win-unerry': 'G:/_devs/project27/' , 'lin-noel': '/home/noel/project27/', 'lin-ubuntu': '/home/ubuntu/project27/' }[CFG['plat']]
os.chdir(DIRCWD)
sys.path.append(DIRCWD + "/aapackage")



try:
    import util

    print(util)
    util.a_info_system()
    util.isanaconda()
    util.date_allinfo()

    vv = np.random.rand(1, 10)
    mm = np.random.rand(100, 5)

    # util.pd_createdf(mm, ["aa", "bb", 'c', 'd', 'e'],  )

    print(util.np_sort(vv))


except Exception as e:
    print(e)


"""
import tensorflow as tf, numpy as np, pandas as pd, sys, os, argparse, arrow; from tabulate import tabulate
import util_min, util_ml as util_ml




import util
"""


############### util    ####################################################################
"""
Regression test : generate meta data of function

package_name, 
name,     aws_function
name_type1, 
name_type2, 
name_type3, 
name_comment
name_doc


arg_name, 
arg_type1, 
arg_default,
arg_comment, 


from . import util

"""
