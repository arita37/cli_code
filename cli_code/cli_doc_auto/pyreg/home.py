# -*- coding: utf-8 -*-

import os
import logging


from ..pyreg.manager import fs
from ..pyreg.manager import regex
from ..pyreg.context import config


LOGGER = logging.getLogger(__name__)


def execute(cliargs):
    config.init(cliargs)

    print(config.SRCDIR)

    sources = fs.list_source_files(config.SRCDIR)
    print(sources)
    sources = fs.filter_by_pattern(sources, config.FILTER)

    regex.analyze(sources)

    try :
       to_text_format()
    except :
        pass


def to_text_format():
    prefix_path = "D:\\_devs\\Python01\\gitdev\\mlmodels\\"
    # Clean formatting
    with open(config.OUT, mode='r') as f:
         ll = f.readlines()

    ll2 = []
    for line in ll:
         line = line.replace(prefix_path, "")
         ll2.append(line)

    with open(config.OUT + ".py", 'w') as f:
         f.write(''.join(ll2))



def to_html_format():
    pass
    # ###### HTML tag  ####################################################
    # head = """
    # <html>
    # <body>

    # """

    # end = """

    # </body>
    # </html>

    # """

    # pref = "<a href='     '>       </a>"
    # ll3 = []
    # for line in ll2:
    #     if "mlmodels\\" in line:
    #         line2 = line.replace("\\", "//")
    #         url = f"https://github.com/arita37/mlmodels/tree/dev/{line2}"

    #     if not "\\raw\\" in url and not "archive" in url:
    #         #line = f"<a href='{url}' target='_blank' >{line}</a><br>"
    #         line = f"[{line}]({url})\n"

    #         ll3.append(line)

    # with open(config.OUT + ".md", 'w') as f:
    #     f.write(head)
    #     f.write('\n'.join(ll3))
    #     f.write(end)
