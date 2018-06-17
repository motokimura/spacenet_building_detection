#!/bin/bash

# Set image name
IMAGE="spacenet_building:test"
if [ $# -eq 1 ]; then
    IMAGE=$1
fi

# Set project root dicrectory to map to docker 
THIS_DIR=$(cd $(dirname $0); pwd)
PROJ_DIR=`dirname ${THIS_DIR}`

# Make some directories if not exist
mkdir -p ${PROJ_DIR}/data ${PROJ_DIR}/models

# Run container
CONTAINER="spacenet_building"

nvidia-docker run -it --rm --ipc=host \
	-p 8888:8888 -p 6006:6006 \
	-v ${PROJ_DIR}:/workspace \
	--name ${CONTAINER} \
	${IMAGE} /bin/bash