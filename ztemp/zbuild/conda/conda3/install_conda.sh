#!/bin/bash
printf "\n\nInstalling gcc, libhdf5\n\n"
export HDF5_DIR=/usr/lib/x86_64-linux-gnu

sudo apt-get update
sudo apt-get install gcc libhdf5-serial-dev hdf5-tools libhdf5-dev
sudo ln -sf /usr/lib/x86_64-linux-gnu/libhdf5_serial_hl.so.10 /usr/lib/x86_64-linux-gnu/libhdf5.so
sudo ln -sf /usr/lib/x86_64-linux-gnu/libhdf5_serial_hl.so.10.0.2 /usr/lib/x86_64-linux-gnu/libhdf5_hl.so

if [ $2 = "enable-gpu" ]; then
	sudo add-apt-repository ppa:graphics-drivers/ppa
	sudo apt-key adv --fetch-keys  http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64/7fa2af80.pub
	sudo bash -c 'echo "deb http://developer.download.nvidia.com/compute/cuda/repos/ubuntu1604/x86_64 /" > /etc/apt/sources.list.d/cuda.list'
	sudo bash -c 'echo "deb http://developer.download.nvidia.com/compute/machine-learning/repos/ubuntu1604/x86_64 /" > /etc/apt/sources.list.d/cuda_learn.list'
	sudo apt update
	sudo apt install cuda-10-0
	sudo apt install libcudnn7

	# set PATH for cuda 10.0 installation
	if [ -d "/usr/local/cuda-10.0/bin/" ]; then
	    export PATH=/usr/local/cuda-10.0/bin${PATH:+:${PATH}}
	    export LD_LIBRARY_PATH=/usr/local/cuda-10.0/lib64${LD_LIBRARY_PATH:+:${LD_LIBRARY_PATH}}
	fi
else
  printf "\n\n No GPU installation"
fi

printf "\n\nInstalling $1.yml\n\n"
conda env create -f $1.yml
printf "\n\nInstalling conda pack\n\n"
conda install -c conda-forge conda-pack
conda run -n $1 python test_installation.py
RESULT=$?
if [ $RESULT -eq 0 ]; then
	printf "\n\nTests are successful\n\n"
	printf "\n\nPackaging the environment\n\n"
	conda pack -n $1
else
	printf "\n\nTests failed"
fi
