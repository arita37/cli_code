#!/usr/bin/env python

import os 
import logging


from pyreg.manager import fs
from pyreg.manager import regex 
from pyreg.context import config



LOGGER = logging.getLogger(__name__)

def execute(cliargs):
    config.init(cliargs)


    sources = fs.list_source_files(config.SRCDIR) 
    print(sources)
    sources = fs.filter_by_pattern(sources, config.FILTER) 


    regex.analyze(sources)

