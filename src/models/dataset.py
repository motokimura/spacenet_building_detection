#!/usr/bin/env python

import os
import numpy as np
import random

try:
    from PIL import Image
    available = True
except ImportError as e:
    available = False
    _import_error = e
import six

from chainer.dataset import dataset_mixin

from transforms import random_color_distort


def _check_pillow_availability():
    if not available:
        raise ImportError('PIL cannot be loaded. Install Pillow!\n'
                          'The actual import error is as follows:\n' +
                          str(_import_error))


def _read_image_as_array(path, dtype):
    f = Image.open(path)
    try:
        image = np.asarray(f, dtype=dtype)
    finally:
        # Only pillow >= 3.0 has 'close' method
        if hasattr(f, 'close'):
            f.close()
    return image


class LabeledImageDataset(dataset_mixin.DatasetMixin):
    def __init__(self, dataset, root, label_root, dtype=np.float32,
                 label_dtype=np.int32, mean=0, crop_size=256, test=False,
                 distort=False):
        _check_pillow_availability()
        if isinstance(dataset, six.string_types):
            dataset_path = dataset
            with open(dataset_path) as f:
                pairs = []
                for i, line in enumerate(f):
                    line = line.rstrip('\n')
                    image_filename = line
                    label_filename = line
                    pairs.append((image_filename, label_filename))
        self._pairs = pairs
        self._root = root
        self._label_root = label_root
        self._dtype = dtype
        self._label_dtype = label_dtype
        self._mean = mean[np.newaxis, np.newaxis, :]
        self._crop_size = crop_size
        self._test = test
        self._distort = distort

    def __len__(self):
        return len(self._pairs)

    def get_example(self, i):
        image_filename, label_filename = self._pairs[i]
        
        image_path = os.path.join(self._root, image_filename)
        image = _read_image_as_array(image_path, self._dtype)
        if self._distort:
            image = random_color_distort(image)
            image = np.asarray(image, dtype=self._dtype)

        image = (image - self._mean) / 255.0
        
        label_path = os.path.join(self._label_root, label_filename)
        label_image = _read_image_as_array(label_path, self._label_dtype)
        
        h, w, _ = image.shape
        
        label = np.zeros(shape=[h, w], dtype=np.int32) # 0: background
        label[label_image > 0] = 1 # 1: "building"
        
        # Padding
        if (h < self._crop_size) or (w < self._crop_size):
            H, W = max(h, self._crop_size), max(w, self._crop_size)
            
            pad_y1, pad_x1 = (H - h) // 2, (W - w) // 2
            pad_y2, pad_x2 = (H - h - pad_y1), (W - w - pad_x1)
            image = np.pad(image, ((pad_y1, pad_y2), (pad_x1, pad_x2), (0, 0)), 'symmetric')

            if self._test:
                # Pad with ignore_value for test set
                label = np.pad(label, ((pad_y1, pad_y2), (pad_x1, pad_x2)), 'constant', constant_values=255)
            else:
                # Pad with original label for train set  
                label = np.pad(label, ((pad_y1, pad_y2), (pad_x1, pad_x2)), 'symmetric')
            
            h, w = H, W
        
        # Randomly flip and crop the image/label for train-set
        if not self._test:

            # Horizontal flip
            if random.randint(0, 1):
                image = image[:, ::-1, :]
                label = label[:, ::-1]

            # Vertical flip
            if random.randint(0, 1):
                image = image[::-1, :, :]
                label = label[::-1, :]                
            
            # Random crop
            top  = random.randint(0, h - self._crop_size)
            left = random.randint(0, w - self._crop_size)
        
        # Crop the center for test-set
        else:
            top = (h - self._crop_size) // 2
            left = (w - self._crop_size) // 2
        
        bottom = top + self._crop_size
        right = left + self._crop_size
        
        image = image[top:bottom, left:right]
        label = label[top:bottom, left:right]
            
        return image.transpose(2, 0, 1), label
