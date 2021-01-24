#!/usr/bin/env python

"""
Takes a source dir as a positional argument.

Produces 3 files:

    1. documentation
    2. classes.json
    3. functions.json

usage:

python main.py client/yakinoe/pyreg/dataset/requests/ -vvv --tab 4 --out docs.txt
python main.py client/yakinoe/pyreg/dataset/requests/ -vvv --tab 4 --out docs.txt --filter ".*?api.py"
"""

import logging
import argparse
import sys
#from cli_code.cli_doc_auto.lib.common.argparse import cli
#from cli_code.cli_doc_auto.pyreg import home


from pyreg import home


def get_arguments():
    p = argparse.ArgumentParser(description="Produces documentation of python modules given a directory")
    p.add_argument('srcdir',   help='Relative or absolute directory path that contains .py files')
    p.add_argument('--out', '-o',  default='docs.txt', help='Relative or absolute output file location')
    p.add_argument('--ext', nargs='+', default=['py'], help='Extensions of python source files to be analyzed by regex')
    p.add_argument('--filter', help='regex patterns to MATCH from srcdir. ie: ".*?api.py"', nargs='*', default=[], )
    p.add_argument('--tab', '-t', default=None, type=int, help='tabs with spaces')
    p.add_argument('--verbosity', '-v', action='count', default=None, dest='verbosity',
                   help='Verbosity level. dense: -vvvvv, sparse: -v')

    args = p.parse_args()
    return args


def get_logger(verbosity=0):
    logfile = "logs.txt"
    log_format = (
        '[%(asctime)s] %(levelname)-6s %(name)-12s %(message)s'
    )
    VERBOSITY = [
        None,
        logging.CRITICAL,
        logging.ERROR,
        logging.WARN,
        logging.INFO,
        logging.DEBUG,
    ]
    logging.basicConfig(
        level=VERBOSITY[verbosity],
        format=log_format,
        handlers=[
            logging.FileHandler(logfile),
            logging.StreamHandler(sys.stdout),
        ]
    )
    # get a logger
    logger = logging.getLogger(__name__)
    return logger


def main():

    VERBOSITY = [
        None,
        logging.CRITICAL,
        logging.ERROR,
        logging.WARN,
        logging.INFO,
        logging.DEBUG,
    ]

    args = get_arguments()
    # providing same api as the previous cli interface
    args = vars(args)

    logfile = "logs.txt"
    log_format = (
        '[%(asctime)s] %(levelname)-6s %(name)-12s %(message)s'
    )

    if args['verbosity']:
        logging.basicConfig(
            level=VERBOSITY[args['verbosity']],
            format=log_format,
            handlers=[
                logging.FileHandler(logfile),
                logging.StreamHandler(sys.stdout),
            ]
        )

    home.execute(args)


if __name__ == "__main__":
    main()
