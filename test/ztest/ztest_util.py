# -*- coding: utf-8 -*-
# from __future__ import division
# ssfrom __future__ import print_function


#####################################################################################################
import os
import sys

import numpy as np
import pandas as pd
import scipy as sci

import arrow

DIRCWD = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
os.chdir(DIRCWD)
sys.path.append(DIRCWD + "/aapackage")
print(DIRCWD)


##############################################################################################
############################ UNIT TEST #######################################################
if __name__ == "__main__":
    import argparse

    ppa = argparse.ArgumentParser()  # Command Line input
    ppa.add_argument("--do", type=str, default="action", help="test / test02")
    arg = ppa.parse_args()


if __name__ == "__main__" and arg.do == "test":
    print(__file__, DIRCWD)
    try:
        import util

        UNIQUE_ID = util.py_log_write(DIRCWD + "/aapackage/zlog/ztest_log_all.txt", "util")

        ###########################################################################################
        import util

        print(util)
        print("")
        # util.a_info_system()
        util.a_isanaconda()
        util.date_allinfo()

        vv = np.random.rand(1, 10)
        mm = np.random.rand(100, 5)
        df1 = pd.DataFrame(mm, columns=["aa", "bb", "c", "d", "e"])

        # util.pd_createdf(mm, ["aa", "bb", 'c', 'd', 'e'],  )
        print(util.np_sort(vv))

        util.save(df1, "ztest_df")
        df2 = util.load("ztest_df")

        ###########################################################################################
        print(
            "\n\n"
            + UNIQUE_ID
            + " ###################### End:"
            + arrow.utcnow().to("Japan").format()
            + "###########################"
        )
        sys.stdout.flush()
    except Exception as e:
        print(e)


"""
  try :

  except Exception as e: print(e)


import numpy as np, arrow
UNIQUE_ID=    str(np.random.randint(10**14, 10**15,  dtype='int64'))


print("\n\n###################### Start util # :" + arrow.utcnow().to('Japan').format() + "###########################") ; sys.stdout.flush()
 
 
"""
