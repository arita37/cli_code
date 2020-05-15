"""

Python memeory serializer
  pandas, dict, numpy, ...
  
  
  
  sesssion folder
  
  


"""
import pickle
import pandas as np, numpy as np





def save(obj, folder='/folder1/keyname', isabsolutpath=0):
    return py_save_obj(obj, folder=folder, isabsolutpath=isabsolutpath)


def load(folder='/folder1/keyname', isabsolutpath=0):
    return py_load_obj(folder=folder, isabsolutpath=isabsolutpath)

  

def save_session(folder , glob ) :
    
  if not os.path.exists(folder) :
    os.makedirs( folder )   
  
  lcheck = [ "<class 'pandas.core.frame.DataFrame'>", "<class 'list'>", "<class 'dict'>",
             "<class 'str'>" ,  "<class 'numpy.ndarray'>" ]  
  lexclude = {   "In", "Out" }
  
  for x, _ in glob.items() :
     if not x.startswith('_') and  x not in lexclude :
        x_type =  str(type(glob.get(x) ))
        if x_type in lcheck or x.startswith('clf')  :
            try :
              print( save( glob[x], folder  + "/" + x + ".pkl") )
            except Exception as e:
              print(x, x_type, e)






def load_session(folder, glob=None) :
  """
     Data Load session      
    
  """
  print(folder)
  for dirpath, subdirs, files in os.walk( folder ):
    for x in files:
       filename = os.path.join(dirpath, x) 
       x = x.replace(".pkl", "")
       try :
         glob[x] = load(  filename )
         print(filename) 
       except Exception as e :
         print(filename, e)


def py_save_obj(obj, folder='/folder1/keyname', isabsolutpath=0):
    import pickle
    if isabsolutpath == 0 and folder.find('.pkl') == -1:  #Local Path
        dir0, keyname = z_key_splitinto_dir_name(folder)
        os_folder_create(DIRCWD + '/aaserialize/' + dir0)
        dir1 = DIRCWD + '/aaserialize/' + dir0 + '/' + keyname + '.pkl'
    else:
        dir1 = folder

    with open(dir1, 'wb') as f:
        pickle.dump(obj, f, pickle.HIGHEST_PROTOCOL)
    return dir1


def py_load_obj(folder='/folder1/keyname', isabsolutpath=0, encoding1='utf-8'):
    '''def load_obj(name, encoding1='utf-8' ):
         with open('D:/_devs/Python01/aaserialize/' + name + '.pkl', 'rb') as f:
            return pickle.load(f, encoding=encoding1)
    '''
    import pickle
    if isabsolutpath == 0 and folder.find('.pkl') == -1:
        dir0, keyname = z_key_splitinto_dir_name(folder)
        os_folder_create(DIRCWD + '/aaserialize/' + dir0)
        dir1 = DIRCWD + '/aaserialize/' + dir0 + '/' + keyname + '.pkl'
    else:
        dir1 = folder

    with open(dir1, 'rb') as f:
        return pickle.load(f)

      
      
      

      
def z_key_splitinto_dir_name(keyname):
    lkey = keyname.split('/')
    if len(lkey) == 1: dir1 = ""
    else:
        dir1 = '/'.join(lkey[:-1])
        keyname = lkey[-1]
    return dir1, keyname
  
  
  
      
      
      
      
      
