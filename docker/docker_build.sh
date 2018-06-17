#!/bin/bash

# Set image name
IMAGE="spacenet_building:test"

# Get project root dicrectory
THIS_DIR=`dirname $0`
PROJ_DIR=`dirname ${THIS_DIR}`

# Buld docker container in project root directory
cd ${PROJ_DIR} && \
nvidia-docker build -t ${IMAGE} -f ${THIS_DIR}/Dockerfile .