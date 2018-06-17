#!/usr/bin/env python
# -*- coding: utf-8 -*-

import argparse
import os
import random
from tqdm import tqdm


def dump_filenames(filenames, dst_path):

	with open(dst_path, 'w') as f:
		
		for i, filename in enumerate(filenames):
			if i != 0:
				f.write("\n")

			f.write(filename)


def split_dataset(img_dir, dst_dir, ratio, seed=0):
	
	filenames = os.listdir(img_dir)

	random.seed(seed)
	random.shuffle(filenames)

	file_count = len(filenames)

	train_ratio, val_ratio, test_ratio = ratio
	total = train_ratio + val_ratio + test_ratio

	train_count= int(float(file_count * train_ratio) / float(total))
	val_count = int(float(file_count * val_ratio) / float(total))

	train_files = filenames[:train_count]
	val_files = filenames[train_count:train_count + val_count]
	test_files = filenames[train_count + val_count:]

	dump_filenames(train_files, os.path.join(dst_dir, "train.txt"))
	dump_filenames(val_files, os.path.join(dst_dir, "val.txt"))
	dump_filenames(test_files, os.path.join(dst_dir, "test.txt"))


if __name__ == "__main__":

	parser = argparse.ArgumentParser()

	parser.add_argument('img_dir', help='Root directory for building mask images (.tif)')
	parser.add_argument('dst_dir', help='Root directory to output train.txt, val.txt, and test.txt')
	parser.add_argument('--ratio', help='Split ratio for train/val/test set',
						type=int, nargs=3, default=[7, 1, 2])
	parser.add_argument('--seed', help='random seed',
						type=int, default=0)

	args = parser.parse_args()

	split_dataset(args.img_dir, args.dst_dir, args.ratio, args.seed)
