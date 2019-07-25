# -*- coding: utf-8 -*-
"""
 cli_codesource --do    --module jedi
--do  module_signature_write(arg.module)
--do module_unitest_write(module_name= arg.module)



"""
from __future__ import absolute_import, division, print_function, unicode_literals

import ast
import fnmatch
import inspect
import math
import operator
import os
import pydoc
import re
import sys
from builtins import int, open, range, str, zip
from collections import OrderedDict
from importlib import import_module
from pkgutil import walk_packages

import pandas as pd

import regex

####################################################################################################


###################################################################################################
COLS_NAME = [
    "module_name",
    "module_version",
    "full_name",
    "prefix",
    "obj_name",
    "obj_doc",
    "object_type",
]
NAN = float("nan")


def zdoc():
    source = inspect.getsource(ztest)
    print(source)


##################################################################################################
def str_join(*members):
    """join_memebers(member1, ...) takes an orbitrary number of
    arguments of type 'str'and concatinates them with using the '.' separator"""
    return ".".join(members)


def np_merge(*dicts):
    container = {}
    for d in dicts:
        container.update(d)
    return container


##################################################################################################
class Module:
    """class Module(module_name)
    Class Module gets all the submodules, classes, class_methods and functions of 
    the module taken as an argument by its instance. Every instance of the class has:
    ATTRIBUTES: Module.module_name, self.module, self.submodules, self.functions, self.classes, self.class_methods
    METHODS: self.get_module_version(self), self.get_submodules(self), self.get_functions(self), self.get_classes(self),
    self.get_class_methods(), self.isimported(self, name), self.get_mlattr(self, full_name), self.get_submodule(self, attr)."""

    def __init__(self, module_name):
        self.module_name = module_name
        self.module = import_module(self.module_name)
        self.submodules = self.get_submodules()
        self.functions = self.get_functions()
        self.classes = self.get_classes()
        self.class_methods = self.get_class_methods()

    def get_module_version(self):
        """get_module_version(self) Module method
        return the version of the module taken as an instance argument."""
        return self.module.__version__

    def get_submodules(self):
        """get_submodules(self) Module method
        return a list of submodules of the module taken as an instance argument."""
        submodules = {}
        for loader, name, is_pkg in walk_packages(self.module.__path__, self.module.__name__ + "."):
            if self.is_imported(name):
                submodules[name] = self.get_submodule(self.get_mlattr(name))
        return submodules

    def get_functions(self):
        """get_functions(self) Module method
        return a list of functions of the module taken as an instance argument."""
        functions = {}
        for submodule_name, submodule in self.submodules.items():
            for function_name, function in inspect.getmembers(
                submodule, lambda f: inspect.isfunction(f) or inspect.isbuiltin(f)
            ):
                functions[str_join(submodule_name, function_name)] = function
        return functions

    def get_classes(self):
        """get_classes(self) Module method
        return a list of classes of the module taken as an instance argument."""
        classes = {}
        for submodule_name, submodule in self.submodules.items():
            for class_name, class_ in inspect.getmembers(submodule, lambda c: inspect.isclass(c)):
                classes[str_join(submodule_name, class_name)] = class_
        return classes

    def get_class_methods(self):
        """get_class_methods(self) Module method
        return a list of class methods of the module taken as an instance argument."""
        methods = {}
        for class_name, class_ in self.classes.items():
            for method_name, method in inspect.getmembers(
                class_, lambda m: inspect.ismethod(m) or inspect.isbuiltin(m)
            ):
                methods[str_join(class_name, method_name)] = method
        return methods

    def is_imported(self, submodule_name):
        """is_imported(self, submodule_name) Module method
        retrun True if submodule was imported and False otherwise."""
        return submodule_name in sys.modules

    def get_mlattr(self, full_name):
        """get_mlattr(self, full_name) Module method
        return a multi-level attribute of an object."""
        return full_name.split(".", 1)[1]

    def get_submodule(self, attr):
        """get_submodule(self, attr) Module method
        return submodule object of the module by its attribute."""
        return operator.attrgetter(attr)(self.module)


def obj_get_name(obj):
    """get_name(obj) return object name."""
    return obj.__name__


def obj_get_doc_string(obj):
    """get_doc_string(obj) return object doc string"""
    return re.sub("\x08.", "", pydoc.render_doc(obj)) or obj.__doc__


def obj_get_prefix(name):
    """get_prefix(name) return object prefix."""
    return name.split(".", 1)[1].rsplit(".", 1)[0]


def str_strip_text(string):
    """str_strip_text(string) strip \b and \n literals off the string."""
    return re.sub("\x08.", "", string.replace("\n", ""))


def obj_get_signature(obj):
    obj_name = obj.__name__
    obj_doc = str_strip_text(pydoc.render_doc(obj))
    match = regex.findall(obj_name + "(\((?>[^()]+|(?1))*\))", obj_doc)[:2]
    if match:
        if len(match) > 1:
            signature = (
                match[0][1:-1] if match[0][1:-1] != "..." and match[0] != "" else match[1][1:-1]
            )
            return signature
        else:
            return match[0][1:-1] if match[0][1:-1] != "..." else ""
    else:
        return ""


def obj_get_args(obj):
    arguments = OrderedDict()
    if inspect.isbuiltin(obj):
        obj_signature = obj_get_signature(obj)
        if obj_signature:
            pattern = "\w+=[-+]?[0-9]*\.?[0-9]+|\w+=\w+|\w+=\[.+?\]|\w+=\(.+?\)|[\w=']+"
            items = re.findall(pattern, obj_signature)
            for item in items:
                split_item = item.split("=")
                if len(split_item) == 2:
                    arguments[split_item[0]] = split_item[1]
                elif len(split_item) == 1:
                    arguments[split_item[0]] = NAN
            return arguments
        else:
            return {}
    else:
        argspec = inspect.getfullargspec(obj)
        args = argspec.args
        defaults = argspec.defaults
        if defaults:
            args_with_default_values = OrderedDict(zip(args[-len(defaults) :], defaults))
            for arg in args:
                if arg in args_with_default_values:
                    arguments[arg] = args_with_default_values[arg]
                else:
                    arguments[arg] = NAN
            return arguments
        else:
            return OrderedDict(zip(args, [NAN] * len(args)))


def obj_guess_arg_type(arg_default_values):
    types = []
    for arg_value in arg_default_values:
        if isinstance(arg_value, str):
            try:
                types.append(type(ast.literal_eval(arg_value)).__name__)
            except ValueError:
                types.append("str")
            except SyntaxError:
                types.append(NAN)
        elif isinstance(arg_value, float) and math.isnan(arg_value):
            types.append(NAN)
        else:
            types.append(type(arg_value).__name__)
    return tuple(types)


def obj_get_arginfo(obj, args):
    """get_arginfo(obj, args) return a tuple of the object argument info."""
    return ("arg_info",) * len(args)


def obj_get_nametype(obj):
    """get_name(obj) return object name."""
    types = {"function": inspect.isfunction, "method": inspect.ismethod, "class": inspect.isclass}
    for obj_type, inspect_type in types.items():
        if inspect_type(obj):
            return obj_type
    return None


def obj_class_ispecial(obj):
    try:
        inspect.getfullargspec(obj.__init__)
    except TypeError:
        return False
    else:
        if inspect.isclass(obj):
            return True
        else:
            return False


def obj_get_type(x):
    # eval
    if isinstance(x, str):
        return "str"
    if isinstance(x, int):
        return "int"
    if isinstance(x, float):
        return "float"


#############################################################################################################
def module_signature_get(module_name):
    """module_signature(module_name) return a dictionary containing information
       about the module functions and methods"""
    module = Module(module_name)
    members = np_merge(module.functions, module.classes, module.class_methods)
    doc_df = {
        "module_name": module_name,
        "module_version": module.get_module_version(),
        "full_name": [],
        "prefix": [],
        "obj_name": [],
        "obj_doc": [],
        ## TODO:   add function_type column
        # 'obj_type'    class / class.method /  function / decorator ....
        "object_type": [],
        "arg": [],
        "arg_default_value": [],
        "arg_type": [],
        "arg_info": [],
    }

    for member_name, member in members.items():
        isclass = obj_class_ispecial(member)
        isfunction = inspect.isfunction(member)
        ismethod = inspect.ismethod(member)

        if isclass or isfunction or ismethod:
            doc_df["full_name"].append(member_name)
            doc_df["prefix"].append(obj_get_prefix(member_name))
            doc_df["obj_name"].append(obj_get_name(member))
            doc_df["obj_doc"].append(obj_get_doc_string(member))
            doc_df["object_type"].append(obj_get_nametype(member))
            doc_df["arg"].append(tuple(obj_get_args(member.__init__ if isclass else member).keys()))
            doc_df["arg_default_value"].append(
                tuple(obj_get_args(member.__init__ if isclass else member).values())
            )
            doc_df["arg_type"].append(obj_guess_arg_type(doc_df["arg_default_value"][-1]))
            doc_df["arg_info"].append(obj_get_arginfo(member, doc_df["arg"][-1]))

    return doc_df


def pd_df_expand(x):
    y = pd.DataFrame(x.values.tolist())
    return y.stack()


def pd_df_format(df, index, filter=True):
    level_to_drop = "level_{}".format(len(index))
    # if filter: df = filter_data(['private_methods'], pd.DataFrame(df))   # We keep ALL the data as RAW data in csv.
    formated_df = (
        df.set_index(index)
        .apply(lambda x: pd_df_expand(x), 1)
        .stack()
        .reset_index()
        .drop(level_to_drop, 1)
    )
    formated_df.columns = index + [x for x in df.columns if x not in index]
    return formated_df


def module_signature_write(module_name, file_out="", return_df=0, isdebug=0):
    """  Write down the files.
         
    """
    df = module_signature_get(module_name)
    df = pd_df_format(pd.DataFrame(df), COLS_NAME)
    df = df.sort_values("full_name", ascending=True)

    if return_df == 1:
        return df  # return df
    else:
        file_out = (
            file_out
            if file_out != ""
            else os.path.join(os.getcwd(), str_join("doc_" + module_name, "csv"))
        )
        if isdebug:
            print("Signature Writing")
        print(file_out)
        df.to_csv(file_out, index=False, mode="w")


#############################################################################################################
# def drop_private_methods(data):
#    return data.drop(data[data.obj_name.str.contains('^_')].index)


# def filter_data(filter_type, data):
#    for filter in filter_type:
#        if filter == 'private_methods':
#            data = drop_private_methods(data)
#    return data


def obj_arg_filter_apply(df, filter_list=None):
    """  Apply Sequential Filtering to the frame of argument
    :param df: Signature Datframe
    :param filter_list:    ('sort_ascending', 1)  we can add very easily new filter
    :return: dataframe filtering
    """
    if filter_list is None:
        filter_list = [("filter_name", "arg")]
    for filter0 in filter_list:
        f, farg = filter0
        if f == "class_only":
            df = df[(df["function_type"] == "class_method") | (df["function_type"] == "class")]
        if f == "function_only":
            df = df[(df["function_type"] == "function")]

        if f == "public_only":
            df = df[-df["obj_name"].str.startswith(r"__", na=False)]
        if f == "private_only":
            df = df[(df["obj_name"].str.startswith(r"__", na=False))]

        if f == "fullname_regex":
            df = df[df["full_name"].str.contains(farg, na=False)]
        if f == "fullname_startwith":
            df = df[df["full_name"].str.startswith(farg, na=False)]
        if f == "fullname_exclude":
            df = df[-df["full_name"].str.contains(farg, na=False)]

        if f == "sort_ascending":
            df = df.sort_values("full_name", ascending=farg)
    return df


def obj_arg_filter_nonetype(x):
    try:
        if x["arg_type"] == "NoneType":
            return x["args_dummy"] + "None"
        if pd.isnull(x["arg_type"]):
            return x["args_dummy"]
        else:
            return x["args_dummy"] + str(x["arg_default_value"])
    except Exception as e:
        print(e)
        return ""


def module_unitest_write(
    input_signature_csv_file="",
    module_name="",
    outputfile="unittest.txt",
    filter_list=None,
    isdebug=0,
):
    """
     :param module_name:     name of modul in string
     :param input_signature_csv_file:   csv file name
     :param outputfile: 
     :param filter_list:  ("public_only","") 
     :return: 
    """
    if filter_list is None:
        filter_list = []
    if isdebug:
        print("Module Unitest Writing ")
    if module_name != "":
        data0 = module_signature_write(module_name, return_df=1)
    elif input_signature_csv_file != "":
        data0 = pd.read_csv(input_signature_csv_file)
        print(input_signature_csv_file)
    else:
        print("Provide module name OR CSV file")
        return 1

    if isdebug:
        print(data0.head(5))
        print(data0.dtypes)

    # Filtering  ###############################################################################
    data = data0[data0["arg"] != "self"].copy(deep=True)  # self argument
    data = obj_arg_filter_apply(data, filter_list)  # Apply Sequential Fitlering

    ## Generate dummy variables aXXXX=  YYYY    for assignment
    data["args_dummy"] = "a" + data.groupby("obj_name").cumcount().add(1).astype(str)
    data["arg"] = data["arg"] + "=" + data["args_dummy"]
    data["args_dummy"] += "="
    data["args_dummy"] = data.apply(lambda x: obj_arg_filter_nonetype(x), axis=1)

    ## Generate  1 line function
    df1 = pd.DataFrame(data.groupby("full_name")["arg"].apply(tuple))
    df1["arg"] = df1["arg"].apply(lambda x: "(" + ",".join(x) + ")")

    df2 = pd.DataFrame(data.groupby("full_name")["args_dummy"].apply(tuple))

    ndf = pd.concat([df1, df2], 1)
    ndf = ndf.reset_index()

    # print(ndf)
    ndf["function"] = ndf["full_name"] + ndf["arg"]

    # ndf['function'] = (ndf.reset_index()['full_name'] + ndf.reset_index()['arg'].astype(str)).tolist()
    ndf["function"].replace(["'", ",\)"], ["", ")"], regex=True, inplace=True)
    # ndf = ndf.reset_index(drop=True).drop('arg', 1)

    ## Generate  1 line function
    # df1=  pd.DataFrame(data.groupby('full_name')['arg'].apply(tuple))
    # df2=  pd.DataFrame(data.groupby('full_name')['args_dummy'].apply(tuple))
    # ndf = pd.concat([df1, df2 ], 1)
    # ndf['function'] = (ndf.reset_index()['full_name'] + ndf.reset_index()['arg'].astype("unicode")).tolist()
    # ndf['function'].replace(["'", ",\)"], ["", ")"], regex=True,inplace=True)
    # ndf = ndf.reset_index(drop=True).drop('arg', 1)

    # Output writing
    if isdebug:
        print("Writing : " + outputfile)
    with open(outputfile, "a") as template:
        for module_name in list(data.module_name.unique()):
            template.write("import {}\n\n".format(module_name))

        for row in ndf.itertuples():  # Unit test with dummy var and function code.
            for arg in row.args_dummy:
                template.write("{}\n".format(arg))

            template.write("{}\n\n".format(row.function))  # 1 line writing

    #### Improvement : Sperate case of Class and Function
    """
      Need instance of class be using method.
      MyClass1=  MyClass.__init__(arg1=a1)
      
      a1=
      Myclass1.method1(arg1=a1)
      
      a1=
      Myclass1.method2(arg1=a1)
            
        Example of Unit Tests: 
        https://github.com/search?l=Python&q=%22import+json%22+test+json+unit+test&type=Code&utf8=%E2%9C%93
       
        Unit test  
    http://eli.thegreenplace.net/2014/04/02/dynamically-generating-python-test-cases
           
    """


def module_doc_write(
    module_name="", input_signature_csv_file="", outputfile="", filter_list=None, debug=0
):
    """
      Write doc of module: 1 line per function /argument :
      numpy.core.sometrue(a, axis, out, keepdims) 
      numpy.core.sort(a, axis, kind, order) 

    """
    if filter_list is None:
        filter_list = [("public_only", "")]
    if module_name != "":
        df_data = module_signature_write(module_name, return_df=1)
    elif input_signature_csv_file != "":
        df_data = pd.read_csv(input_signature_csv_file)
    else:
        print("Provide module name OR CSV file")
        return 1

    # Filtering  ###############################################################################
    df_data = obj_arg_filter_apply(df_data, filter_list)  # Apply Sequential Fitlering
    # print(data.head(5))

    ## Generate  1 line function
    def agg_in_1line(dfi):
        full_name = dfi.full_name.values[0]
        args = "(" + ",".join(list(dfi.arg.values)) + ")"
        function = full_name + args
        # function.replace( ["'", ",\)"], ["", ")"], regex=True,inplace=True )
        return pd.Series([args, function], ["arg", "function"])

    df_out = df_data.groupby("full_name").apply(agg_in_1line)
    if debug:
        print(df_out.columns)
        print(df_out.head(5))

    # ndf=  pd.DataFrame(data.groupby('full_name')['arg'].apply(tuple))
    # ndf['function'] = (ndf.reset_index()['full_name'] + ndf.reset_index()['arg'].astype(str)).tolist()
    # ndf['function'].replace(["'", ",\)"], ["", ")"], regex=True,inplace=True)
    # ndf = ndf.reset_index(drop=True).drop('arg', 1)

    # Output writing
    write_mode = "wb" if sys.version_info.major == 2 else "w"
    with open(outputfile, "w") as template:
        module_name1 = df_data["module_name"].values[0] + "_" + df_data["module_version"].values[0]
        template.write("#{}\n".format(module_name1))

        for row in df_out.itertuples():
            template.write("{}\n".format(row.function))  # 1 line writing


def module_doc_write_batch(module_list=None, list_exclude=None, folder_export="/"):
    if list_exclude is None:
        list_exclude = [""]
    if module_list is None:
        module_list = ["json"]


def module_signature_compare(df_csv_new, df_csv_old, export_csv="", return_df=0):
    """
    2)  Take 2 csv files   numpy_doc181.csv       and numpy_doc192.csv   generated by previous method.
Then, generate a pd dataframe with  the  columns
module      :   module1
mod_version      :   19.2.2
prefix_full   :    module1.class1.subclass2.subclass3
prefix         :         class1.subclass2.subclass3
fun_name     :      myfunction1
fun_doc    :         DocString of function / method

arg_name     :         myarg
arg_default_value:    like  5, "default_val",


status_arg :   deprecated / new           
status     :   new


Save the output file in a folder.
Goal is to check the method which are deprecated / added from source file.
"""
    df1 = pd.read_csv(df_csv_old)
    df2 = pd.read_csv(df_csv_new)

    #### Method name Added/Removed   #######################
    df1_full_name = set(list(df1["full_name"].unique()))
    df2_full_name = set(list(df2["full_name"].unique()))

    ll_new = df2_full_name.difference(df1_full_name)
    ll_deprecated = df1_full_name.difference(df2_full_name)  # Not in new, but in old

    ### New Arguments in method (but method name unchanged)
    df1["unique_name"] = df1.full_name + "-" + df1.arg
    df2["unique_name"] = df2.full_name + "-" + df2.arg

    df1_unique_name = set(list(df1["unique_name"].unique()))
    df2_unique_name = set(list(df2["unique_name"].unique()))
    ll_modified = df2_unique_name.difference(df1_unique_name)
    ll_modified = list(set([x.split("-")[0] for x in ll_modified]))

    #### Merge dataframe
    df0 = pd.concat((df1, df2[df2.full_name.isin(ll_new)]))  # Add only new

    df0["status"] = ""
    df0[df0.full_name.isin(ll_new)]["status"] = "new"
    df0[df0.full_name.isin(ll_deprecated)]["status"] = "deprecated"

    df0["status_arg"] = ""
    df0[df0.full_name.isin(ll_modified)][
        "status_arg"
    ] = "modified"  # Argument names are modified but same method name.

    ### Export All:
    if return_df:
        return df0
    df0[df0.status == "new"].to_csv(export_csv[:-4] + "_new.csv", index=False)
    df0[df0.status == "deprecated"].to_csv(export_csv[:-4] + "_deprecated.csv", index=False)
    df0[df0.status_arg == "modified"].to_csv(export_csv[:-4] + "_modified.csv", index=False)
    df0.to_csv(export_csv[:-4] + "_all.csv", index=False)


###############################################################################################
def obj_guess_arg_type2(full_name, arg_name, type_guess_engine="pytype"):
    """
     guess typing pytypes de Google
    :param full_name: 
    :param arg_name: 
    :param type_guess_engine: 
    :return: 
    """
    if type_guess_engine == "pytype":
        """
          Use Google pytype, but doc is super poor.....
          Google pytype --->  generate source code with type...
        
        
        """
        pass

    if type_guess_engine == "github":
        """
          gh= github.login(login, password)
          res= gh.search_code( 'import json'  AND
                           'json.method_name('  AND 
                          language=python )
        
          Parse res to find method_name(  args=5 ....)
        
        
       """

    return 1


###############################################################################################
#######Github Helpers ########################################################################################
def os_folder_create(directory):
    DIR0 = os.getcwd()
    if not os.path.exists(directory):
        os.makedirs(directory)
    os.chdir(DIR0)


def code_search_github(
    keywords=None,
    outputfolder="",
    browser="",
    login="",
    password="",
    page_start=1,
    page_end=1,
    isreturn_df=0,
    iswrite_df=1,
    isdownload_file=1,
    isdebug=0,
    outputfile="df_github_codesearch_01.csv",
    FILTER=1,
    CFG=None,
):
    """  pip install selenium  --no-deps
 #df= github_search_source_code(keywords= ["import jedi",   "jedi.Script(" ], outputfolder= DIRCWD + "/tmp/", browser="",
  # page_num=1, isreturn_df=1)

 ### pip install attrdict
 """
    # from attrdict import AttrDict as dict2
    # CFG= dict2({ "github_login": "", "github_pass":   "",  "github_phantomjs": "D:/_devs/webserver/phantomjs-1.9.8/phantomjs.exe"})

    if keywords is None:
        keywords = ["import jedi", "jedi.Script("]
    CFG_phantomjs, CFG_github_login, CFG_github_pass = (
        CFG.phantomjs,
        CFG.github_login,
        CFG.github_pass,
    )

    from selenium import webdriver
    from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
    from selenium.webdriver.common.keys import Keys
    from bs4 import BeautifulSoup

    # noinspection PyUnresolvedReferences
    import wget

    DesiredCapabilities.PHANTOMJS[
        "phantomjs.page.settings.userAgent"
    ] = "Mozilla/5.0 (Windows NT 6.1; Win64; x64; rv:16.0) Gecko/20121026 Firefox/16.0"

    if browser == "firefox":
        driver = webdriver.Firefox()
    else:
        driver = webdriver.PhantomJS(
            CFG_phantomjs
        )  # r"D:/_devs/webserver/phantomjs-1.9.8/phantomjs.exe"

    driver.get("https://github.com/login")
    username = driver.find_element_by_id("login_field")
    password = driver.find_element_by_id("password")
    username.clear()
    username.send_keys(CFG_github_login)
    password.clear()
    password.send_keys(CFG_github_pass)
    # driver.find_element_by_name("commit").click()
    password.send_keys(Keys.ENTER)

    os_folder_create(outputfolder)

    # INSERT KEYWORDS
    kw_query = ""
    for kw in keywords:
        kw_query = kw_query + "%22" + kw + "%22+"

    print("Search results:", flush=True)
    box_id = 0
    list_of_dicts = []
    list_filename = []
    try:
        for page in range(page_start, page_end + 1):
            print("\nPage " + str(page) + ": ", end=" ", flush=True)

            base_url = (
                "https://github.com/search?l=Python&p="
                + str(page)
                + "&q="
                + kw_query
                + "&type=Code&utf8=%E2%9C%93"
            )
            driver.get(base_url)
            html1 = driver.page_source
            soup = BeautifulSoup(html1, "lxml")

            box_id = 0
            # Scraping
            for desc, blob in zip(
                soup.findAll("div", class_="d-inline-block col-10"),
                soup.findAll("div", class_="file-box blob-wrapper"),
            ):

                desc_text = desc.text.strip()
                box_filename = desc_text.split("\n      –\n      ")[1].split("\n")[0].strip()

                if (FILTER and (box_filename not in list_filename)) or (not FILTER):
                    box_id = box_id + 1
                    print(box_id, end=" ", flush=True)

                    dict1 = {
                        "keywords": keywords,
                        "language": "Python",
                        "box_id": "",
                        "box_date": "",
                        "box_text": "",
                        "box_reponame": "",
                        "box_repourl": "",
                        "box_filename": "",
                        "box_fileurl": "",
                    }

                    urls = desc.findAll("a")
                    dict1["box_repourl"] = "https://github.com" + urls[0]["href"]
                    dict1["box_fileurl"] = "https://github.com" + urls[1]["href"]
                    driver.get(dict1["box_fileurl"])

                    dict1["box_id"] = box_id
                    dict1["box_filename"] = box_filename
                    dict1["box_reponame"] = desc_text.split(" ")[0].split("/")[-1].strip("\n")
                    dict1["box_date"] = (
                        desc_text.split("\n      –\n      ")[1]
                        .split("\n")[3]
                        .strip("Last indexed on ")
                    )

                    ######### DOWNLOADING    #####################################################################
                    if isdownload_file:
                        outputfile2 = (
                            outputfolder
                            + "/"
                            + dict1["box_reponame"]
                            + "_"
                            + dict1["box_filename"]
                            + "_"
                            + str(box_id)
                            + ".py"
                        )
                        driver.find_element_by_xpath('//*[@id="raw-url"]').click()
                        if isdebug:
                            print(driver.current_url, flush=True)
                        wget.download(url=driver.current_url, out=outputfile2)

                    blob_code = """ """
                    for k in blob.findAll("td", class_="blob-code blob-code-inner"):
                        aux = k.text.rstrip()
                        if len(aux) > 1:
                            blob_code = blob_code + "\n" + aux
                    dict1["box_text"] = blob_code

                    list_of_dicts.append(dict1)
                    list_filename.append(box_filename)

    except Exception as e:
        print(e)
    driver.quit()

    df = pd.DataFrame(list_of_dicts)
    print("Nb elements:" + str(len(df)))

    if iswrite_df:
        df.to_csv(
            outputfolder + "/" + outputfile, sep=r"§", encoding="utf-8", index=False, mode="w"
        )
    if isreturn_df:
        return df


def code_search_usage(
    module_name="jedi", method="Script", outputfolder="", sep=r"§", page_end=8, from_source="github"
):
    """      
        "from jedi import Script"   "Script("
        "from jedi"       "Script(" 
        "import jedi    .Script("
   output folder :  zdocs/module_sample/jedi/  username_reponame_filename.py 
   """
    import random

    ll_pattern = [
        ["import " + module_name, "." + method + "(", "test"],
        ["from " + module_name + " ", method + "(", "test"],
        ["import " + module_name, "." + method + "("],
        ["from " + module_name + " ", method + "("],
    ]

    outputfolder += "/" + module_name + "/"
    os_folder_create(outputfolder)
    output_codefile = outputfolder + "/codefile/"
    os_folder_create(output_codefile)

    if from_source == "github":
        df_all = None
        for ii, x in enumerate(ll_pattern):
            df = code_search_github(
                keywords=x,
                outputfolder=output_codefile,
                browser="",
                page_start=1,
                page_end=page_end,
                isreturn_df=1,
                iswrite_df=0,
                isdownload_file=1,
                isdebug=0,
                outputfile="",
            )

            try:
                df_all = pd.concat((df_all, df))
            except:
                df_all = df
        df_all.drop_duplicates("box_fileurl", inplace=True)
        outputfile = (
            outputfolder
            + "/"
            + module_name
            + "_"
            + method
            + "_sample_"
            + str(random.randint(1000, 9999))
            + ".txt"
        )
        df_all.to_csv(outputfile, sep=sep, encoding="utf-8", index=False, mode="w")
        print(outputfile)


######################################################################################################
############## Code Search #################################################################################
def conda_path_get(subfolder="package/F:/"):
    if os.__file__.find("envs") > -1:
        DIRANA = os.__file__.split("envs")[0] + "/"  # Anaconda from linux
    else:
        DIRANA = os.__file__.split("Lib")[0] + "/"  # Anaconda from root

    os_name = sys.platform[:3]
    if subfolder == "package":
        DIR2 = None
        if os_name == "lin":
            DIR2 = DIRANA + "/Lib/site-packages/"
        elif os_name == "win":
            DIR2 = DIRANA + "/Lib/site-packages/"
        return DIR2


def os_file_listall(dir1, pattern="*.*", dirlevel=1, onlyfolder=0):
    """ dirpath, filename, fullpath
   # DIRCWD=r"D:\_devs\Python01\project"
   # aa= listallfile(DIRCWD, "*.*", 2)
   # aa[0][30];   aa[2][30]
  """
    matches = {}
    dir1 = dir1.rstrip(os.path.sep)
    num_sep = dir1.count(os.path.sep)
    matches["dirpath"] = []
    matches["filename"] = []
    matches["fullpath"] = []

    for root, dirs, files in os.walk(dir1):
        num_sep_this = root.count(os.path.sep)
        if num_sep + dirlevel <= num_sep_this:
            del dirs[:]
        for f in fnmatch.filter(files, pattern):
            matches["dirpath"].append(os.path.splitext(f)[0])
            matches["filename"].append(os.path.splitext(f)[1])
            matches["fullpath"].append(os.path.join(root, f))
    return matches


def os_file_search_fast(fname, texts=None, mode="regex/str"):
    if texts is None:
        texts = ["myword"]
    res = []  # url:   line_id, match start, line
    nb = 0
    error_flag = False
    enc = "utf-8"
    fname = os.path.abspath(fname)
    try:
        if mode == "regex":
            texts = [(text, re.compile(text.encode(enc))) for text in texts]
            for lineno, line in enumerate(open(fname, "rb")):
                for text, textc in texts:
                    found = re.search(textc, line)
                    if found is not None:
                        try:
                            line_enc = line.decode(enc)
                        except:
                            line_enc = line
                        res.append((text, fname, lineno + 1, found.start(), line_enc))

        elif mode == "str":
            texts = [(text, text.encode(enc)) for text in texts]
            for lineno, line in enumerate(open(fname, "rb")):
                for text, textc in texts:
                    found = line.find(textc)
                    if found > -1:
                        try:
                            line_enc = line.decode(enc)
                        except:
                            line_enc = line
                        res.append((text, fname, lineno + 1, found, line_enc))

        elif mode == "full":
            texts = [(text, text.encode(enc)) for text in texts]
            with open(fname, "rb") as f1:
                lines = f1.readlines()

            for lineno, line in enumerate(lines):
                for text, textc in texts:
                    found = line.find(textc)
                    if found > -1:
                        try:
                            line_enc = line.decode(enc)
                        except Exception:
                            line_enc = line
                        res.append((text, fname, lineno + 1, found, line_enc))

    except IOError as xxx_todo_changeme:
        (_errno, _strerror) = xxx_todo_changeme.args
        print("permission denied errors were encountered")

    except re.error:
        print("invalid regular expression")

    return res


def code_search_file(
    srch_pattern=None,
    mode="str/regex",
    module_name_in="",
    folder_in="",
    folder_excluder=None,
    file_pattern="*.py",
    output_file="",
    dirlevel=20,
):
    if srch_pattern is None:
        srch_pattern = ["word1", "word2"]
    if folder_excluder is None:
        folder_excluder = [""]
    if module_name_in != "":
        folder_in = conda_path_get(subfolder="package")
        folder_in += "/" + module_name_in + "/"
    print(folder_in)

    list_all = os_file_listall(folder_in, pattern=file_pattern, dirlevel=dirlevel)
    ll = []
    for f in list_all["fullpath"]:
        ll = ll + os_file_search_fast(f, texts=srch_pattern, mode=mode)

    df = pd.DataFrame(ll, columns=["search", "filename", "lineno", "pos", "line"])
    if output_file != "":
        df.to_csv(output_file, sep="§", encoding="utf-8", mode="w")
    return df
    # aa= code_search_file( srch_pattern=[ u"from ","import "], mode="str", dir1=DIRCWD, file_pattern="*.py", dirlevel=1)
    # aa= code_search_file( srch_pattern=[ u"from ","import "], mode="full", dir1=DIRCWD, file_pattern="*.py", dirlevel=1)


################################################################################################
def np_list_dropduplicate(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


def np_list_flatten(l):
    if l is not None:
        if len(l) > 0:
            return [item for sublist in l for item in sublist]
    else:
        return []


def code_parse_line(li, pattern_type="import/import_externa"):
    """
    External Packages
  """
    ### Import pattern
    if pattern_type == "import":
        if li.find("from") > -1:
            l = li[li.find("from") + 4 : li.find("import")].strip().split(",")
        else:
            l = li.strip().split("import ")[1].strip().split(",")

        l = [x for x in l if x != ""]
        l = np_list_dropduplicate(l)
        return l

    # Only external
    if pattern_type == "import_extern":
        if li.find("from") > -1:
            l = li[li.find("from") + 4 : li.find("import")].strip().split(",")
        else:
            l = li.strip().split("import ")[1].strip().split(",")

        l = [x for x in l if x != ""]
        l = [x for x in l if x[0] != "."]
        l = [x.split(".")[0].split("as")[0].split("#")[0].strip() for x in l]
        l = np_list_dropduplicate(l)
        return l


def code_extract_pattern(
    pattern="import", module_name_in="conda", folder_in="", import_type1="extern/intern"
):

    if pattern == "import":
        df = code_search_file(
            srch_pattern=["import "],
            mode="str",
            module_name_in=module_name_in,
            folder_in=folder_in,
            folder_excluder=[""],
            file_pattern="*.py",
            output_file="",
            dirlevel=20,
        )

        df["module_list"] = df["line"].apply(lambda x: code_parse_line(x, "import"))
        df["module_list_extern"] = df["line"].apply(lambda x: code_parse_line(x, "import_extern"))
        lextern = np_list_dropduplicate(np_list_flatten(df["module_list_extern"].values))
        lall = np_list_dropduplicate(np_list_flatten(df["module_list"].values))
        return lextern, lall, df


# lextern, lall, df_import = code_search_pattern(pattern="import", module_name_in="conda", import_type1="extern/intern")
# print(lextern[:20], lall[:20], df_import.head(5))


def code_parse_file(filepattern="*.py", folder="", search_regex="", dirlevel=0):
    """
    Search into downloaded .py file using regex and put into nice tabular format
    for type inference.
      if module_name in file_i and  object_name_regex in line :
          High probability than object_name == our name
          --> Get the code string ---> Split into arguments -->
          --> for each argument, do testing of types
          
      
    """
    pass


######################################################################################################
######################################################################################################
IIX = 0


def pprint(a):
    global IIX
    IIX = IIX + 1
    print("\n--" + str(IIX) + ": " + a, flush=True)


def ztest():
    DIRCWD = "/home/ubuntu/ztest/"
    pprint("### Unit Tests")
    # os_folder_create("/ztest")

    pprint("module_doc_write")
    module_doc_write(module_name="jedi", outputfile="zz_doc_jedi.txt")

    pprint("module_signature_write")
    module_signature_write(module_name="json", isdebug=1)

    pprint("module_unitest_write")
    module_unitest_write(
        input_signature_csv_file="doc_json.csv", outputfile="zz_unitest_run_json.txt", isdebug=1
    )

    pprint("module_unitest_write: module name")
    module_unitest_write(module_name="json", outputfile="zz_unitest_run_json2.txt", isdebug=1)

    pprint("module_signature_compare: version between 2 docs.")
    df = module_signature_compare(
        "doc_json.csv", "doc_json.csv", export_csv="zz_json_compare.csv", return_df=1
    )
    print(df.head(5))
    """
    Might be tricky to get 2 version of numpy in same environnement....
      Need to generate in 2 different python envs  and get the csv
    """

    pprint("module Github Donwload")
    # df= github_code_search(keywords= ["import jedi",   "jedi.Script(" ], outputfolder= os.getcwd()+"/tmp/", browser="",
    #                       page_start=25, page_end= 25, isreturn_df=1, isdebug=1)
    # print( len(df), df.dtypes )

    pprint("code search")
    os_file_search_fast("codesource.py", texts=["from ", "import "], mode="str")
    aa = code_search_file(
        srch_pattern=["from ", "import "],
        mode="str",
        folder_in=DIRCWD,
        file_pattern="*.py",
        dirlevel=1,
    )
    aa.head(3)

    pprint("code search: import module conda")
    lextern, lall, df_import = code_extract_pattern(
        pattern="import", module_name_in="conda", import_type1="extern"
    )
    print(lextern[:20], lall[:20], df_import.head(5))


####################################################################################################
####################################################################################################
if __name__ == "__main__":
    import argparse

    ppa = argparse.ArgumentParser()
    ppa.add_argument("--do", type=str, default="", help=" unit_test")
    ppa.add_argument("--module", type=str, default="", help=" unit_test")
    arg = ppa.parse_args()

    if arg.do != "" and arg.module != "":
        print("Running Task")
        if arg.do == "module_signature_write":
            module_signature_write(arg.module)
        if arg.do == "module_unittestt_write":
            module_unitest_write(module_name=arg.module)
        else:
            globals()[arg.action](arg.module)  # Execute command

    if arg.do == "test":
        ztest()
