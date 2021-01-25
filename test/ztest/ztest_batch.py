#!/bin/python
"""

Test to run _batch module:

might need arguments to run this:

$python ztest_batch.py --hyperparam hyperparams.csv --optimizer optimizer.py --directory _batch



"""
import _batch

# EXECUTE FROM CMD ARGS;
# _batch.execute_batch(krepeat=1)

# EXECUTE FROM CURRENT ARGS;
_batch.build_execute_batch("hyperparams.csv", "_batch", "_batch/optimizer.py", "")
