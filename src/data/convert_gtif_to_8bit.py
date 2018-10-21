#!/usr/bin/env python
# -*- coding: utf-8 -*-

import gdal
import subprocess

def convert_gtif_to_8bit(src_raster_path, dst_raster_path):

	srcRaster = gdal.Open(src_raster_path)

	outputPixType='Byte'
	outputFormat='GTiff'

	cmd = ['gdal_translate', '-ot', outputPixType, '-of', outputFormat, '-co', '"PHOTOMETRIC=rgb"']
	
	scaleList = []
	for bandId in range(srcRaster.RasterCount):
	    bandId = bandId + 1
	    band = srcRaster.GetRasterBand(bandId)
	    min = band.GetMinimum()
	    max = band.GetMaximum()
	    
	    # if not exist minimum and maximum values
	    if min is None or max is None:
	        (min, max) = band.ComputeRasterMinMax(1)
	    
	    cmd.append('-scale_{}'.format(bandId))
	    cmd.append('{}'.format(0))
	    cmd.append('{}'.format(max))
	    cmd.append('{}'.format(0))
	    cmd.append('{}'.format(255))
	    
	cmd.append(src_raster_path)
	cmd.append(dst_raster_path)

	print(cmd)

	return subprocess.call(cmd)