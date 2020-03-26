# -*- coding: utf-8 -*-

import os 
import logging


from pyreg.manager import fs
from pyreg.manager import regex 
from pyreg.context import config



LOGGER = logging.getLogger(__name__)

def execute(cliargs):
    config.init(cliargs)

    print(config.SRCDIR)
  

    sources = fs.list_source_files(config.SRCDIR) 
    print(sources)
    sources = fs.filter_by_pattern(sources, config.FILTER) 


    regex.analyze(sources)

    #### Clean formatting
    with open( config.OUT, mode='r') as f :
    	ll = f.readlines()

    ll2 = []
    for line in ll :
    	line = line.replace("D:\\_devs\\Python01\\gitdev\\mlmodels\\"  , "")
    	ll2.append(line)
    
    with open(config.OUT, 'w') as f:
       	f.write(''.join(ll2))       	


