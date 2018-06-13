#!/bin/bash

if [ $# -ne 3 ]; then
    echo "bash docker_run.sh PROJ_DIR DATA_DIR IMAGE"
    exit 1
fi

PROJ_DIR=$1
DATA_DIR=$2
IMAGE=$3

nvidia-docker run -it --rm --ipc=host \
	-p 8888:8888 -p 6006:6006 \
	-v ${PROJ_DIR}:/workspace -v ${DATA_DIR}:/workspace/data ${IMAGE} \
	/bin/bash