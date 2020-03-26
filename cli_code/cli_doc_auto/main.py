#!/usr/bin/env python

"""

"""

DESC = """
takes a source dir as a positional argument.



produces 3 files:

    1. documentation
    2. classes.json
    3. functions.json

usage:
    python main.py client/yakinoe/pyreg/dataset/requests/ -vvv --tab 4 --out docs.txt
    python main.py client/yakinoe/pyreg/dataset/requests/ -vvv --tab 4 --out docs.txt --filter ".*?api.py"

"""

import logging

#from cli_code.cli_doc_auto.lib.common.argparse import cli
#from cli_code.cli_doc_auto.pyreg import home



from lib.common.argparse import cli
from pyreg import home


def main():
    cliargs = cli.CLI( description=DESC )\
            .add('srcdir',   help='relative or absolute directory path that contains .py files')\
            .add('--out',    help='relative or absolute output file location', default='docs.txt')\
            .add('--ext',    help='extensions of python source files to be analyzed by regex', nargs='+', default=['py'], )\
            .add('--filter', help='regex patterns to MATCH from srcdir. ie: ".*?api.py"', nargs='*', default=[], )\
            .add('--tab',    help='tabs with spaces', default=None, type=int)\
            .add('-v', '--verbosity', help='verbosity level. dense: -vvvvv, sparse: -v', dest='verbosity', action='count', default=None)\
            .build()

    VERBOSITY = [
            None,
            logging.CRITICAL,
            logging.ERROR,
            logging.WARN,
            logging.INFO,
            logging.DEBUG,
            ]

    if cliargs['verbosity']:
        logging.basicConfig(level=VERBOSITY[cliargs['verbosity']])

    home.execute(cliargs)


if __name__ == "__main__":
    main()


