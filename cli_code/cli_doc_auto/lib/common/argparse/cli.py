#!/usr/bin/env python

import sys
import argparse

"""

snippets:

.add('--crawl', dest='crawl', action='append', default=[])\
.add('--refetch', dest='refetch', action='store_true')\

.sub('init')\
    .add('dbname', help='ie:"local" or "myapp00.myservice"')\
    .add('configpath', nargs='?', default=None)\
    .add('extpath', nargs='?', default=None)\
    .pack()\
.sub('destroy_server')\
    .add('serverdir', help='ie: "myapp00"')\
    .pack()\

"""

class CLIComponent(object):
    def on_update_cli(self, cli):
        """
        meant to be implemented within extending components

        ie: lib.common.unittest.picker.TestPicker:
        def on_update_cli(self, cli):
            cli.update(self, '--pick', dest='pick', default=None, help='--pick @<testcase_class>:<test_routine_name>')
        
        ie: lib.common.logging.formatter.LoggingFormatter:
        def on_update_cli(self, cli):
            cli.update(self, '-v', '--verbosity', dest='verbosity', action='count', default=None)
        """
        raise NotImplementedError()

    def on_cli_arg(self, key, value):

        """
        called when CLI instance parsed a value that is related with a component. 
        
        ie: lib.common.unittest.picker.TestPicker:
        def on_cli_arg(self, key, value):
            if key == 'pick':
                self.set_selection(value)

        

        ie: lib.common.logging.formatter.LoggingFormatter:
        
        def on_cli_arg(self, key, value):
            setattr(self, key, value)
        
        @property
        def verbosity(self):
            return self._verbosity

        @verbosity.setter
        def verbosity(self, verbosity):
            .
            .
            .
        """
        raise NotImplementedError()




class CLI(object):
    SUBCOMMAND_DEST = 'command'


    def __init__(self, components=(), description=None, add_help=True):
        self.rules    = []
        self.subrules = {}
        self.cliargs  = None
        self.parser   = argparse.ArgumentParser(description, add_help=add_help)

        self.argnames         = {}
        self.subparser        = {}
        self.subparsers       = None
        self.subparser_latest = None

        self.components = {}
        for component in components:
            self.components[component] = []
            component.on_update_cli(self)

    def _obtain_flag_dest(self, *args, **kwargs):
        dest = kwargs.get('dest', None)
        if dest:
            return dest

        for arg in args:
            if arg.startswith('--'):
                return arg.replace('--', '')
        
        for arg in args:
            if arg.startswith('-'):
                return arg.replace('-', '')

    def __getitem__(self, key):
        return getattr(self.cliargs, key, None)

    def __str__(self):
        return str(self.cliargs)

    def update(self, component, *args, **kwargs):
        self.add(*args, **kwargs)

        dest = self._obtain_flag_dest(*args, **kwargs)
        self.components[component].append(dest)

    def add(self, *args, **kwargs):
        if self.subparser_latest:
            self.subrules[self.subparser_latest].append( (args, kwargs) )
        else:
            self.rules.append( (args, kwargs) )

        return self

    def sub(self, name):
        if not self.subparsers:
            self.subparsers = self.parser.add_subparsers(dest=self.SUBCOMMAND_DEST)

        if self.subparser_latest:
            self.pack()

        self.subrules[name]   = []
        self.subparser[name]  = self.subparsers.add_parser(name)
        self.subparser_latest = name

        return self

    def pack(self):
        if not self.subparser_latest:
            raise ValueError('Call .sub("<name>") first.')

        self.argnames[self.subparser_latest] = []

        for rule in self.subrules[self.subparser_latest]:
            self.subparser[self.subparser_latest].add_argument(*rule[0], **rule[1])

        self.argnames[self.subparser_latest] = []
        for action in self.subparser[self.subparser_latest]._actions:
            if action.dest == 'help':
                continue
            self.argnames[self.subparser_latest].append(action.dest)

        self.subparser_latest = None
        return self 

    def getargs(self, *args):
        return [ getattr(self.cliargs, arg) for arg in args if arg] 

    def build(self, *components):
        if self.subparser_latest:
            self.pack()

        for rule in self.rules:
            self.parser.add_argument(*rule[0], **rule[1])

        self.cliargs = self.parser.parse_args( sys.argv[1:] )

        for component in self.components:
            for key in self.components[component]:
                component.on_cli_arg(key, self[key])

        return self

    def operation(self):
        cmd = getattr(self.cliargs, self.SUBCOMMAND_DEST, None) 
        if not cmd:
            return None

        kwargs = {}
        for arg in self.argnames[cmd]:
            kwargs[arg] = getattr(self.cliargs, arg, None) 

        return cmd, kwargs
