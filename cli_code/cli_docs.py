# -*- coding: utf-8 -*-
"""
 python  cli_docs.py  --do doc    --module sys

 cli_doc  --do test  

 cli__doc  --do docs    --module jedi


##############  TODO :   ###########################################################
  1) Arguments of functions or methos are missing in XXXX_doc.txt :
       numpy.random.binomial(n, p, size=None)
       Please add them

  Some issues with :
      cannot find __path__ for os,sys modules
    


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
import regex
import pkgutil
import shutil
import stat



import pandas as pd
####################################################################################################



###################################################################################################
SEP =  "\\"  if  "win" in sys.platform  else "/"


COLS_NAME = [
    "module_name",
    "module_version",
    "full_name",
    "prefix",
    "obj_name",
    "obj_doc",
    "object_type",
    "arg_full",
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


def module_load(name_or_path="") :
    name_or_path = os.path.abspath(name_or_path)

    try :
        module = import_module(m_name)
        print("Module imported", module)
        return module
    except :
        #sys.path.add(m_name)  ## Absolute path
        mpath = name_or_path.split(SEP)[:-1]
        mpath = SEP.join( mpath )
        print(mpath)
        sys.path.insert(0, mpath )  ## Absolute path
        m_name = name_or_path.split(SEP)[-1]
        module = import_module(m_name)
        print("Module imported", module, flush=True)
        return module



def module_getname(name) :
   if SEP not in name : return name 
   else  :
    return name.split(SEP)[-1]



def module_getpath(name) :
    return name








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
        self.module = module_load(self.module_name)
        self.module_isbuiltin = self.get_module_isbuiltin()
        self.submodules = self.get_submodules()
        self.functions = self.get_functions()
        self.functions_built = self.get_builtin_functions()
        self.classes = self.get_classes()
        self.class_methods = self.get_class_methods()

    def get_module_version(self):
        """get_module_version(self) Module method
        return the version of the module taken as an instance argument."""
        try :
            return self.module.__version__
        except :
            return 0

    def get_module_isbuiltin(self):
        builtin_modules = list(sys.builtin_module_names)
        for x in builtin_modules:
            if self.module.__name__ == x:
                return True
        return False 

    def get_submodules(self):
        """get_submodules(self) Module method
        return a list of submodules of the module taken as an instance argument."""
        submodules = {} 
        
        try:      
            for loader, name, is_pkg in walk_packages(self.module.__path__, self.module.__name__ + "."):
                if self.is_imported(name):
                    submodules[name] = self.get_submodule(self.get_mlattr(name))
        except:
#            for loader, name, is_pkg in walk_packages(sys.path, self.module.__name__ + "."):
            for loader, name, is_pkg in walk_packages(None, self.module.__name__ + "."):
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

    def get_builtin_functions(self):
        """get_builtin_functions(self) Module method
        return a list of functions of the module taken as an instance argument."""
        functions_built = {}
        if self.module_isbuiltin:
            mod = eval(self.module.__name__)
        else:
            mod = self.module.__name__
        for function_name, function in inspect.getmembers(
            mod, lambda f: inspect.isfunction(f) or inspect.isbuiltin(f) 
            ):                
                functions_built[str_join(self.module.__name__, function_name)] = function
        return functions_built

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

def obj_get_full_signature(obj):
    arg_full = OrderedDict()
    try:
        args = inspect.signature(obj)
    except:
        args = ""
    arguments = str(args)
    arguments = re.sub('()', '', arguments)
    arg_full[1] = arguments
    return arg_full

    
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
    if module.module_isbuiltin:
        members = module.functions_built
    else:
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
        #"function_type":[],
        "object_type": [],
        "arg_full": [],
        "arg": [],
        "arg_default_value": [],
        "arg_type": [],
        "arg_info": [],
        
    }

    for member_name, member in members.items():
        
        isclass = obj_class_ispecial(member)
        isfunction = inspect.isfunction(member)
        ismethod = inspect.ismethod(member)
                        
        if isclass or isfunction or ismethod or module.module_isbuiltin:
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
            if not module.module_isbuiltin:
                doc_df["arg_full"].append(tuple(obj_get_full_signature(member.__init__ if isclass else member).values()))
            else:
                doc_df["arg_full"].append(None)
                   
    return doc_df


def pd_df_expand(x):
    y = pd.DataFrame(x.values.tolist())
    return y.stack()


def pd_df_format(df, index, filter=True):
    level_to_drop = "level_{}".format(len(index))
    # if filter: df = filter_data(['private_methods'], pd.DataFrame(df))   # We keep ALL the data as RAW data in csv.
    print(df)
    
    df =  df.set_index(index)
    
    #### Issues with Empty list
    df = df.apply(lambda x: pd_df_expand(x), 1)
    

    formated_df = (
        df.stack()
        .reset_index()
        .drop(level_to_drop, 1)
    )
   
    #formated_df.columns = index + [x for x in df.columns if x not in index]
    return formated_df


def module_signature_write(module_name, outputfile="", return_df=0, isdebug=0):
    """  Write down the files.
         
    """
    df = module_signature_get(module_name)
    df = pd_df_format(pd.DataFrame(df), COLS_NAME)
    df = df.sort_values("full_name", ascending=True)
    
    if return_df == 1:
        return df  # return df
    else:
        outputfile = (
            outputfile
            if outputfile != ""
            else os.path.join(os.getcwd(), str_join("doc_" + module_name, "csv"))
        )
        if isdebug:
            print("Signature Writing")
        print(outputfile)
        df.to_csv(outputfile, index=False, mode="w")


#############################################################################################################
# def drop_private_methods(data):
#    return data.drop(data[data.obj_name.str.contains('^_')].index)


# def filter_data(filter_type, data):
#    for filter in filter_type:
#        if filter == 'private_methods':
#            data = drop_private_methods(data)
#    return data


def obj_arg_filter_apply_1(df, filter_list=None):
    """  Apply Sequential Filtering to the frame of argument
    :param df: Signature Datframe
    :param filter_list:    ('sort_ascending', 1)  we can add very easily new filter
    :return: dataframe filtering
    """
    if filter_list is None:
        filter_list = [("filter_name", "arg_full")]

    for (f, farg) in filter_list:
        if f == "class_only":  df = df[(df["function_type"] == "class_method") | (df["function_type"] == "class")]
        if f == "function_only":  df = df[(df["function_type"] == "function")]
        if f == "public_only":  df = df[-df["obj_name"].str.startswith(r"__", na=False)]
        if f == "private_only":  df = df[(df["obj_name"].str.startswith(r"__", na=False))]
        if f == "fullname_regex":df = df[df["full_name"].str.contains(farg, na=False)]
        if f == "fullname_startwith":  df = df[df["full_name"].str.startswith(farg, na=False)]
        if f == "fullname_exclude":   df = df[-df["full_name"].str.contains(farg, na=False)]
        if f == "sort_ascending":  df = df.sort_values("full_name", ascending=farg)

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
    try:
        data = data0[data0["arg"] != "self"].copy(deep=True)  # self argument
    except:
        data = data0.copy(deep=True)
        data["arg"] = "" 
    data = obj_arg_filter_apply_1(data, filter_list)  # Apply Sequential Fitlering

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
    print("writing outpit file ", outputfile)
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
    df_data = obj_arg_filter_apply_1(df_data, filter_list)  # Apply Sequential Fitlering
    # print(data.head(5))
    
    ## Generate  1 line function
    def agg_in_1line(dfi):
        full_name = dfi.full_name.values[0]
        
        try :
    #      args = "(" + ",".join(list(dfi["arg_full"].values)) + ")"
          args = ",".join(dfi.arg_full.values[0])
        except :
           args = "()"
        
        function = full_name + args
        
        # function.replace( ["'", ",\)"], ["", ")"], regex=True,inplace=True )
        #return pd.Series([args, function], ["arg", "function"])
        return pd.Series([function], ["function"])

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
        try:
            module_name1 = df_data["module_name"].values[0] + "_" + df_data["module_version"].values[0]
        except :
            module_name1 = df_data["module_name"].values[0]
        
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
    try:
        df1["unique_name"] = df1.full_name + "-" + df1.arg
    except:
        df1["unique_name"] = df1.full_name
        
    
    try:
        df2["unique_name"] = df2.full_name + "-" + df2.arg
    except:
        df2["unique_name"] = df2.full_name

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



################################################################################################
def np_list_dropduplicate(seq):
    seen = set()
    seen_add = seen.add
    return [x for x in seq if not (x in seen or seen_add(x))]


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

######################################################################################################
def module_tofolder(name_or_path, outputfolder="./zmp", isdebug=1):
        ### Export docs to specific folder
        module_name = module_getname(name_or_path)

        module = Module(name_or_path)
        module_version = module.get_module_version()
        

        path = f"{outputfolder}/{module_name}/{module_version}/"
        os.makedirs(path, exist_ok=True)

        log("module_doc_write")
        module_doc_write(module_name, outputfile= f"{path}/doc_{module_name}.txt")
    
        
        log("module_signature_write")
        module_signature_write(module_name, outputfile= f"{path}/list_{module_name}.csv", isdebug=isdebug)
            
        
        log("module_unitest_write")
        module_unitest_write(
            input_signature_csv_file= f"{path}/list_{module_name}.csv", outputfile= f"{path}/zz_unitest_run_{module_name}.txt", isdebug=isdebug      
        )

        log("module_unitest_write: module name")
        module_unitest_write(module_name = module_name, outputfile=path+ f"/zz_unitest_run_{module_name}{2}.txt", isdebug=isdebug)

        
        
        
        

######################################################################################################
######################################################################################################
IIX = 0


def log(*args, reset=0):
    global IIX
    IIX = IIX + 1
    a = ",".join(args)
    print( f"\n--{IIX} : {a}", flush=True)


def ztest():
    # DIRCWD = "/home/ubuntu/ztest/"
    print(os.getcwd())
    os.makedirs("ztmp",exist_ok=True)
    log("### Unit Tests")
    for f in [  "json",  "os",  "numpy", "template/simplejson/" ] :
        try :
            # os_folder_create("/ztest")
            log("module_doc_write", f)
            module_doc_write(module_name=f, outputfile= f"ztmp/doc_{f}.txt")

          
            log("module_signature_write",f)
            module_signature_write(module_name= f, outputfile= f"ztmp/list_{f}.csv", return_df=0 ,isdebug=1)

            
            log("module_unitest_write", f)
            module_unitest_write(
                input_signature_csv_file= f"ztmp/list_{f}.csv", outputfile= f"ztmp/zz_unitest_run_{f}.txt", isdebug=1)
                

            log("module_unitest_write: module name")
            module_unitest_write(module_name=f, outputfile="ztmp/zz_unitest_run_{f}_02.txt", isdebug=1)
           

            log("module_signature_compare: version between 2 docs.")
            """
            Might be tricky to get 2 version of numpy in same environnement....
              Need to generate in 2 different python envs  and get the csv
            """
            df = module_signature_compare(
                f"doc_{f}.csv", f"doc_{f}.csv", export_csv= f"zz_{f}_compare.csv", return_df=1     
            )
            print(df.head(5))

        except Exception as e :
            print(f, e)
        

def ztest_mod(mod):
    DIRCWD = "/home/ubuntu/ztest/"
    
    log("### Unit Tests")
    # os_folder_create("/ztest")
    log("module_doc_write")
    module_doc_write(mod, outputfile="ztmp/doc_{}.txt".format(mod))
   
    log("module_signature_write")
    module_signature_write(mod, outputfile="ztmp/list_{}.csv".format(mod), isdebug=1)
        
    
    log("module_unitest_write")
    module_unitest_write(
        input_signature_csv_file="ztmp/list_{}.csv".format(mod), outputfile="ztmp/zz_unitest_run_{}.txt".format(mod), isdebug=1      
    )
  
    log("module_unitest_write: module name")
    module_unitest_write(module_name = mod, outputfile="ztmp/zz_unitest_run_{}{}.txt".format(mod, "2"), isdebug=1)
    

    log("module_signature_compare: version between 2 docs.")
    df = module_signature_compare(
        "doc_{}.csv".format(mod), "doc_{}.csv".format(mod), export_csv="ztmp/zz_{}_compare.csv".format(mod), return_df=1     
    )
   
    print(df.head(5))
    
    """
    Might be tricky to get 2 version of numpy in same environnement....
      Need to generate in 2 different python envs  and get the csv
    """


def main():
    import argparse
    
    p = argparse.ArgumentParser()
    p.add_argument("--do", type=str, default="", help=" unit_test")
    p.add_argument("--module", type=str, default="", help=" unit_test")

    p.add_argument("--outputfolder", type=str, default="ztmp/", help=" file output")  
    p.add_argument("--outputfile", type=str, default="", help=" file output")        
    arg = p.parse_args()

    m_name = module_getname(arg.module)
    m_path = module_getpath(arg.module)

    if arg.do == "": 
        print("""
          cli_repo_docs  --do doc   --module  jedi    --outputfolder ztmp/ 
        """)

    if arg.do == "test":
        if arg.module != "":
            ztest_mod(arg.module)
        else:
            ztest()


    if arg.do != "" and arg.module != "":
        
        module   = module_load( arg.module )
        filename = m_name if arg.outputfile == "" else arg.outputfile


        if arg.do == "doc_single":
           print("Generate Signature", arg.module, arg.do)
           module_signature_write(arg.module, outputfile= f"{arg.outputfolder}/doc_{filename}.txt")
           module_unitest_write(module_name = module, outputfile= f"zz_unitest_run_{module}{2}.txt", isdebug=1)
           

        if arg.do == "module_unittest":
            module_unitest_write(module_name= arg.module)


        if arg.do == "doc":
            module_tofolder(arg.module, arg.outputfolder)


        else  :
            print("No valid action")    
        

####################################################################################################
####################################################################################################
if __name__ == "__main__":
   main()


