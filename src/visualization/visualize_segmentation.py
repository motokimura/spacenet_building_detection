#!/usr/bin/env python

import numpy as np
import cv2

def overlay_mask(image, mask, alpha=0.5, rgb=[255, 0, 0]):
	
	overlay = image.copy()
	overlay[mask] = np.array(rgb, dtype=np.uint8)

	output = image.copy()
	cv2.addWeighted(overlay, alpha, output, 1 - alpha, 0, output)

	return output