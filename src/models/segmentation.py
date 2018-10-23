#!/usr/bin/env python

import numpy as np
import cv2
import math

import chainer
import chainer.functions as F
from chainer import cuda, serializers, Variable

from unet import UNet


class SegmentationModel:

	def __init__(self, model_path, mean, gpu=0):

		# Load model
		self.__model = UNet()
		serializers.load_npz(model_path, self.__model)

		chainer.cuda.get_device(gpu).use()
		self.__model.to_gpu(gpu)

		# Add height and width dimensions to mean 
		self.__mean = mean[np.newaxis, np.newaxis, :]


	def apply_segmentation(self, image):

		image_in, crop = self.__preprocess(image)

		with chainer.using_config('train', False):
			score = self.__model.forward(image_in)
		
		score = F.softmax(score)
		score = cuda.to_cpu(score.data)[0]
		
		top, left, bottom, right = crop
		score = score[:, top:bottom, left:right]
		
		return score


	def apply_segmentation_to_mosaic(self, mosaic, grid_px=800, tile_overlap_px=200):

		h, w, _ = mosaic.shape

		assert ((grid_px + tile_overlap_px * 2) % 16 == 0), "(grid_px + tile_overlap_px * 2) must be divisible by 16"

		pad_y1 = tile_overlap_px
		pad_x1 = tile_overlap_px

		n_y = int(float(h) / float(grid_px))
		n_x = int(float(w) / float(grid_px))
		pad_y2 = n_y * grid_px + 2 * tile_overlap_px - h - pad_y1
		pad_x2 = n_x * grid_px + 2 * tile_overlap_px - h - pad_x1

		mosaic_padded = np.pad(mosaic, ((pad_y1, pad_y2), (pad_x1, pad_x2), (0, 0)), 'symmetric')

		H, W, _ = mosaic_padded.shape
		score_padded = np.zeros(shape=[self.__model.class_num, H, W], dtype=np.float32)

		for yi in range(n_y):
		    for xi in range(n_x):
		        
		        top = yi * grid_px
		        left = xi * grid_px
		        bottom = top + grid_px + 2 * tile_overlap_px
		        right = left + grid_px + 2 * tile_overlap_px
		        
		        tile = mosaic_padded[top:bottom, left:right]
		        
		        score_tile = self.apply_segmentation(tile)
		        
		        score_padded[:, top:bottom, left:right] = score_tile

		score = score_padded[:, pad_y1:-pad_y2, pad_x1:-pad_x2]

		return score


	def __preprocess(self, image):

		h, w, _ = image.shape
		h_padded = int(math.ceil(float(h) / 16.0) * 16)
		w_padded = int(math.ceil(float(w) / 16.0) * 16)

		pad_y1 = (h_padded - h) // 2
		pad_x1 = (w_padded - w) // 2
		pad_y2 = h_padded - h - pad_y1
		pad_x2 = w_padded - w - pad_x1

		image_padded = np.pad(image, ((pad_y1, pad_y2), (pad_x1, pad_x2), (0, 0)), 'symmetric')
		image_in = (image_padded - self.__mean) / 255.0
		image_in = image_in.transpose(2, 0, 1)
		image_in = image_in[np.newaxis, :, :, :]
		image_in = Variable(cuda.cupy.asarray(image_in, dtype=cuda.cupy.float32))

		top, left = pad_y1, pad_x1
		bottom, right = top + h, left + w

		return image_in, (top, left, bottom, right)
