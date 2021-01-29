# -*- coding: utf-8 -*-
"""

Alll related to json dynamic parsing


"""
import os
import re
import fnmatch
import pandas as pd
import json
import importlib
import time
# import toml
from pathlib import Path
#from jsoncomment import JsonComment ; json = JsonComment()
import fire
from inspect import getmembers


####################################################################################################
class to_namespace(object):
    def __init__(self, adict):
        self.__dict__.update(adict)

    def get(self, key):
        return self.__dict__.get(key)


def log(*s, n=0, m=0):
    sspace = "#" * n
    sjump = "\n" * m
    print("")
    print(sjump, sspace, *s, sspace, flush=True)


####################################################################################################
def os_package_root_path(filepath="", sublevel=0, path_add=""):
    """
       get the module package root folder
    """
    from pathlib import Path
    import os
    import inspect

    path = os.path.abspath((__file__))
    #path = Path(inspect.getfile()).parent
    # print( path )
    # path = Path(os.path.realpath(filepath)).parent
    for i in range(1, sublevel + 1):
        path = path.parent

    path = os.path.join(path.absolute(), path_add)
    return path


###################################################################################################
def path_norm(path):
    """
     Nornalize Path
    """
    return path


def params_json_load(path, config_mode="test",
                     tlist=["model_pars", "data_pars", "compute_pars", "out_pars"]):
    #from jsoncomment import JsonComment ; json = JsonComment()
    pars = json.load(open(path, mode="r"))
    pars = pars[config_mode]

    ### HyperParam, model_pars, data_pars,
    list_pars = []
    for t in tlist:
        pdict = pars.get(t)
        if pdict:
            list_pars.append(pdict)
        else:
            log("error in json, cannot load ", t)

    return tuple(list_pars)

#########################################################################################
#########################################################################################


def load_function(package="mlmodels.util", name="path_norm"):
    import importlib
    return getattr(importlib.import_module(package), name)


def load_function_uri(uri_name="path_norm"):
    """
    #load dynamically function from URI

    ###### Pandas CSV case : Custom MLMODELS One
    #"dataset"        : "mlmodels.preprocess.generic:pandasDataset"

    ###### External File processor :
    #"dataset"        : "MyFolder/preprocess/myfile.py:pandasDataset"


    """
    import importlib
    import sys
    from pathlib import Path
    pkg = uri_name.split(":")

    assert len(
        pkg) > 1, "  Missing :   in  uri_name module_name:function_or_class "
    package, name = pkg[0], pkg[1]

    try:
        # Import from package mlmodels sub-folder
        return getattr(importlib.import_module(package), name)

    except Exception as e1:
        try:
            # Add Folder to Path and Load absoluate path module
            path_parent = str(Path(package).parent.parent.absolute())
            sys.path.append(path_parent)
            # log(path_parent)

            # import Absolute Path model_tf.1_lstm
            model_name = Path(package).stem  # remove .py
            package_name = str(Path(package).parts[-2]) + "." + str(model_name)
            #log(package_name, model_name)
            return getattr(importlib.import_module(package_name), name)

        except Exception as e2:
            raise NameError(f"Module {pkg} notfound, {e1}, {e2}")


def load_callable_from_uri(uri):
    assert(len(uri) > 0 and ('::' in uri or '.' in uri))
    if '::' in uri:
        module_path, callable_name = uri.split('::')
    else:
        module_path, callable_name = uri.rsplit('.', 1)
    if os.path.isfile(module_path):
        module_name = '.'.join(module_path.split('.')[:-1])
        spec = importlib.util.spec_from_file_location(module_name, module_path)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)
    else:
        module = importlib.import_module(module_path)
    return dict(getmembers(module))[callable_name]


def load_callable_from_dict(function_dict, return_other_keys=False):
    function_dict = function_dict.copy()
    uri = function_dict.pop('uri')
    func = load_callable_from_uri(uri)
    try:
        assert(callable(func))
    except:
        raise TypeError(f'{func} is not callable')
    arg = function_dict.pop('arg', {})
    if not return_other_keys:
        return func, arg
    else:
        return func, arg, function_dict


def test_functions_json(arg=None):
    """

         args :[]   , kw_args : {}

    """
    path = path_norm("dataset/test_json/test_functions.json")
    dd = json.load(open(path))['test']

    for p in dd:
        try:
            log("\n\n", "#"*20, p)

            myfun = load_function_uri(p['uri'])
            log(myfun)

            w = p.get('args', [])
            kw = p.get('kw_args', {})

            if len(kw) == 0 and len(w) == 0:
                log(myfun())
            elif len(kw) > 0 and len(w) > 0:
                log(myfun(*w,  ** kw))
            elif len(kw) > 0 and len(w) == 0:
                log(myfun(** kw))
            elif len(kw) == 0 and len(w) > 0:
                log(myfun(*w))

        except Exception as e:
            log(e, p)


def json_to_object(ddict):
    """
       Execute a function from json to actual arguments
       {uri:    args :[]   , kw_args : {}   }
        { "uri" : "mlmodels.util.log", "args" : [ "x1" , "passed"] ,     "kw_args" : { }  }
       ,{ "uri" : "mlmodels.util:log", "args" : [ "x1" , "passed"] ,      "kw_args" : { }   }     

       , {"uri": "mlmodels.data:download_gogledrive",
          "args": [[{"fileid": "1-K72L8aQPsl2qt_uBF-kzbai3TYG6Qg4", "path_target": "ztest/covid19/test.json"},
                    {"fileid": "1-8Ij1ZXL9YmQRylwRloABdqnxEC1mhP_", "path_target": "ztest/covid19/train.json" }
            ]], 
        "kw_args" : {}} 

    """
    p = ddict
    try:
        myfun = load_function_uri(p['uri'])
        w = p.get('args', [])
        kw = p.get('kw_args', {})
        if len(kw) == 0 and len(w) == 0:
            return myfun()
        elif len(kw) > 0 and len(w) > 0:
            return myfun(*w,  ** kw)
        elif len(kw) > 0 and len(w) == 0:
            return myfun(** kw)
        elif len(kw) == 0 and len(w) > 0:
            return myfun(*w)
    except Exception as e:
        log(e, p)


def json_norm_val(x):
    if x == "none":
        return None
    if x == "":
        return None


def json_norm(ddict):
    return {json_norm_val(x) for k, x in ddict.items()}


def json_parse(ddict):
    """
      https://github.com/arita37/mlmodels/blob/dev/mlmodels/dataset/test_json/test_functions.json
      https://github.com/arita37/mlmodels/blob/dev/mlmodels/dataset/json/benchmark_timeseries/gluonts_m5.json
          "deepar": {
         "model_pars": {
             "model_uri"  : "model_gluon.gluonts_model",
             "model_name" : "deepar",
             "model_pars" : {
                 "prediction_length": 12, 
                 "freq": "D",
                 "distr_output" :  {"uri" : "gluonts.distribution.neg_binomial:NegativeBinomialOutput"}, 

                 "distr_output" :  "uri::gluonts.distribution.neg_binomial:NegativeBinomialOutput", 
    """
    import copy
    js = ddict
    js2 = copy.deepcopy(js)

    def parse2(d2):
        if "uri" in d2:
            # Be careful not to include heavy compute
            return json_to_object(d2)
        else:
            return json_norm(d2)

    for k, val in js.items():
        if isinstance(val, dict):
            js2[k] = parse2(val)

        elif "uri::" in val:  # Shortcut when nor argument
            js2[k] = json_to_object({"uri":  val.split("uri::")[-1]})
        else:
            js2[k] = json_norm_val(val)
    return js2


def json_codesource_to_json(fpath):
    """
        read a python file and create json
        Ex:
        def MyClass():
           def __init__(fname, zout=""):
           def method1(x=1, y=2)
       --->
               {"uri": "MyClass",   "arg" : ["fname"] , "kwargs": {"out" : "ztmp"} }       

               {"uri": "MyClass.method1",   "arg" : [] , "kwargs": {"x" : 1, "y" : 2, } }       


    """
    ff = open(fpath, mode="r")


###################################################################################################
def os_folder_getfiles(folder, ext, dirlevel=-1, mode="fullpath"):
    """

    :param folder: folder path to be analyzed
    :type folder: string
    :param ext: file extension hint example: "*.json"
    :type ext: string
    :param dirlevel: number of levels to be analyzed
    :type dirlevel: int
    :param mode: either fullpath or filename
    :type mode: string
    :return: list of files paths or names (depending on mode param)
    :rtype: list of str
    """

    files_list = os.listdir(folder)
    if dirlevel == 0:
        if (mode == "fullpath"):
            return [os.path.join(folder, p) for p in files_list if fnmatch.fnmatch(p, ext)]
        if (mode == "filename"):
            return [f for f in files_list if fnmatch.fnmatch(f, ext)]
        else:
            print("Error: mode parameter is either fullpath or filename")
    elif (dirlevel == -1 or dirlevel >= 1):
        all_files = []
        for entry in files_list:
            full_path = os.path.join(folder, entry)
            if os.path.isdir(full_path):
                if dirlevel == -1:
                    all_files += os_folder_getfiles(full_path,
                                                    ext, dirlevel, mode)
                if dirlevel >= 1:
                    all_files += os_folder_getfiles(full_path,
                                                    ext, dirlevel-1, mode)
            elif fnmatch.fnmatch(entry, ext):
                if (mode == "fullpath"):
                    all_files.append(full_path)
                if (mode == "filename"):
                    all_files.append(entry)
    else:
        print("Error: dirlevel parameter is either -1 or >=1")
    return all_files


def jsons_to_df(json_paths):
    """

    :param json_paths: list of json paths
    :type json_paths: list of str
    :return: DataFrame of the jsons
    :rtype: DataFrame
    """
    indexed_dicts = []
    problem = 0
    for i in range(len(json_paths)):
        try:
            with open(json_paths[i]) as json_file:
                d = dict()
                d['Path'] = json_paths[i]
                d['Json'] = json.load(json_file)
                indexed_dicts.append(d)
        except:
            if problem == 0:
                print("Files That have a structure problem:\n")
            problem += 1
            print('\t', json_paths[i])
            continue
    print("Total flawed jsons:\t", problem)
    all_jsons = []
    for i in range(len(indexed_dicts)):
        all_jsons.append(indexed_dicts[i]['Json'])

    ddf = pd.json_normalize(all_jsons)
    result = []
    keys = list(ddf.columns)
    for i in range(len(all_jsons)):
        for k in keys:
            if(str(ddf[k][i]) != 'nan'):
                d = dict()
                d['file_path'] = indexed_dicts[i]['Path']
                d['filename'] = os.path.basename(indexed_dicts[i]['Path'])
                d['json_name'] = k.split(".")[0]
                d['fullname'] = k
                d['field_value'] = ddf[k][i]
                result.append(d)
    del ddf
    df = pd.DataFrame(result)

    def getlevel(x, i):
        try:
            return x.split(".")[i]
        except:
            return ""
    df['level_1'] = df['fullname'].apply(lambda x:  getlevel(x, 1))
    df['level_2'] = df['fullname'].apply(lambda x:  getlevel(x, 2))
    df['level_3'] = df['fullname'].apply(lambda x:  getlevel(x, 3))
    return df


def dict_update(fields_list, d, value):
    """
    :param fields_list: list of hierarchically sorted dictionary fields leading to value to be modified
    :type fields_list: list of str
    :param d: dictionary to be modified
    :type d: dict
    :param value: new value
    :type value: any type
    :return: updated dictionary
    :rtype: dict
    """
    if len(fields_list) > 1:
        l1 = fields_list[1:]
        k = fields_list[0]
        if k not in list(d.keys()):
            d[k] = dict()
        d[k] = dict_update(l1, d[k], value)
    else:
        k = fields_list[0]
        d[k] = value
        return d
    return d


def json_csv_to_json(file_csv="", out_path="dataset/"):
    """

    :param csv: csv file containing jsons to be normalized
    :type csv: str
    :return: list of normalized jsons as dictionaries
    :rtype: list of dicts
    """
    ddf = pd.read_csv(file_csv)
    paths = list(ddf['file_path'].unique())
    fullnames = list(ddf['fullname'].unique())
    dicts = []
    for fp in paths:
        dd = dict()
        for fn in fullnames:
            l = fn.split('.')
            dd = dict_update(l, dd, None)
        json_ddf = ddf[ddf['file_path'] == fp]
        filled_values = list(json_ddf['fullname'])
        for fv in filled_values:
            dd.update(dict_update(fv.split('.'), dd, list(
                json_ddf[json_ddf['fullname'] == fv]['field_value'])[0]))
        dicts.append(dd)

    dataset_dir = path_norm(out_path)
    #dataset_dir = os_package_root_path()+'dataset'
    # os.chdir(dataset_dir)
    paths = [p[len(dataset_dir)+1:] for p in paths]

    new_paths = []
    for i in range(len(paths)):
        lp = paths[i].split('/')
        lp[0] = 'normalized_jsons'
        dire = '/'.join(''.join(i) for i in lp[:len(lp)-1])
        new_paths.append(dire)
    for p in list(set(new_paths)):
        if not os.path.exists(p):
            os.makedirs(p)

    for i in range(len(paths)):
        with open(new_paths[i] + '/' + paths[i].split('/')[-1], 'w') as fp:
            json.dump(dicts[i], fp, indent=4)
    print("New normalized jsons created, check mlmodels\\mlmodels\\dataset")
    return dicts


def test_json_conversion():
    """
    Function to test converting jsons in dataset/json to normalized jsons
    :rtype: list of normalized jsons as dictionaries
    """
    json_folder_path = path_norm("dataset\\json")
    jsons_paths = os_folder_getfiles(json_folder_path, ext="*.json")
    df = jsons_to_df(jsons_paths)
    df.to_csv('table_json.csv')
    print('csv created successfully')
    time.sleep(1)
    dicts2 = json_csv_to_json('table_json.csv')
    print(dicts2)
    return dicts2


def main():
    pass


# Testing code
if __name__ == "__main__":
    import fire
    fire.Fire()

    # python mlmodels/util_json.py  test_json_conversion
