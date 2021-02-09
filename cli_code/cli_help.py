"""
Display help about different commands for many commonly used cli tools like bash, docker, conda etc.
Easily lookup help for a given command or get a brief overview of commands available 

Usage:

cli_help bash -c ls cut

# display a long list of commands available in docker
cli_help docker -l

"""
import sys
import os
import datetime
from pprint import pprint

from fuzzywuzzy import fuzz
from fuzzywuzzy import process
##############################################################################################

help_files = {
    'bash': "cli_code\\help\\bash.txt",
    'docker': "cli_code\\help\\docker.txt",
    'conda': 'cli_code\\help\\conda.txt'
}


def get_docs(tool):
    """
    Retrieve the help file for the specified tool and 
    return as a text file.
    """
    help_file = help_files[tool]

    # help_file = os.path.join("help", tool,
    try:
        with open(help_file, encoding="utf-8") as hf:
            return hf.read()
    except OSError as err:
        print(err)
        sys.exit(1)


def get_cmd_help(tool_docs, commands):
    """
    Searches for commands in documentaion and returns help text.
    """
    # TODO: Put start and stop markers in help files, so that
    # TODO: we can easily returen a section coressponding to cmd

    # rst contains tuple, first element is line match and second is match ratio
    cmd_help = {}
    for cmd in commands:
        cmd_help[cmd] = []
        rst = process.extract(cmd, tool_docs.splitlines(), limit=100)

        for line in rst:
            if "-" in line[0] and len(line[0]) < 60:
                cmd_help[cmd].append(line[0])

    return cmd_help


def load_arguments():
    """
    Parse the arguments
    """
    import argparse

    p = argparse.ArgumentParser(
        description="Utility to quickly and consicely get help about different commands in different tools")
    p.add_argument("tool", default="bash",
                   help="specify the tool for which you want to lookup commands")
    p.add_argument("--cmd", "-c", default=None, nargs='+',
                   help="Specify command(s) to lookup for the mentioned tool")

    arg = p.parse_args()
    return arg


def main():
    args = load_arguments()

    # tool is any piece of software for which we want to lookup help
    tools_available = ['bash', 'docker', 'conda']
    tool_name = args.tool
    cmd2check = args.cmd

    # before goining forward, let's check we have the docs
    assert tool_name in tools_available, f"Docs not available for {tool_name}"

    docs = get_docs(tool_name)
    cmd_help = get_cmd_help(docs, cmd2check)
    pprint(cmd_help)


if __name__ == "__main__":
    main()
