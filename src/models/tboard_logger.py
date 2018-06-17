#!/usr/bin/env python

from chainer.training import extension
from chainer import Variable
import cupy

class TensorboardLogger(extension.Extension):

    def __init__(self, logger, entries=None):
        
        self._entries = entries
        self._logger = logger
        
        return

    def __call__(self, trainer):

        observation = trainer.observation
        for k, v in observation.items():
            if (self._entries is not None) and (k not in self._entries):
                continue
            
            if isinstance(v, cupy.core.core.ndarray):
                v = Variable(v)
            
            self._logger.add_scalar(k, v, trainer.updater.iteration)

        return
