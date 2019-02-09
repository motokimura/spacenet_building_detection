#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
from tqdm import tqdm

import sys
sys.path.append("spacenet_lib")

from create_poly_mask import create_poly_mask


def build_labels(src_raster_dir, src_vector_dir, dst_dir):
	
	os.makedirs(dst_dir, exist_ok=True)

	file_count = len([f for f in os.walk(src_vector_dir).__next__()[2] if f[-8:] == ".geojson"])

	print("[INFO] Found {} geojson files. Preparing building mask images...".format(file_count))

	for idx in tqdm(range(1, file_count + 1)):

		src_raster_filename = "3band_AOI_1_RIO_img{}.tif".format(idx)
		src_vector_filename = "Geo_AOI_1_RIO_img{}.geojson".format(idx)

		src_raster_path = os.path.join(src_raster_dir, src_raster_filename)
		src_vector_path = os.path.join(src_vector_dir, src_vector_filename)
		dst_path = os.path.join(dst_dir, src_raster_filename)

		create_poly_mask(
			src_raster_path, src_vector_path, npDistFileName=dst_path, 
			noDataValue=0, burn_values=255
		)


if __name__ == "__main__":

	parser = argparse.ArgumentParser()

	parser.add_argument('src_raster_dir', help='Root directory for raster files (.tif)')
	parser.add_argument('src_vector_dir', help='Root directory for vector files (.geojson)')
	parser.add_argument('dst_dir', help='Output directory')

	args = parser.parse_args()

	build_labels(args.src_raster_dir, args.src_vector_dir, args.dst_dir)
