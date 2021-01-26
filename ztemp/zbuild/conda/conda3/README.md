Important
---------

1. Make sure that conda is available on the CLI.
2. `install_conda.sh` will try to update APT and install gcc, libhdf5 libraries.
	IF you already have these, you may comment them out.

3. `install_conda.sh` requires the name of the environment that you want to install
	into, as a parameter (see step 2 below). 

	In case, you want to rename these environments, you should follow the following.

	The argument to the shell script should be identical :
	a. to the name of the yml environment configuration file and 
	b. to the "name" parameter in the configuration file.

	For ex: when installing `env1_py36` environment, make sure that the 
	`env1_py36.yml` file exists and environment name in the `env1_py36.yml`
	file is also set to `env1_py36`.



Steps to execute
----------------

1. Make sure the steps in the above section are followed.
2. `sh install_conda.sh env1_py36`

The `install_conda.sh` will run the `test_installation.py` script
	via conda in the same environment and will start to make a bundle 
	with conda pack in the same directory, once the test executes
	without unforeseen errors.
3. If you need GPU with your installation you should run the command with 
	an extra parameter:

	`sh install_conda.sh env1_py36 enable-gpu`