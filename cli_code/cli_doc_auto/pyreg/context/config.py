#!/usr/bin/env python

import os
import re
import sys


SRCDIR = None
EXT = None
OUT = None
FILTER = None
TAB_SPACE = None


def _exact_filepath(path):
    if not isinstance(path, str):
        return None

    if not (path.startswith('/') or path.startswith('.')):
        path = './{}'.format(path)

    return os.path.abspath(os.path.expanduser(os.path.expandvars(path)))


def init(cliargs):
    global SRCDIR
    global EXT
    global OUT
    global FILTER
    global TAB

    # src directory
    SRCDIR = _exact_filepath(cliargs['dir_in'])
    if not os.path.isdir(SRCDIR):
        print('invalid source directory')
        sys.exit(1)

    # extensions
    EXT = list(map(lambda x: '.{}'.format(x), map(lambda x: re.sub(
        r'[^\w\d]', '', x), filter(lambda x: x, cliargs['ext']))))

    # fnmatch pattern
    FILTER = cliargs['filter']

    # output
    OUT = cliargs['dir_out']

    TAB = cliargs['tab']
