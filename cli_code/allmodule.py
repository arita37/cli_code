# -*- coding: utf-8 -*-
"""  All module here for include  


"""
import copy
import math as mth
import os
import re
import sys
from calendar import isleap
from collections import OrderedDict
from datetime import datetime, timedelta

import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
import requests
import scipy as sci
from bs4 import BeautifulSoup
from matplotlib.collections import LineCollection

from aapackage import util
from tabulate import tabulate

# if  sys.platform.find('win') > -1  :
#  from guidata import qthelpers  #Otherwise Erro with Spyder Save


##### Pandas
# from pandas.types.dtypes import CategoricalDtype
# import  ggplot as gg


# import datanalysis as da, fast

#############################################################################################


#############################################################################################
# ---------------------  utilities           --------------------------------------------------
def pprint(table1, tablefmt="simple"):
    """To print nice column headers, supply the second argument (`headers`):
      - `headers` can be an explicit list of column headers
      - if `headers="firstrow"`, then the first row of data is used
      - if `headers="keys"`, then dictionary keys or column indices are used
    print(tabulate([[1, 2.34], [-56, "8.999"], ["2", "10001"]]))
  """
    # from tabulate import tabulate

    # if isinstance(table1, pd.DataFrame) :
    #  print tabulate(table1, headers="keys", tablefmt=tablefmt,
    #                floatfmt="g", numalign="decimal", stralign="left", missingval="")
    # else :
    #   print tabulate(table1, headers="keys", tablefmt=tablefmt,
    #               floatfmt="g", numalign="decimal", stralign="left", missingval="")


def pprint2(x):
    """import pprint
     stuff = ['spam', 'eggs', 'lumberjack', 'knights', 'ni']
stuff.insert(0, stuff[:])
pp = pprint.PrettyPrinter(indent=4)
pp.pprint(ALLDB)
  """
    import pprint

    pp = pprint.PrettyPrinter(indent=3)
    pp.pprint(x)


################## Unicode / UTF-8 Converter ###################################################################
def str_convert_beforeprint(x):
    """ #Before writing/output to printer put in utf-8 """
    try:
        return x.encode("utf-8")
    except:
        return x


def str_to_utf8(x):
    """ #Before writing/output to printer put in utf-8 """
    try:
        return x.encode("utf-8")
    except:
        return x


def str_to_unicode(x, encoding="utf-8"):
    """ #After Loading Text from CSV ---> Immediately in unicode """
    if isinstance(x, str):
        if not isinstance(x, str):
            x = str(x, encoding)
            return x
    else:
        return x
