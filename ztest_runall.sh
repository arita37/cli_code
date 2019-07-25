cd /d d:\_devs\Python01\project27\aapackage



#### py36 tests   ######################################################
source activate py36
python  ztest/ztest_import.py    >> zlog/ztest_py36_import.txt 2>>&1

python  ztest/ztest_util.py    >> zlog/ztest_py36_util.txt 2>>&1





#### py27 tests   ######################################################
source activate py27
python  ztest/ztest_import.py    >> zlog/ztest_py27.txt 2>>&1

python  ztest/ztest_util.py    >> zlog/ztest_py27_util.txt 2>>&1



