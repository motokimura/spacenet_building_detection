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


	def __preprocess(self, image):

		h, w, _ = image.shape
		h_padded = int(math.ceil(float(h) / 16.0) * 16)
		w_padded = int(math.ceil(float(w) / 16.0) * 16)

		image_pad = np.zeros(shape=[h_padded, w_padded, 3], dtype=np.float32)
		top, left = (h_padded - h) // 2, (w_padded - w) // 2
		bottom, right = top + h, left + w
		image_pad[top:bottom, left:right, :] = image
			
		image_in = (image_pad - self.__mean) / 255.0
		image_in = image_in.transpose(2, 0, 1)
		image_in = image_in[np.newaxis, :, :, :]
	
		image_in = Variable(cuda.cupy.asarray(image_in, dtype=cuda.cupy.float32))

		return image_in, (top, left, bottom, right)
