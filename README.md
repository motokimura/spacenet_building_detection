# SpaceNet Building Detection

This repository privides some python scripts and jupyter notebooks to train and evaluate convolutional neural networks 
which extracts buildings from [SpaceNet](https://spacenetchallenge.github.io/) satellite images. 

## Dependency

* [NVIDIA Driver](https://www.nvidia.com/Download/index.aspx)
* [NVIDIA Docker](https://github.com/NVIDIA/nvidia-docker)
* [AWS CLI](https://docs.aws.amazon.com/streams/latest/dev/kinesis-tutorial-cli-installation.html)

## Usage

### 0. Clone this repo

```
$ PROJ_DIR=~/spacenet_building_detection  # assuming you clone this repo to your home directory

$ git clone --recursive https://github.com/motokimura/spacenet_building_detection.git $PROJ_DIR
```

### 1. Download SpaceNet dataset

Download satellite image and ground-truth building footprint data (of SpaceNet AOI-1 Rio). 
Assuming you already configured [AWS CLI](https://docs.aws.amazon.com/streams/latest/dev/kinesis-tutorial-cli-installation.html) 
to download the data from AWS S3.

```
$ cd $PROJ_DIR/data

# Download processed 200mx200m tiles of AOI 1 (3.4 GB) with associated building footprints
$ aws s3api get-object --bucket spacenet-dataset --key AOI_1_Rio/processedData/processedBuildingLabels.tar.gz --request-payer requester processedBuildingLabels.tar.gz

$ tar -xvf processedBuildingLabels.tar.gz
$ cd processedBuildingLabels
$ tar -xvf 3band.tar.gz

$ cd vectordata 
$ tar geojson.tar.gz

# Download the Source Imagery Mosaic (3-band = 2.3 GB and 8-band = 6.5 GB)
$ cd $PROJ_DIR/data
$ aws s3api get-object --bucket spacenet-dataset --key AOI_1_Rio/srcData/rasterData/3-Band.tar.gz --request-payer requester 3-Band.tar.gz
$ tar -xvf 3-Band.tar.gz
```

You can find more details [here](https://spacenetchallenge.github.io/AOI_Lists/AOI_1_Rio.html).

### 2. Build Docker image

Build docker image to setup the environment to preprocess SpaceNet dataset, train and evaluate the convolutional neural networks. 

```
$ cd $PROJ_DIR/docker
$ bash build.sh
```

Even though you can use this repo without docker, I strongly reccomend you to use it because you may have some troubles to install some geo-spatial data processing libraries. In case you don't want to use docker, you have  to install additional dependencies described in `docker/Dockerfile`.

### 3. Train U-Net

### 4. Evaluate U-Net

## License

[MIT License](LICENSE)

## References
