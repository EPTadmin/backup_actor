FROM continuumio/miniconda3:latest

# create app directory
WORKDIR /actor-bu

# copy the files needed
COPY ./env.yaml .
COPY ./syncro.py .


# install rsync
RUN apt-get update && apt-get install rsync -y

# install mamba
RUN conda install -n base conda-libmamba-solver && conda config --set solver libmamba

# setup the environment
RUN conda env create -f ./env.yaml
SHELL ["conda", "run", "-n", "actor-bu", "/bin/bash", "-c"]

ENTRYPOINT python -m syncro
