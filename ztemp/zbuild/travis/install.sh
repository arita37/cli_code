#!/bin/bash
# This script is meant to be called by the "install" step defined in
# .travis.yml. See https://docs.travis-ci.com/ for more details.
# The behavior of the script is controlled by environment variabled defined
# in the .travis.yml in the top level folder of the project.
#  https://conda.github.io/conda-pack/cli.html

set -e

echo 'List files from cached directories'
echo 'pip:'
ls $HOME/.cache/pip
ls $HOME


if [ $TRAVIS_OS_NAME = "linux" ]
then
	export CC=/usr/lib/ccache/gcc
	export CXX=/usr/lib/ccache/g++
	# Useful for debugging how ccache is used
	# export CCACHE_LOGFILE=/tmp/ccache.log
	# ~60M is used by .ccache when compiling from scratch at the time of writing
	ccache --max-size 2000M --show-stats
fi




make_conda() {
	TO_INSTALL="$@"
    # Deactivate the travis-provided virtual environment and setup a
    # conda-based environment instead
    # If Travvis has language=generic, deactivate does not exist. `|| :` will pass.
    deactivate || :


    # Install conda
    # wget https://repo.continuum.io/archive/Anaconda3-5.2.0-Linux-x86_64.sh \
    #    -O miniconda.sh

    #MINICONDA_PATH=$HOME/miniconda
    #chmod +x miniconda.sh && ./miniconda.sh -b -p $MINICONDA_PATH
    #export PATH=$MINICONDA_PATH/bin:$PATH
    #conda update --yes conda
    #source activate base

    #pip install arrow==0.10.0 attrdict==2.0.0 backports.shutil-get-terminal-size==1.0.0 configmy==0.14.87 github3.py==1.2.0 jwcrypto==0.6.0 kmodes==0.9 rope-py3k==0.9.4.post1 tables==3.3.0 tabulate==0.8.2 uritemplate==3.0.0
    #pip install pytest toml


    # Install miniconda
    #if [ $TRAVIS_OS_NAME = "osx" ]
	# then
	#	fname=Miniconda3-latest-MacOSX-x86_64.sh
	# else
	# 	fname=Miniconda3-latest-Linux-x86_64.sh
	#fi
    #wget https://repo.continuum.io/miniconda/$fname \
    #    -O miniconda.sh
    #MINICONDA_PATH=$HOME/miniconda

    # chmod +x miniconda.sh && ./miniconda.sh -b -p $MINICONDA_PATH
    # export PATH=$MINICONDA_PATH/bin:$PATH
    # conda update --yes conda


    #### Test env install
    if test -e $HOME/miniconda/bin; then
      echo "Conda already isntalled"
      ls  $HOME/miniconda/bin
      export PATH=$HOME/miniconda/bin:$PATH
      conda update --yes conda
      source activate testenv

    else
      echo  "Install testenv"
      chmod +x $HOME/download/miniconda.sh
      $HOME/download/miniconda.sh -b -p $HOME/miniconda;

      export PATH=$HOME/miniconda/bin:$PATH
      conda update --yes conda

      conda create -n testenv --yes $TO_INSTALL --file zbuild/py36.txt
      source activate testenv
      pip install arrow==0.10.0 attrdict==2.0.0 backports.shutil-get-terminal-size==1.0.0 configmy==0.14.87 github3.py==1.2.0 jwcrypto==0.6.0 kmodes==0.9 rope-py3k==0.9.4.post1 tables==3.3.0 tabulate==0.8.2 uritemplate==3.0.0
      pip install pytest==4.3.0
      pip install toml

    fi;


    python --version
    python -c "import numpy; print('numpy %s' % numpy.__version__)"
    conda list
    pwd

    export BOTO_CONFIG=/dev/null
}

TO_INSTALL="python=$PYTHON_VERSION pip pytest pytest-cov \
            numpy=$NUMPY_VERSION scipy=$SCIPY_VERSION \
            cython=$CYTHON_VERSION"

if [[ "$INSTALL_MKL" == "true" ]]; then
    TO_INSTALL="$TO_INSTALL mkl"
else
    TO_INSTALL="$TO_INSTALL nomkl"
fi

if [[ -n "$PANDAS_VERSION" ]]; then
    TO_INSTALL="$TO_INSTALL pandas=$PANDAS_VERSION"
fi

if [[ -n "$PYAMG_VERSION" ]]; then
    TO_INSTALL="$TO_INSTALL pyamg=$PYAMG_VERSION"
fi

if [[ -n "$PILLOW_VERSION" ]]; then
    TO_INSTALL="$TO_INSTALL pillow=$PILLOW_VERSION"
fi

if [[ -n "$JOBLIB_VERSION" ]]; then
    TO_INSTALL="$TO_INSTALL joblib=$JOBLIB_VERSION"
fi
    make_conda $TO_INSTALL


if [[ "$COVERAGE" == "true" ]]; then
    pip install coverage codecov
fi

if [[ "$TEST_DOCSTRINGS" == "true" ]]; then
    pip install sphinx numpydoc  # numpydoc requires sphinx
fi

# Build scikit-learn in the install.sh script to collapse the verbose
# build output in the travis output when it succeeds.
python --version
python -c "import numpy; print('numpy %s' % numpy.__version__)"
python -c "import scipy; print('scipy %s' % scipy.__version__)"
python -c "\
try:
    import pandas
    print('pandas %s' % pandas.__version__)
except ImportError:
    pass
"
