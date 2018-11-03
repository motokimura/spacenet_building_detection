FROM nvidia/cuda:8.0-cudnn6-devel

RUN apt-get update && apt-get install -y --no-install-recommends \
        build-essential \
        cmake \
        git \
        curl \
        vim \
        wget \
        make \
        g++ \
        unzip \
        ca-certificates \
        libsm6 \
        libxext6 \
        libxrender-dev &&\
    rm -rf /var/lib/apt/lists/*

# Install libspatialindex
RUN curl -L http://download.osgeo.org/libspatialindex/spatialindex-src-1.8.5.tar.gz | tar xz && \
    cd spatialindex-src-1.8.5 && \
    ./configure && make && make install && ldconfig && \
    cd .. && rm -r spatialindex-src-1.8.5

# Setup conda environment
ENV PYTHON_VERSION=3.6
RUN curl -o ~/miniconda.sh -O https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh && \
    chmod +x ~/miniconda.sh && ~/miniconda.sh -b -p /opt/conda && rm ~/miniconda.sh && \
    /opt/conda/bin/conda create -y --name py$PYTHON_VERSION \
        python=$PYTHON_VERSION \
        numpy \
        pyyaml \
        scipy \
        ipython \
        mkl \
        matplotlib \
        scikit-learn \
        scikit-image \
        Pillow \
        jupyter \
        gdal && \
    /opt/conda/bin/conda clean -ya 

# Activate conda environment
ENV PATH /opt/conda/envs/py$PYTHON_VERSION/bin:$PATH

# Install chainer under conda environment
RUN pip install cupy==4.0.0b3 chainer==4.0.0b3

# Clone chainer repository
RUN git clone https://github.com/chainer/chainer.git /opt/chainer

# Install some additional packages ..
RUN pip install tensorflow tensorboard tensorboardX \
    geopandas==0.3.0 Rtree==0.8.3 centerline==0.3 osmnx==0.6 \
    opencv-python tqdm

# Setup jupyter
RUN jupyter notebook --generate-config && \
    ipython profile create

RUN echo "c.NotebookApp.ip = '0.0.0.0'" >> /root/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.open_browser = False" >> /root/.jupyter/jupyter_notebook_config.py && \
    echo "c.InteractiveShellApp.matplotlib = 'inline'" >> /root/.ipython/profile_default/ipython_config.py && \
    HASH=$(python3 -c "from IPython.lib import passwd; print(passwd('passw0rd'))") && \
    echo "c.NotebookApp.password = u'${HASH}'" >> /root/.jupyter/jupyter_notebook_config.py && \
    echo "c.NotebookApp.allow_root = True" >> /root/.jupyter/jupyter_notebook_config.py

# Specify matplotlib backend
WORKDIR /root/.config/matplotlib
RUN echo "backend : Agg" >> matplotlibrc

WORKDIR /workspace