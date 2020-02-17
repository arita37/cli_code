# Merge-Conda-YAML

This is a very simple piece of script that allows user to merge multiple YAML files generated anaconda into a single unified YAML.
The output of this script is on console. It outputs the content of two files, one is the merged YAML file while the other is the requirements.txt file ready to be read by pip.

## Usage

Using this script is very simple. Just call the package using "merge-conda-yaml" and specify the paths to all the yaml files you need to merge.

## Example

-> merge-conda-yaml ./file1.yml ./file2.yml ./file3.yml