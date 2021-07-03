FROM openjdk:8

MAINTAINER Kevin <nono>

RUN update-ca-certificates -f \
  && apt-get update \
  && apt-get upgrade -y \
  && apt-get install -y \
    software-properties-common \
    wget \
    git \
    libatlas3-base \
    libopenblas-base \
    libatlas-base-dev \
    build-essential \
  && apt-get clean


# Miniconda
ENV CONDA_DIR=/opt/miniconda
ENV PATH=$CONDA_DIR/bin:$PATH

RUN wget https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh -O miniconda.sh && \
    chmod a+x miniconda.sh && \
    ./miniconda.sh -b -p $CONDA_DIR && \
    rm ./miniconda.sh && \
    conda install python=3.6

WORKDIR /app/

#RUN pip install --upgrade pip \

#RUN conda  install -c conda-forge -y  pyspark==2.4.6 \
#    ua-parser==0.10.0  \

RUN pip  install -r requirements.txt


CMD /bin/bash