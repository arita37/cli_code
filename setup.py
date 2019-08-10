
"""
Pypi Uploader
Usage:
First of all, you need to copy the script to /usr/bin directory and mark it as an executable, like so:

$ ~ sudo cp script.py /usr/bin/NAMEYOUWANT
$ ~ sudo chmod +x /usr/bin/NAMEYOUWANT

And then to upload PyPI, you need to create a file called .pypirc that has to contain login credentials.


$ ~ YOURTEXTEDITOR ~/.pypirc
Open a file and paste this to in it:

[pypi]
username = token
password = pypi-AgEI


"""



import io
import os
import subprocess
import sys
from setuptools import setup, find_packages

######################################################################################
root = os.path.abspath(os.path.dirname(__file__))



##### check if GPU available  #######################################################
p = subprocess.Popen(['command -v nvidia-smi'], stdout=subprocess.PIPE, shell=True)
out = p.communicate()[0].decode('utf8')
gpu_available = len(out) > 0



##### Version
version ='6.1.0'
""""
with io.open(os.path.join(root, 'nlp_architect', 'version.py'), encoding='utf8') as f:
    version_f = {}
    exec(f.read(), version_f)
    version = version_f['NLP_ARCHITECT_VERSION']
"""


with open("README.md", "r") as fh:
    long_description = fh.read()


### Packages  ####################################################
packages = ["cli_code"] + ["cli_code." + p for p in find_packages("cli_code")]


### CLI Scripts
scripts = [
    "cli_code/cli_module_autoinstall.py",  #
    "cli_code/cli_module_analysis.py",  #
    "cli_code/cli_convert_ipny.py",  #  ipny to py scrips
]





setup(
    name="cli_code",
    version=version,
    description="Tools for Python Doc Generation, Tool analysis, Package Auto Install, Converter",
    author="arita37",
    url="https://github.com/arita37/cli_code",
    install_requires=["numpy"],
    packages=packages,
    scripts=scripts,
)


################################################################################
################################################################################
"""


https://packaging.python.org/tutorials/packaging-projects/


import io
import os
import subprocess
import sys

from setuptools import setup, find_packages

root = os.path.abspath(os.path.dirname(__file__))


# required packages for NLP Architect
with open('requirements.txt') as fp:
    install_requirements = fp.readlines()

# check if GPU available
p = subprocess.Popen(['command -v nvidia-smi'], stdout=subprocess.PIPE, shell=True)
out = p.communicate()[0].decode('utf8')
gpu_available = len(out) > 0

# Tensorflow version (make sure CPU/MKL/GPU versions exist before changing)
for r in install_requirements:
    if r.startswith('tensorflow=='):
        tf_version = r.split('==')[1]

# default TF is CPU
chosen_tf = 'tensorflow=={}'.format(tf_version)
# check system is linux for MKL/GPU backends
if 'linux' in sys.platform:
    system_type = 'linux'
    tf_be = os.getenv('NLP_ARCHITECT_BE', False)
    if tf_be and 'mkl' == tf_be.lower():
        chosen_tf = 'intel-tensorflow=={}'.format(tf_version)
    elif tf_be and 'gpu' == tf_be.lower() and gpu_available:
        chosen_tf = 'tensorflow-gpu=={}'.format(tf_version)

for r in install_requirements:
    if r.startswith('tensorflow=='):
        install_requirements[install_requirements.index(r)] = chosen_tf

with open('README.md', encoding='utf8') as fp:
    long_desc = fp.read()

with io.open(os.path.join(root, 'nlp_architect', 'version.py'), encoding='utf8') as f:
    version_f = {}
    exec(f.read(), version_f)
    version = version_f['NLP_ARCHITECT_VERSION']

setup(name='nlp-architect',
      version=version,
      description='Intel AI Lab\'s open-source NLP and NLU research library',
      long_description=long_desc,
      long_description_content_type='text/markdown',
      keywords='NLP NLU deep learning natural language processing tensorflow keras dynet',
      author='Intel AI Lab',
      author_email=
      license='Apache 2.0',
      python_requires='>=3.6.*',
      packages=find_packages(exclude=['tests.*', 'tests', '*.tests', '*.tests.*',
                                      'examples.*', 'examples', '*.examples', '*.examples.*']),
      install_requires=install_requirements,
      scripts=['nlp_architect/nlp_architect'],
      include_package_data=True,
      classifiers=[
          'Development Status :: 3 - Alpha',
          'Intended Audience :: End Users/Desktop',
          'Intended Audience :: Developers',
          'Intended Audience :: Science/Research',
          'License :: OSI Approved :: Apache Software License',
          'Programming Language :: Python :: 3',
          'Programming Language :: Python :: 3.6',
          'Topic :: Scientific/Engineering',
          'Topic :: Scientific/Engineering :: ' +
          'Artificial Intelligence',
          'Topic :: Software Development :: Libraries',
          'Topic :: Software Development :: Libraries :: ' +
          'Python Modules',
          'Topic :: Scientific/Engineering :: Information Analysis',
          'Environment :: Console',
          'Environment :: Web Environment',
          'Operating System :: POSIX',
          'Operating System :: MacOS :: MacOS X',
      ]
      )



import os
from io import open

from setuptools import find_packages, setup

packages = ['elfi'] + ['elfi.' + p for p in find_packages('elfi')]

# include C++ examples
package_data = {'elfi.examples': ['cpp/Makefile', 'cpp/*.txt', 'cpp/*.cpp']}

with open('requirements.txt', 'r') as f:
    requirements = f.read().splitlines()

optionals = {'doc': ['Sphinx'], 'graphviz': ['graphviz>=0.7.1']}

# read version number
__version__ = open('elfi/__init__.py').readlines()[-1].split(' ')[-1].strip().strip("'\"")

setup(
    name='elfi',
    keywords='abc likelihood-free statistics',
    packages=packages,
    package_data=package_data,
    version=__version__,
    author='ELFI authors',
    author_email='elfi-support@hiit.fi',
    url='http://elfi.readthedocs.io',
    install_requires=requirements,
    extras_require=optionals,
    description='ELFI - Engine for Likelihood-free Inference',
    long_description=(open('docs/description.rst').read()),
    license='BSD',
    classifiers=[
        'Programming Language :: Python :: 3.5', 'Topic :: Scientific/Engineering',
        'Topic :: Scientific/Engineering :: Artificial Intelligence',
        'Topic :: Scientific/Engineering :: Bio-Informatics',
        'Topic :: Scientific/Engineering :: Mathematics', 'Operating System :: OS Independent',
        'Development Status :: 4 - Beta', 'Intended Audience :: Science/Research',
        'License :: OSI Approved :: BSD License'
    ],
    zip_safe=False)



"""
