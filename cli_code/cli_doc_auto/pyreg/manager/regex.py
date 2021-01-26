# -*- coding: utf-8 -*-

import os
import re
import json
import logging


from ..context import config


LOGGER = logging.getLogger()


ARG_SEP = '\s*,\s*'
KWARGS_OP = '\s*=\s*'

KEY_PATTERNS = [
    ('var',    '[\w_][\w\d_]*'),
    ('args',   '\*\s*[\w_][\w\d_]*'),
    ('kwargs', '\*\*\s*[\w_][\w\d_]*'),
]

VAL_PATTERNS = [
    ('cont', '(:?\[(.*?)\]|\(.*?\)|\{.*?\})'),
    ('call', '[\w_][\w\d_]*\s*\(.*?\)',),
    ('expr', '(:?.*?\s*,|.*?$)'),
]

CLS_PATTERN = '([\t ]*)class\s+([\w_][\w\d_]*)\s*(\((.*?)\))?\s*:'
MTD_PATTERN = 'def\s+([\w_][\w\d_]*)\s*\((.*?)\)\s*:'

CLS_DEF = '.*?class\s+[\w_][\w\d_]*'
UNTIL_CLS_DEF = '^(?:(?!class\s+[\w_][\w\d_]*).)*'


def _wipe_docstrings_comments(src):

    for docstring in re.findall('""".*?"""', src, re.MULTILINE | re.DOTALL):
        src = src.replace(docstring, '')

    for docstring in re.findall("'''.*?'''", src, re.MULTILINE | re.DOTALL):
        src = src.replace(docstring, '')

    src = re.sub('^#.*', '', src, re.MULTILINE | re.DOTALL)
    return src


def _match_kwarg(signature):
    LOGGER.debug(signature)
    for name, pattern in VAL_PATTERNS:
        match = re.match(pattern, signature)
        if not match:
            LOGGER.info('not match {}'.format(name))
            continue
        match = match.group()
        # check for argsep
        argsep = re.match(ARG_SEP, match[::-1])
        if argsep:
            argsep = argsep.group()
            signature = signature[len(match)-len(argsep):]
            match = match[:-len(argsep)]
        else:
            signature = signature[len(match):]

        return signature, match

    return signature, None


FORMAT = u'%(levelname)-9s [%(module)9s:%(lineno)3s - %(funcName)9s]--> %(message)s'


def _match(signature):
    # trim whitespaces
    signature = re.sub('^\s+', '', signature)
    signature = re.sub('\s+$', '', signature)
    signature = re.sub(r'\\', '', signature)
    signature = signature

    args = []
    kwargs = []
    match = True
    while match:
        match = None
        for name, pattern in KEY_PATTERNS:
            match = re.match(pattern, signature)
            if not match:
                continue
            LOGGER.info('match {}'.format(name))

            match = match.group()

            # update index
            signature = signature[len(match):]

            # is it a kwarg?
            kwarg_op = re.match(KWARGS_OP, signature)
            if kwarg_op:
                kwarg_op = kwarg_op.group()
                signature = signature[len(kwarg_op):]
                signature, kwargval = _match_kwarg(signature)
                kwargs.append((match, kwargval))
            else:
                # this is an arg
                args.append(match)

            # proceed to next arg
            argsep = re.match(ARG_SEP, signature)
            if argsep:
                argsep = argsep.group()
                signature = signature[len(argsep):]
            else:
                pass

            break

    return args, kwargs


def _parse_arglist(arglist):
    args, kwargs = _match(arglist)

    pack = {}
    for arg in args[:]:
        if re.match(KEY_PATTERNS[1][1], arg):
            pack['args'] = arg.replace('*', '')
            args.remove(arg)

        elif re.match(KEY_PATTERNS[2][1], arg):
            pack['kwargs'] = arg.replace('*', '')
            args.remove(arg)

    return args, kwargs, pack


def _extract_functions(src):
    defs = re.findall(
        '^def[ \t]+([\w_][\w\d_]*)\((.*?)\)[\s]*:', src, re.MULTILINE | re.DOTALL)

    result = []
    for name, arglist in defs:
        args, kwargs, pack = _parse_arglist(arglist)
        result.append(dict(
            name=name,
            args=args,
            kwargs=kwargs,
            pack=pack,
        ))

    return result


def _calc_indent(indent):
    if config.TAB:
        return indent.count(' ') / config.TAB
    return indent.count('\t')


def _next_class(src):
    tmpcls = re.match(CLS_DEF, src, re.MULTILINE | re.DOTALL)
    if not tmpcls:
        return None

    clsidx_start = 0
    clsidx_end = len(tmpcls.group())

    src2 = src[clsidx_end:]

    tmpcls = re.match(UNTIL_CLS_DEF, src2, re.MULTILINE | re.DOTALL)
    if not tmpcls:
        return clsidx_start, -1

    return clsidx_start, clsidx_end+len(tmpcls.group())


def _extract_classes(src):
    clz = re.findall(CLS_PATTERN, src, re.MULTILINE | re.DOTALL)

    classes = []
    methods = {}

    plugged = []

    for indent_cls, clsname, _, inherits in clz:
        raw_indentcls = indent_cls
        indent_cls = _calc_indent(indent_cls)

        classes.append({
            "name":     clsname,
            "indent":   indent_cls,
            "inherits": inherits,
        })

        cls_limits = _next_class(src)
        if not cls_limits:
            continue

        start, end = cls_limits
        clsbody = src[start:end]

        if clsname not in methods:
            methods[clsname] = []

        # find methods of the class
        if config.TAB:
            tabs = ' '*config.TAB
        else:
            tabs = '\t'
        tabs = tabs * int(indent_cls+1)
        mtd = re.findall('^{}{}'.format(tabs, MTD_PATTERN),
                         clsbody, re.MULTILINE | re.DOTALL)

        for mtdname, arglist in mtd:
            args, kwargs, pack = _parse_arglist(arglist)
            methods[clsname].append(
                {
                    'name':   mtdname,
                    'args':   args,
                    'kwargs': kwargs,
                    'pack':   pack,
                }
            )

        src = src[len(clsbody):]

    return classes, methods


def _analyze_classes(sourcefiles):
    results = {}
    for path in sourcefiles:
        print(path)
        try:
            with open(path, 'r') as f:
                src = f.read()
            src = _wipe_docstrings_comments(src)

            results[path] = _extract_classes(src)
        except Exception as e:
            print(e)

    path = os.path.join(os.path.dirname(config.OUT), 'classes.json')
    with open(path, 'w') as f:
        data = json.dumps(results, indent=2, ensure_ascii=False)
        f.write(data)

    return results


def _analyze_functions(sourcefiles):
    results = {}

    for path in sourcefiles:
        print(path)
        try:
            with open(path, 'r') as f:
                src = f.read()
            src = _wipe_docstrings_comments(src)

            results[path] = _extract_functions(src)
        except Exception as e:
            print(e)

    path = os.path.join(os.path.dirname(config.OUT), 'functions.json')
    with open(path, 'w') as f:
        data = json.dumps(results, indent=2, ensure_ascii=False)
        f.write(data)

    return results


def _documentation(classes, functions):
    lines = []

    # documents class methods
    for srcpath in classes:
        sort = []
        lines.append(
            '{}\n----------------methods----------------'.format(srcpath))
        for clsname, methods in classes[srcpath][1].items():
            for method in methods:
                args = ', '.join(method['args'])
                kwargs = ', '.join(u'{}={}'.format(key, val)
                                   for key, val in method['kwargs'])

                pack = []
                if method['pack']:
                    if method['pack'].get('args'):
                        pack.append('*{}'.format(method['pack']['args']))
                    if method['pack'].get('kwargs'):
                        pack.append('**{}'.format(method['pack']['kwargs']))

                pack = ', '.join(pack) or ''

                if args:
                    args = '{}, '.format(args)

                if kwargs:
                    kwargs = '{}, '.format(kwargs)

                sort.append('{}.{}({} {} {})'.format(
                    clsname, method['name'], args, kwargs, pack))

        sort = sorted(sort)
        lines.extend(sort)

        sort = []
        lines.append('\n---------------functions---------------')
        for fn in functions[srcpath]:
            args = ', '.join(fn['args'])
            kwargs = ', '.join(u'{}={}'.format(key, val)
                               for key, val in fn['kwargs'])

            pack = []
            if fn['pack']:
                if fn['pack'].get('args'):
                    pack.append('*{}'.format(fn['pack']['args']))
                if fn['pack'].get('kwargs'):
                    pack.append('**{}'.format(fn['pack']['kwargs']))

            pack = ', '.join(pack) or ''

            if args:
                args = '{}, '.format(args)

            if kwargs:
                kwargs = '{}, '.format(kwargs)

            sort.append('{}({} {} {})'.format(fn['name'], args, kwargs, pack))

        sort = sorted(sort)
        lines.extend(sort)
        lines.append('')
        lines.append('')

    with open(config.OUT, 'w') as f:
        f.write('\n'.join(lines))


def analyze(sourcefiles):
    functions = _analyze_functions(sourcefiles)
    classes = _analyze_classes(sourcefiles)

    _documentation(classes, functions)
