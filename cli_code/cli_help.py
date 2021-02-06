"""


Display Helpher matching command

Usage:

cli_format -i /path/to/file or /path/to/dir --out_dir /path/to/output

"""
import re
import glob
import fire
import os
import tqdm
import datetime
##############################################################################################

ddict = {
  'bash': "help/bash.txt",
  'docker' : "help/bash.txt",

  'conda' :'help/conda.txt'

}



def get_doc(cmd):
   """
    bash copy

   """
    cmds = cmd.split(" ")

    if 'bash' in cmds[0] :
        open(file)

        extract lines with  cmds[1]  keywords
        display on screen

    if 'docker' in cmds[0] :



def load_arguments():
    """
    Parse the arguments
    """
    import argparse

    p = argparse.ArgumentParser(description="")
    p.add_argument("--cmd", "-i", required='True',
                   default="bash",  help="commmand")

    p.add_argument("--cmd", "-i", required='True',
                   default="bash",  help="commmand")

    arg = p.parse_args()
    return arg

# TODO: Add functions for formating functions and dictionaries


def main():
    args = load_arguments()

    cmd = args.cmd

    from prettyprint import print as print2

    txt = get_doc(cmd)
    pritn2(txt)


if __name__ == "__main__":
    main()
