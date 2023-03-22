FROM nvidia/cuda:10.2-base

RUN rm /etc/apt/sources.list.d/cuda.list
RUN rm /etc/apt/sources.list.d/nvidia-ml.list

RUN apt-get update && apt-get install -y build-essential && apt-get install -y wget && apt-get clean && rm -rf /var/lib/apt/lists/*

RUN apt-get update

RUN apt-get -y install curl gnupg

ENV CONDA_DIR /opt/conda

# Install miniconda
RUN wget --quiet https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh -O ~/miniconda.sh && /bin/bash ~/miniconda.sh -b -p /opt/conda

# Put conda in path so we can use conda activate
ENV PATH=$CONDA_DIR/bin:$PATH

RUN conda init

#install nodejs
RUN curl -sL https://deb.nodesource.com/setup_14.x  | bash -
RUN apt-get -y install nodejs

#create conda env
COPY environment.yml ./
RUN conda env create -f environment.yml

COPY tool_methods.py ./
COPY main.py ./

SHELL ["conda", "run", "-n", "tool", "/bin/bash", "-c"]
ENTRYPOINT ["conda", "run", "--no-capture-output", "-n", "tool", "python", "main.py"]