"""This Python code parser fetches variable information from the given source

The source may be given either as a .py filepath or as a directory path
containing multiple .py source files

The output is written to standard output in CSV format with the following
columns; it starts with a header row:
filepath,function_or_class_name,variable_name,is_local

Function_or_class_name defaults to (global) when there's no enclosing function
nor class

# pythoncodeparser

This Python code parser fetches variable information from the given source

The source may be given either as a .py filepath or as a directory path
containing multiple .py source files

The output is written to standard output in CSV format with the following
columns; it starts with a header row:
filepath,function\_or\_class\_name,variable\_name,is\_local

Function\_or\_class\_name defaults to (global) when there's no enclosing
function nor class

### Example:

**pythoncodeparser$ ./main.py src/file_finder.py**


filepath,function_or_class_name,variable_name,is_local
src/file_finder.py,findVariablesInFile,filepath,False
src/file_finder.py,findVariablesInDir,findVariablesInFile,False
src/file_finder.py,_walk,args,False
src/file_finder.py,_walk,f,True



### Run all unittests
**pythoncodeparser$ python3 -m unittest discover -p '*_test.py'**
"""

import ast
import os
import sys


def analyzeSource(source):
    """Analyzes the given Python source

  Args:
    source: string

  Returns:
    A dict over all variables encountered in the tree, in following form:
    {(ast.stmt function_or_class,
      str variable_name): bool is_local, ...}
  """
    tree = ast.parse(source)
    analyzer = ASTAnalyzer()
    analyzer.visit(tree)

    return analyzer.getVariables()


class ASTAnalyzer(ast.NodeVisitor):
    """Visits nodes in a Python AST and collects information on variables"""

    LOCAL = "local"
    GLOBAL = "global"
    FORCE_GLOBAL = "force_global"

    def __init__(self):
        self.function_or_class = None
        self.variables = {}

    def getVariables(self):
        """Lists variables parsed from the given AST

    Returns:
      A dict over all variables encountered in the tree, in following form:
      {(ast.stmt function_or_class,
        str variable): bool is_local, ...}
    """
        label_to_bool = {
            self.__class__.LOCAL: True,
            self.__class__.GLOBAL: False,
            self.__class__.FORCE_GLOBAL: False,
        }

        return {k: label_to_bool[v] for (k, v) in self.variables.items()}

    def _handleArguments(self, arguments):
        for arg in arguments.args:
            self._handleLocalVariable(variable_name=arg.arg)

    def _handleForceGlobalVariable(self, variable_name):
        key = (self.function_or_class, variable_name)

        self.variables[key] = self.__class__.FORCE_GLOBAL

    def _handleGlobalVariable(self, variable_name):
        key = (self.function_or_class, variable_name)

        self.variables.setdefault(key, self.__class__.GLOBAL)

    def _handleLocalVariable(self, variable_name):
        key = (self.function_or_class, variable_name)

        if self.variables.get(key) != self.__class__.FORCE_GLOBAL:
            self.variables[key] = self.__class__.LOCAL

    def _handleVariable(self, node):
        is_local = False
        if self.function_or_class is not None:
            if type(node.ctx) in [ast.Param, ast.Store, ast.AugStore]:
                is_local = True

        variable_name = node.id

        if is_local:
            self._handleLocalVariable(variable_name)
        else:
            self._handleGlobalVariable(variable_name)

        self.generic_visit(node)

    def _impl_visit_Function(self, node):
        old, self.function_or_class = self.function_or_class, node

        self._handleArguments(node.args)

        self.generic_visit(node)
        self.function_or_class = old

    def visit_AsyncFunctionDef(self, node):
        self._impl_visit_Function(node)

    def visit_ClassDef(self, node):
        old, self.function_or_class = self.function_or_class, node
        self.generic_visit(node)
        self.function_or_class = old

    def visit_FunctionDef(self, node):
        self._impl_visit_Function(node)

    def visit_Global(self, node):
        for variable_name in node.names:
            self._handleForceGlobalVariable(variable_name)

        self.generic_visit(node)

    def visit_Lambda(self, node):
        self._impl_visit_Function(node)

    def visit_Name(self, node):
        self._handleVariable(node)


def usage(message):
    """Prints the usage description"""
    print(message)
    print(
        f"""
Usage:
{sys.argv[0]} filepath|directory_path
"""
    )


def main():
    """Entry point"""
    try:
        path = sys.argv[1]
    except IndexError:
        usage("Either a filepath or a directory path must be provided")
        return

    if os.path.isdir(path):
        variables = findVariablesInDir(path)
    elif os.path.isfile(path):
        variables = findVariablesInFile(path)
    else:
        usage(f"The given path is neither a file nor a directory: {path}")
        return

    writeCSV(variables)


def findVariablesInFile(filepath):
    """Lists variables parsed from the given file

  Args:
    filepath: A path to a file containing Python code to be parsed

  Returns:
    A set of 4-tuples describing found variables
    {(str file,
      ast.stmt function_or_class,
      str variable,
      bool is_local), ...}
  """
    ret = set()

    with open(filepath, "r") as source_file:
        source = source_file.read()
        variables = analyzeSource(source)

        for ((function_or_class, variable_name), is_local) in variables.items():
            ret.add((filepath, function_or_class, variable_name, is_local))

    return ret


def findVariablesInDir(directory):
    """Lists variables parsed from the given directory

  Args:
    directory: A path to a directory containing Python code to be parsed

  Returns:
    A set of 4-tuples describing found variables
    {(str file,
      ast.stmt function_or_class,
      str variable,
      bool is_local), ...}
  """
    ret = set()

    for root, _, files in _walk(directory, onerror=_onerror_reraise, include_hidden=False):
        for filename in files:
            if filename.endswith(".py"):
                filepath = os.path.join(root, filename)
                ret |= findVariablesInFile(filepath)

    return ret


def _onerror_reraise(e):
    raise e


def _walk(*args, include_hidden=None, **kwargs):
    """A thin wrapper over os.walk which lists only non-hidden files on demand"""
    if include_hidden is None:
        raise ValueError("include_hidden must be specified")

    exclude_prefixes = () if include_hidden else (".")

    for root, dirs, files in os.walk(*args, **kwargs):
        files = [f for f in files if not f.startswith(exclude_prefixes)]
        dirs[:] = [d for d in dirs if not d.startswith(exclude_prefixes)]

        yield root, dirs, files


def writeCSV(variables, file_handle=sys.stdout):
    """Writes found variables' data to file_handle in CSV format

  The output is written to standard output by default

  The output starts with a header row:
  filepath,function_or_class_name,variable_name,is_local

  Function_or_class_name defaults to (global) when there's no enclosing function
  nor class

  Args:
    variables: A set of 4-tuples in format provided by the file_finder module
  """
    file_handle.write("filepath,function_or_class_name,variable_name,is_local\n")

    for filepath, function_or_class, variable_name, is_local in variables:
        function_or_class_name = (
            function_or_class.name if function_or_class is not None else "(global)"
        )

        file_handle.write(
            "%s,%s,%s,%s\n" % (filepath, function_or_class_name, variable_name, is_local)
        )


if __name__ == "__main__":
    main()
