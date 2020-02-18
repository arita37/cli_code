"""
# Merge-Conda-YAML
This is a very simple piece of script that allows user to merge multiple YAML files generated anaconda into a single unified YAML.
The output of this script is two files, one is the merged YAML file while the other is the requirements.txt file ready to be scanned by pip.



## Example
python cli_conda_merge.py ./file1.yml ./file2.yml ./file3.yml
cli_conda_merge.py ./file1.yml ./file2.yml ./file3.yml



## Changing Output Filenames

In order to change the name of the output files, edit the "dump(output_yaml, piplist)" function definition.

"""

import yaml
import sys
import argparse
import os
import datetime

from os import path
from collections import OrderedDict, deque
from copy import deepcopy

class MergeError (Exception):
    """Exceptions that will be used to notify users if any error occurred during the merge"""
    pass

def parse_args(argv=None):
    """Parse command line arguments (or user provided ones as list)"""
    description = sys.modules[__name__].__doc__
    parser = argparse.ArgumentParser(
        description=description,
        formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument('yamls', nargs='+')     # Place the files that were recieved in 'yamls' namespace
    return parser.parse_args(argv)

def getPriorityList():
    """ 
    A simple funciton that reutrns all the packages that 
    need to be treated as high-priority dependencies 
    """
    priorities = ['pytorch', 'tensorflow']
    return priorities

def prioritySort (dependencies):
    """ 
    Function that will sort the dependencies for pip's requirements.txt format
    while prioritizing the packages defined in getPriorityList() function
    """
    priorityList = getPriorityList()

    # Removing duplicates
    dependencies = list(dict.fromkeys(dependencies))

    for i in dependencies:
        if i in priorityList:
            dependencies.insert(0, dependencies.pop(dependencies.index(i)))
    
    return dependencies

def getPipRequirementsContent(dependencies):
    """ Function to convert conda dependencies and pip dependencies to a single pip list and sort it """
    pips = dependencies[len(dependencies)-1]
    dependencies.pop(len(dependencies)-1)

    for pip in pips.get('pip'):
        dependencies.append(pip)
    
    dependencies = prioritySort(dependencies)
    return dependencies

def sortYamlDeps(dependencies):
    """ Function that will sort and prioritize dependencies of the environment YAML """
    # Separate out pips and conda dependencies
    pips = dependencies[len(dependencies)-1]
    dependencies.pop(len(dependencies)-1)

    # Convert pips to list
    """
    remember to convert it back to dict. like this:
    """
    pips = pips.get('pip')

    # Remove duplicates from pip. If conda ackage of the same 
    # name is available, remove its counterpart from pip.
    for condadep in dependencies:
        for pipdep in pips:
            if condadep.startswith(pipdep) or pipdep.startswith(condadep):
                pips.remove(pipdep)

    # Sort both lists based on priorities
    dependencies = prioritySort(dependencies)
    pips = prioritySort(pips)

    # Put pips back in dependencies list
    dependencies.append({'pip': pips})
    
    return dependencies

def dump(output_yaml):
    """Function used to dump the final state of the output files

    This Function will deal with the dumping of the merged YAML
    file as well as the requirements.txt file formatted to be used by PIP
    
    """
    # Outputting to files
    cwd = os.getcwd()
    today = datetime.datetime.today()
    suffix = str(today.day) + str(today.month) + "_" + str(today.hour) + str(today.minute) + str(today.second)
    outputyamlfilename = "mergedYAML_{}.yml".format(suffix)
    outputreqfilename = "mergedPIPs_{}.txt".format(suffix)

    # Writing YAML file
    output_yaml['dependencies'] = sortYamlDeps(output_yaml.get('dependencies'))
    with open(path.join(cwd, outputyamlfilename), 'w') as f:
        yaml.dump(output_yaml, f, indent=2, default_flow_style=False)

    # Writing requirements.txt file
    piplist = getPipRequirementsContent(output_yaml.get('dependencies'))

    with open (path.join(cwd, outputreqfilename), 'w') as rf:
        for pipdep in piplist:
            rf.write(pipdep)
            rf.write("\n")
    
    print ("\nThe output YAML and pip requirements have been written in {} and {}.".format(outputyamlfilename, outputreqfilename))



def merge_envs (args):
    """Main entry point for the script"""
    # Check if all the yaml files exist 
    for f in args.yamls:
        if not path.exists(f):
            raise MergeError("The following file does not exist: {}".format(f))

    # Load all files
    yaml_files = []
    for f in args.yamls:
        with open(f) as file:
            yaml_files.append(yaml.safe_load(file))
    
    # The main loop that will be calling the merge files fucntion
    output_yaml = {}
    for i in range(0, len(yaml_files)):
        if i==0:
            output_yaml = yaml_files[i]
            continue
        output_yaml = merge(output_yaml, yaml_files[i])
    
    dump(output_yaml)
    

def merge (yaml1, yaml2):
    """Function that will handle the merging of two yamls"""
    # Extracting keys out from both the YAMLs
    keys1 = []
    keys2 = []
    keys_output = ['name', 'channels', 'dependencies']
    merged_yaml = {}

    for key, value in yaml1.items():
        keys1.append(key)
    for key, value in yaml2.items():
        keys2.append(key)
    
    # Making sure that the YAMLs are in proper format"""
    # TODO: add name of the YAML file that has faulty format
    if ('channels' not in keys1 or 'dependencies' not in keys1 or 'channels' not in keys2 or 'dependencies' not in keys2):
        raise MergeError ("One of the YAML files seems to be corrupted. Please make sure that it is in proper format. (Proper format must contain 'channels' and 'dependencies' keys.")

    # Resolve name of the output file's env
    # If a name does not exist in both yamls, use a generic placeholder
    outputName = yaml1.get(keys_output[0])
    if outputName is None:
        outputName = yaml2.get(keys_output[0])
        if outputName is None:
            outputName = "myenv"    # Generic placeholder
    merged_yaml[keys_output[0]] = outputName

    # Merging channels while keeping their priorities in mind
    try:
        env_definitions = [yaml1, yaml2]
        output_channels = merge_channels(env.get('channels') for env in env_definitions)
    except MergeError as exc:
        print("Falied to merge channel priorities.\n{}\n".format(exc.args[0]),
              file=sys.stderr)
        raise
    if output_channels:
        merged_yaml[keys_output[1]] = output_channels

    # Merging dependencies (including pip dependencies)
    output_dependencies = resolve_dependencies(env.get('dependencies') for env in env_definitions)

    if output_dependencies:
        merged_yaml[keys_output[2]] = output_dependencies
    return merged_yaml

def resolve_dependencies (dependencies_list):
    """Merge all dependencies to one list and return it.

    Two overlapping dependencies (e.g. package-a and package-a=1.0.0) are not
    unified, and both are left in the list (except cases of exactly the same
    dependency). Conda itself handles that very well so no need to do this ourselves.

    """
    pips = []
    merged_dependencies = []
    for dependenciess in dependencies_list:
        if dependenciess is None:  # not found in this environment definition
            continue
        for dep in dependenciess:
            if isinstance(dep, dict) and dep['pip']:
                pips.append(dep['pip'])
            elif dep not in merged_dependencies:
                merged_dependencies.append(dep)
    merged_dependencies = sorted(merged_dependencies)
    if pips:
        piplist = merge_pips(pips)
        merged_dependencies.append(piplist)
    return merged_dependencies

def merge_pips (pips):
    """Merge pip requirements lists the same way as `merge_dependencies` work"""
    return {'pip': sorted({req for reqs in pips for req in reqs})}

def merge_channels(channels_list):
    """Merge multiple channel priorities list and output a unified one.

    Use a directed-acyclic graph to create a topological sort of the priorities,
    so that the order from each environment file will be preserved in the output.
    If this cannot be satisfied, a MergeError is raised.
    If no channel priories are found (all are None), return an emply list.
    This part of code is an extract taken from https://github.com/amitbeka/conda-merge
    """
    dag = DAG()
    try:
        for channels in channels_list:
            if channels is None:  # not found in this environment definition
                continue
            for i, channel in enumerate(channels):
                dag.add_node(channel)
                if i > 0:
                    dag.add_edge(channels[i-1], channel)
        return dag.topological_sort()
    except ValueError as exc:
        raise MergeError("Can't satisfy channels priority: {}".format(exc.args[0]))

class DAG(object):
    """Directed acyclic graph for merging channel priorities.

    This is a stripped down version adopted from:
    https://github.com/thieman/py-dag (MIT license)

    """

    def __init__(self):
        self.graph = OrderedDict()

    def __len__(self):
        return len(self.graph)

    def add_node(self, node_name):
        if node_name not in self.graph:
            self.graph[node_name] = []

    def add_edge(self, from_node, to_node):
        if from_node not in self.graph or to_node not in self.graph:
            raise KeyError('one or more nodes do not exist in graph')
        if to_node not in self.graph[from_node]:
            test_graph = deepcopy(self.graph)
            test_graph[from_node].append(to_node)
            if self.validate():
                self.graph[from_node].append(to_node)
            else:
                raise ValueError("{} -> {}".format(from_node, to_node))

    @property
    def independent_nodes(self):
        """Return a list of all nodes in the graph with no dependencies."""
        dependent_nodes = set(node for dependents in self.graph.values()
                              for node in dependents)
        return [node for node in self.graph.keys()
                if node not in dependent_nodes]

    def validate(self):
        """Return whether the graph doesn't contain a cycle"""
        if len(self.independent_nodes) > 0:
            try:
                self.topological_sort()
                return True
            except ValueError:
                return False
        return False

    def topological_sort(self):
        """Return a topological ordering of the DAG.

        Raise an error if this is not possible (graph is not valid).

        """
        in_degree = {}
        for node in self.graph:
            in_degree[node] = 0

        for from_node in self.graph:
            for to_node in self.graph[from_node]:
                in_degree[to_node] += 1

        queue = deque()
        for node in in_degree:
            if in_degree[node] == 0:
                queue.appendleft(node)

        sorted_nodes = []
        while queue:
            independent_node = queue.pop()
            sorted_nodes.append(independent_node)
            for next_node in self.graph[independent_node]:
                in_degree[next_node] -= 1
                if in_degree[next_node] == 0:
                    queue.appendleft(next_node)

        if len(sorted_nodes) == len(self.graph):
            return sorted_nodes
        else:
            raise ValueError('graph is not acyclic')
    
def main():
    """Main entry point for console_scripts of setup.py"""
    try:
        merge_envs(parse_args())
    except MergeError:
        return 1

if __name__ == '__main__':
    main()
