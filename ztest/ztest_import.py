# -*- coding: utf-8 -*-
from __future__ import division, print_function

import calendar
import copy
import gc
import math as mth
import os
import re
import shutil
import sys
import time
from builtins import map, next, object, range, str, zip
from calendar import isleap
from collections import OrderedDict
from datetime import datetime, timedelta

import IPython
import matplotlib.pyplot as plt
import numba
############################################################################################
import numpy as np
import pandas as pd
import requests
import scipy as sci
import sklearn as sk
import urllib3
from bs4 import BeautifulSoup
from dateutil import parser
from future import standard_library
from numba import float32, float64, int32, int64, jit
from past.builtins import basestring
from past.utils import old_div

import arrow
import regex
import tensorflow as tf
# import util_search
# import fast
############################################################################################
from aapackage import (allmodule, datanalysis, function_custom, globalvar, portfolio, util,
                       util_aws, util_ml, util_release, util_spark, util_sql, util_web)
from attrdict import AttrDict as dict2
from tabulate import tabulate

standard_library.install_aliases()

############################################################################################
print("Start")















# import rstatpy







############################################################################################
try:
    import matplotlib.pyplot as plt
    from matplotlib.collections import LineCollection

except Exception as e:
    print(e)


############################################################################################
print("Success")


print([x for x in globals().keys() if x[0] != "_"])


############################################################################################
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
