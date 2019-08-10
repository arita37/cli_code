###########################################################################################
###########################################################################################
def obj_is_iterable(obj):
    """
    >>> is_iterable([])   True
    >>> is_iterable(())  True
    >>> is_iterable([x for x in range(10)])    True

    >>> is_iterable("abc")    False
    >>> is_iterable({})     False
    """
    return isinstance(obj, (list, tuple, types.GeneratorType)) or (
        not isinstance(obj, (int, str, dict)) and bool(getattr(obj, "next", False))
    )


def np_list_concat(xss):
    """
    Concatenates a list of lists.
    >>> concat([[]])    []
    >>> concat((()))    []
    >>> concat([[1,2,3],[4,5]])   [1, 2, 3, 4, 5]
    >>> concat([[1,2,3],[4,5,[6,7]]])
    """
    return list(anyconfig.compat.from_iterable(xs for xs in xss))


def obj_is_dict_like(obj):
    """    :param obj: Any object behaves like a dict.
    >>> is_dict_like("a string")    False
    >>> is_dict_like({})     True
    """
    return isinstance(obj, (dict, collections.Mapping))  # any others?


def obj_is_namedtuple(obj):
    """
    >>> p0 = collections.namedtuple("Point", "x y")(1, 2)
    >>> is_namedtuple(p0)  True
    >>> is_namedtuple(tuple(p0))   False
    """
    return isinstance(obj, tuple) and hasattr(obj, "_asdict")


def obj_is_list_like(obj):
    """
    >>> is_list_like([])    True
    >>> is_list_like(())    True
    >>> is_list_like([x for x in range(10)]   True
    >>> is_list_like((1, 2, 3)) True
    >>> is_list_like(g)    True
    >>> is_list_like("abc")   False
    >>> is_list_like(0)    False
    >>> is_list_like({})   False
    """
    return isinstance(obj, _LIST_LIKE_TYPES) and not (
        isinstance(obj, anyconfig.compat.STR_TYPES) or is_dict_like(obj)
    )


"""
Search code:
https://searchcode.com/?q=import+jedi+++jedi.Script%28&lan=19
https://searchcode.com/api/codesearch_I/?q=import+jedi+++jedi.Script%28&lan=19&per_page=50


def github_search_api(keyword= ["'import jedi'",   "'jedi.Script('" ]):

     #Using github3 package retrieve the code
     #import github3
     #gh = github3.GitHub()
     # gh.set_client_id(client_id, client_secret)

     #gh= github3.login(username="arita37", password="")

     #res= gh.search_code(    'requests auth github filename:.py language:python'
                )

    import requests
    ss= " ".join(keyword)


    ## return a dict of github_url_name, rank, code_snippet, repo, user, module_name, method_name
    return res_dict



########################
https://github.com/search?l=Python&q=%22import+json%22+test+json+unit+test&type=Code&utf8=%E2%9C%93

JSON

https://searchcode.com/api/codesearch_I/?q=[searchterm]&p=[page]&per_page[per_page]&lan=[lan]&src=[src]&loc=[loc]&loc2=[loc2]
JSONP

https://searchcode.com/api/jsonp_codesearch_I/?q=[searchterm]&p=[page]&per_page[per_page]&lan=[lan]&src=[src]&loc=[loc]&loc2=[loc2]&callback=[myCallback]
Params

q: search term 
The following filters are textual and can be added into query directly
Filter by file extention ext:EXTENTION E.g. "gsub ext:erb"
Filter by language lang:LANGUAGE E.g. "import lang:python"
Filter by repository repo:REPONAME E.g. "float Q_rsqrt repo:quake"
Filter by user/repository repo:USERNAME/REPONAME E.g. "batf repo:boyter/batf"
p: result page starting at 0 through to 49

per_page: number of results wanted per page max 100
lan: allows filtering to languages supplied by return types. Supply multiple to filter to multiple languages.
src: allows filtering to sources supplied by return types. Supply multiple to filter to multiple sources.
loc: filter to sources with greater lines of code then supplied int. Valid values 0 to 10000.
loc2: filter to sources with less lines of code then supplied int. Valid values 0 to 10000.


Github Search code API
http://github3py.readthedocs.io/en/master/search_structs.html?highlight=search

Search for code source

https://github.com/search?utf8=%E2%9C%93&q=%22import+jedi%22++%22jedi.Script%28%22+++extension%3Apy&type=Code


Rate limit
The Search API has a custom rate limit. For requests using Basic Authentication, OAuth, or client ID and secret, you can make up to 30 requests per minute. For unauthenticated requests, the rate limit allows you to make up to 10 requests per minute.



import github3
gh = github3.GitHub()
# gh.set_client_id(client_id, client_secret)

gh= github3.login(username="arita37", password="")

res= gh.search_code(    'requests auth github filename:.py language:python'
                )


gh = Github(LOGIN, PASSWORD)
# print(list(gh.search_code('requests auth github filename:.py language:python')[:5]))

search_query = 'requests auth github filename:.py language:python'
# print(gh.search_code(search_query).totalCount)

gh.search_code(     'HTTPAdapter in:file language:python'
                ' repo:kennethreitz/requests'  )


for item in  res.items()  :
    print(item)

#!/usr/bin/env python3
# -*- coding: utf-8 -*-


from config import LOGIN, PASSWORD


from github import Github
gh = Github(LOGIN, PASSWORD)
# print(list(gh.search_code('requests auth github filename:.py language:python')[:5]))

search_query = 'requests auth github filename:.py language:python'
# print(gh.search_code(search_query).totalCount)

# The Search API has a custom rate limit. For requests using Basic Authentication, OAuth, or client ID and
# secret, you can make up to 30 requests per minute. For unauthenticated requests, the rate limit allows
# you to make up to 10 requests per minute.
#
# Если авторизован, то каждые 2 секунды можно слать запрос, иначе каждые 6
timeout = 2 if LOGIN and PASSWORD else 6

# Немного добавить на всякий
timeout += 0.5

import time

search_result = gh.search_code(search_query)
total_count = search_result.totalCount
page = 0

data = search_result.get_page(page)
print(data[0])
print(dir(data[0]))
print(data[0].url)
print(data[0].content)
from base64 import b64decode as base64_to_text
print(base64_to_text(data[0].content.encode()).decode())
print(data[0].html_url)

# get user from repo url
user = data[0].html_url.split('/')[3]
print(user)

# i = 1
# while total_count > 0:
#     data = search_result.get_page(page)
#     for result in data:
#         print(i, result)
#         i += 1
#
#     print('page: {}, total: {}, results: {}'.format(page, total_count, len(data)))
#     page += 1
#     total_count -= len(data)
#
#     # Задержка запросов, чтобы гитхаб не блокировал временно доступ
#     time.sleep(timeout)


# i = 1
# for match in gh.search_code(search_query):
#     print(i, match)
#     i += 1
#
#     time.sleep(timeout)
#
#     # print(dir(match))
#     # break


"""

'''
# -*- coding: utf-8 -*-
from __future__ import print_function

"""Minimal API documentation generation."""

# Imports
import inspect
import os.path as op
import re
import sys

from six import string_types


#------------------------------------------------------------------------------
# Utility functions

def _name(obj):
    if hasattr(obj, '__name__'):
        return obj.__name__
    elif inspect.isdatadescriptor(obj):
        return obj.fget.__name__


def _full_name(subpackage, obj):
    return '{}.{}'.format(subpackage.__name__, _name(obj))


def _anchor(name):
    anchor = name.lower().replace(' ', '-')
    anchor = re.sub(r'[^\w\- ]', '', anchor)
    return anchor


_docstring_header_pattern = re.compile(r'^([^\n]+)\n[\-\=]{3,}$',
                                       flags=re.MULTILINE,
                                       )
_docstring_parameters_pattern = re.compile(r'^([^ \n]+) \: ([^\n]+)$',
                                           flags=re.MULTILINE,
                                           )


def _replace_docstring_header(paragraph):
    """Process NumPy-like function docstrings."""

    # Replace Markdown headers in docstrings with light headers in bold.
    paragraph = re.sub(_docstring_header_pattern,
                       r'*\1*',
                       paragraph,
                       )

    paragraph = re.sub(_docstring_parameters_pattern,
                       r'\n* `\1` (\2)\n',
                       paragraph,
                       )

    return paragraph

def _doc(obj):
    doc = inspect.getdoc(obj) or ''
    doc = doc.strip()
    if doc and '---' in doc:
        return _replace_docstring_header(doc)
    else:
        return doc

def _import_module(module_name):
    """
    Imports a module. A single point of truth for importing modules to
    be documented by `pdoc`. In particular, it makes sure that the top
    module in `module_name` can be imported by using only the paths in
    `pdoc.import_path`.
    If a module has already been imported, then its corresponding entry
    in `sys.modules` is returned. This means that modules that have
    changed on disk cannot be re-imported in the same process and have
    its documentation updated.
    """
    import_path = sys.path[:]
    if import_path != sys.path:
        # Such a kludge. Only restrict imports if the `import_path` has
        # been changed. We don't want to always restrict imports, since
        # providing a path to `imp.find_module` stops it from searching
        # in special locations for built ins or frozen modules.
        #
        # The problem here is that this relies on the `sys.path` not being
        # independently changed since the initialization of this module.
        # If it is changed, then some packages may fail.
        #
        # Any other options available?

        # Raises an exception if the parent module cannot be imported.
        # This hopefully ensures that we only explicitly import modules
        # contained in `pdoc.import_path`.
        imp.find_module(module_name.split('.')[0], import_path)

    if module_name in sys.modules:
        return sys.modules[module_name]
    else:
        __import__(module_name)
        return sys.modules[module_name]


#------------------------------------------------------------------------------
# Introspection methods

def _is_public(obj):
    name = _name(obj) if not isinstance(obj, string_types) else obj
    if name:
        return not name.startswith('_')
    else:
        return True


def _is_defined_in_package(obj, package):
    if isinstance(obj, property):
        obj = obj.fget
    mod = inspect.getmodule(obj)
    if mod and hasattr(mod, '__name__'):
        name = mod.__name__
        return name.split('.')[0] == package
    return True


def _iter_doc_members(obj, package=None):
    for _, member in inspect.getmembers(obj):
        if _is_public(member):
            if package is None or _is_defined_in_package(member, package):
                yield member


def _iter_subpackages(package, subpackages):
    """Iterate through a list of subpackages."""
    for subpackage in subpackages:
        yield _import_module('{}.{}'.format(package, subpackage))


def _iter_vars(mod):
    """Iterate through a list of variables define in a module's
    public namespace."""
    vars = sorted(var for var in dir(mod) if _is_public(var))
    for var in vars:
        yield getattr(mod, var)


def _iter_functions(subpackage):
    return filter(inspect.isfunction, _iter_vars(subpackage))


def _iter_classes(subpackage):
    return filter(inspect.isclass, _iter_vars(subpackage))


def _iter_methods(klass, package=None):
    for member in _iter_doc_members(klass, package):
        if inspect.isfunction(member) or inspect.ismethod(member):
            if inspect.isdatadescriptor(member):
                continue
            yield member


def _iter_properties(klass, package=None):
    for member in _iter_doc_members(klass, package):
        if isinstance(member, property):
            yield member.fget


#------------------------------------------------------------------------------
# API doc generation

def _concat(header, docstring):
    return '{header}\n\n{docstring}'.format(header=header,
                                            docstring=docstring,
                                            )

def _function_header(subpackage, func):
    """Generate the docstring of a function."""
    args = inspect.formatargspec(*inspect.getfullargspec(func))
    return "{name}{args}".format(name=_full_name(subpackage, func),
                                   args=args,
                                   )


def _doc_function(subpackage, func):
    return _concat(_function_header(subpackage, func),
                   _doc(func),
                   )


def _doc_method(klass, func):
    """Generate the docstring of a method."""
    argspec = inspect.getfullargspec(func)
    # Remove first 'self' argument.
    if argspec.args and argspec.args[0] == 'self':
        del argspec.args[0]
    args = inspect.formatargspec(*argspec)
    header = "{klass}.{name}{args}".format(klass=klass.__name__,
                                             name=_name(func),
                                             args=args,
                                             )
    docstring = _doc(func)
    return _concat(header, docstring)


def _doc_property(klass, prop):
    """Generate the docstring of a property."""
    header = "{klass}.{name}".format(klass=klass.__name__,
                                       name=_name(prop),
                                       )
    docstring = _doc(prop)
    return _concat(header, docstring)


def _link(name, anchor=None):
    return "[{name}](#{anchor})".format(name=name,
                                        anchor=anchor or _anchor(name),
                                        )


def _generate_preamble(package, subpackages):

    yield "# API documentation of {}".format(package)
    yield _doc(_import_module(package))
    yield "## Table of contents"

    # Table of contents: list of modules.
    for subpackage in _iter_subpackages(package, subpackages):
        subpackage_name = subpackage.__name__

        yield "### " + _link(subpackage_name)

        # List of top-level functions in the subpackage.
        for func in _iter_functions(subpackage):
            yield '* ' + _link(_full_name(subpackage, func),
                               _anchor(_function_header(subpackage, func))
                               )

        # All public classes.
        for klass in _iter_classes(subpackage):

            # Class documentation.
            yield "* " + _link(_full_name(subpackage, klass))

        yield ""

    yield ""


def _generate_paragraphs(package, subpackages):
    """Generate the paragraphs of the API documentation."""

    # API doc of each module.
    for subpackage in _iter_subpackages(package, subpackages):
        subpackage_name = subpackage.__name__

        yield "## {}".format(subpackage_name)

        # Subpackage documentation.
        yield _doc(_import_module(subpackage_name))

        # List of top-level functions in the subpackage.
        for func in _iter_functions(subpackage):
            yield '##### ' + _doc_function(subpackage, func)

        # All public classes.
        for klass in _iter_classes(subpackage):

            # Class documentation.
            yield "### {}".format(_full_name(subpackage, klass))
            yield _doc(klass)

            yield "#### Methods"
            for method in _iter_methods(klass, package):
                yield '##### ' + _doc_method(klass, method)

            yield "#### Properties"
            for prop in _iter_properties(klass, package):
                yield '##### ' + _doc_property(klass, prop)


def _print_paragraph(paragraph):
    out = ''
    out += paragraph + '\n'
    if not paragraph.startswith('* '):
        out += '\n'
    return out


def generate_api_doc(package, subpackages, path=None):
    out = ''
    for paragraph in _generate_preamble(package, subpackages):
        out += _print_paragraph(paragraph)
    for paragraph in _generate_paragraphs(package, subpackages):
        out += _print_paragraph(paragraph)
    if path is None:
        return out
    else:
        with open(path, 'w') as f:
            f.write(out)


if __name__ == '__main__':
    package = 'phy'
    subpackages = [
                   'cluster',
                   'cluster.manual',
                   'electrode',
                   'gui',
                   'io',
                   'plot',
                   'stats',
                   'traces',
                   'utils',
                   ]

    curdir = op.dirname(op.realpath(__file__))
    path = op.join(curdir, '../doc/docs/api.md')
    generate_api_doc(package, subpackages, path=path)
    
    '''


"""
Naming Convention :
  It's mainly to copy paste this module code into another module or for auto-completion
       module_get....
       module_find...
        
       str_find...
       str_get...
       str_print...


  This is not strict rule since good naming is very Hard !!!
  This is for mnemonic / remind easily when you have 50+ functions in one 1 file.
  
  This is to refactor similar methods/functions with similar prefix (ie pseudo-class).
  
  
  
part 3 :  
This is to generate template of unit test from signature.
from numpy_doc182.csv,  generate skeleton of unit test code.  like this :


input csv (previously generated)

  ... prefix.myfunc1    arg1     int     0
  ... prefix.myfunc1    arg2     float
   
    
We need to flatten the arguments into 1 list :
  --->  [ 'prefix1.myfunc1' ,  'arg1'     ,  'arg2'  ]   
  --->  [ 'a1'     ,  'a2'  ]                                  #add temp variable.
  --->  [  0     ,    None  ]                                  #add temp variable  value
  --->  [ 'FullNAME' ,  'arg1=a1'     ,  'arg2=a2'  ]   #add temp variable.  
  ---> Write and flatten the all into a file like this :
        a1= 0
        a2= 
        prefix1.myfunc1( arg1=   a2  ,  arg2=a2)   

  
For Class, we need to generate 1 instance of class  beforehands
   --->   
   --->   
          a1= 0
          a2=
          a3= 
          classname1= Classname(arg1= a1, arg2= a2, arg3= a3)
          classname1.method1(arg1= b1)

           
Algo would be:
   Fitler functions from classes
      df_class= df[ df.type= 'class']
   
   Get the list of unique full_name    prefix.func1
       df.full_name.unique()
       
   for each full_name, flatten the arguments, get default value
         [ 'prefix1.myfunc1' ,  'arg1'     ,  'arg2'  ] 
                

#############################################################################################
part 2 :
Goal is to find the signatures change (ex: from numpy version 1.2 and numpy 1.3)
Take 2 csv files   
   reference_fiel=     numpy_doc181.csv       
   compare_file=       numpy_doc192.csv   generated by previous method.
Then, generate a pandas dataframe with  the  columns


We compare  numpy_doc192.csv to numpy_doc181.csv
    pandas=    copy (numpy_doc181.csv)
    pandas.append (    numpy_doc192.csv  ONLY added full_name)
    

module      :         module1
mod_version      :    19.2.2
full_name        :
prefix_full    :      module1.class1.subclass2.subclass3
prefix         :      class1.subclass2.subclass3
fun_name       :      myfunction1
fun_doc        :      DocString of function / method

arg_name     :         myarg
arg_default_value:    like  5, "default_val",
arg_type1   :         type infered from default value
arg_type2   :        Guess type from JEDI
arg_type3    :       Guess type from different way.
arg_info      :      Any docstring info. 

file1 :           numpy_doc181
file2 :           numpy_doc192
status_file1 :    deprecated   / signature_modified/ added /same

Save the output file in a folder.
Goal is to check the method which are deprecated / added from source file.


"""


'''
# -*- coding: utf-8 -*-
from __future__ import print_function

"""Automatic release tools."""


#------------------------------------------------------------------------------
# Imports
#------------------------------------------------------------------------------

import sys
import os
import os.path as op
import re
from subprocess import call

import six
from six.moves import input
from github3 import login


# -----------------------------------------------------------------------------
# Utilities
# -----------------------------------------------------------------------------

def _call(cmd, system=False):
    if system:
        ret = os.system(cmd)
    else:
        ret = call(cmd.split(' '))
    if ret != 0:
        raise RuntimeError()


# -----------------------------------------------------------------------------
# Messing with version in __init__.py
# -----------------------------------------------------------------------------

root = op.realpath(op.join(op.dirname(__file__), '../'))
_version_pattern = r"__version__ = '([0-9\.]+)((?:\.dev)?)([0-9]+)'"
_version_replace = r"__version__ = '{}{}{}'"


def _path(fn):
    return op.realpath(op.join(root, fn))


def _get_stable_version():
    fn = _path('phy/__init__.py')
    with open(fn, 'r') as f:
        contents = f.read()
    m = re.search(_version_pattern, contents)
    return m.group(1)


def _update_version(dev_n='+1', dev=True):
    fn = _path('phy/__init__.py')
    dev = '.dev' if dev else ''

    def func(m):
        if dev:
            if isinstance(dev_n, six.string_types):
                n = int(m.group(3)) + int(dev_n)
            assert n >= 0
        else:
            n = ''
        if not m.group(2):
            raise ValueError()
        return _version_replace.format(m.group(1), dev, n)

    with open(fn, 'r') as f:
        contents = f.read()

    contents_new = re.sub(_version_pattern, func, contents)

    with open(fn, 'w') as f:
        f.write(contents_new)


def _increment_dev_version():
    _update_version('+1')


def _decrement_dev_version():
    _update_version('-1')


def _set_final_version():
    _update_version(dev=False)


# -----------------------------------------------------------------------------
# Git[hub] tools
# -----------------------------------------------------------------------------

def _create_gh_release():
    version = _get_stable_version()
    name = 'Version {}'.format(version)
    path = _path('dist/phy-{}.zip'.format(version))
    assert op.exists(path)

    with open(_path('.github_credentials'), 'r') as f:
        user, pwd = f.read().strip().split(':')
    gh = login(user, pwd)
    phy = gh.repository('kwikteam', 'phy')

    if input("About to create a GitHub release: are you sure?") != 'yes':
        return
    release = phy.create_release('v' + version,
                                 name=name,
                                 # draft=False,
                                 # prerelease=False,
                                 )

    release.upload_asset('application/zip', op.basename(path), path)


def _git_commit(message, push=False):
    assert message
    if input("About to git commit {}: are you sure?") != 'yes':
        return
    _call('git commit -am "{}"'.format(message))
    if push:
        if input("About to git push upstream master: are you sure?") != 'yes':
            return
        _call('git push upstream master')


# -----------------------------------------------------------------------------
# PyPI
# -----------------------------------------------------------------------------

def _upload_pypi():
    _call('python setup.py sdist --formats=zip upload')


# -----------------------------------------------------------------------------
# Docker
# -----------------------------------------------------------------------------

def _build_docker():
    _call('docker build -t phy-release-test docker/stable')


def _test_docker():
    _call('docker run --rm phy-release-test /sbin/start-stop-daemon --start '
          '--quiet --pidfile /tmp/custom_xvfb_99.pid --make-pidfile '
          '--background --exec /usr/bin/Xvfb -- :99 -screen 0 1400x900x24 '
          '-ac +extension GLX +render && '
          'python -c "import phy; phy.test()"',
          system=True)


# -----------------------------------------------------------------------------
# Release functions
# -----------------------------------------------------------------------------

def release_test():
    _increment_dev_version()
    _upload_pypi()
    _build_docker()
    _test_docker()


def release():
    version = _get_stable_version()
    _set_final_version()
    _upload_pypi()
    _git_commit("Release {}.".format(version), push=True)
    _create_gh_release()


if __name__ == '__main__':
    globals()[sys.argv[1]]()
    
    '''


"""
Hello,

I have some code generating doc for a given module like this :
generate_doc("numpy")  ---> Text file as below
...
numpy.polynomial.hermite.hermgauss(deg) 
numpy.polynomial.hermite.hermgrid2d(x, y, c) 
numpy.polynomial.hermite.hermgrid3d(x, y, z, c) 
numpy.polynomial.hermite.hermint(c, m, k, lbnd, scl, axis) 
numpy.polynomial.hermite.hermline(off, scl) 
numpy.polynomial.hermite.hermmul(c1, c2) 
numpy.polynomial.hermite.hermmulx(c) 
numpy.polynomial.hermite.hermpow(c, pow, maxpower) 
numpy.polynomial.hermite.hermroots(c) 
numpy.polynomial.hermite.hermsub(c1, c2) 



Goal is to create a class  with the following methods :

1)  Generate list of functions / class  / methods in Pandas
Input :   Name of python module  like  'numpy'

Output :  Pandas dataframe with the format, columns
module      :   module1
mod_version      :   19.2.2
prefix_full   :    module1.class1.subclass2.subclass3
prefix         :         class1.subclass2.subclass3
fun_name     :      myfunction1
fun_doc    :         DocString of function / method

arg_name     :         myarg
arg_default_value:    like  5, "default_val",
arg_type1   :   type infered from default value
arg_type2   :   Guess type from JEDI
arg_type3    :  Guess type from different way
arg_info      :  Any info 

( 1 row per argument !!!)
Example :  myfun1(a1=9, a2='ok', a3=5.6)  gives 3 pandas rows :
  ...   myfun1    a1   9
  ...   myfun1   a2   'ok'
  ...   myfun1   a3   5.6

and save the pandas into csv file.






3) from numpy_doc182.csv,  generate skeleton of unit test code.  like this :
arg2i=
arg1i= 
prefix1.myfunc1( arg1=   arg1i  ,  arg2=arg2i)   



4)  Given a python file   myfile.py  and a reference doc numpy_doc182.csv
     Parse the file  and  check for each line  if the right member belongs to numpy_doc182.csv
      if Yes --->   the right_line into pandas dataframe
        iF not --> go to next line.

    Using source code information, we want to solve missing type information.
    When we get the full doc, we can do static check as well as test generation.


    Pre-fetched type can be used: https://github.com/python/typeshed



"""
