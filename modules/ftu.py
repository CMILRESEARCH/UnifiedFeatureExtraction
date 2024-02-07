import os
from abc import ABC, abstractmethod, ABCMeta

class FTU(ABC):

    __metaclass__ = ABCMeta

    @abstractmethod
    def add_feature(self, feature, value):
        """
        self.features[feature] = value
        """

    @abstractmethod
    def add_segmentation(self, layer, value):
        """
        self.segmentation[layer] = value
        """

class Tubule(FTU):
    def __init__(self, config, patch, mask):
        self.features = {}
        self.patch = patch
        self.mask = mask
        self.segmentation = {}

    def add_feature(self, feature, value):
        self.features[feature] = value
        
    def add_segmentation(self, layer, value):
        self.segmentation[layer] = value
        
    def get_segmentation(self, layer):
        return self.segmentation[layer]

    def __str__(self):
        return ', '.join(self.features)
    
    def splitIm(self, im):
        if len(im.shape)==3:
            _, w, _ = im.shape
            patch = im[:, :w//2, :]
            mask = im[:, w//2:, :]
        else:
            _, w = im.shape
            patch = im[:, :w//2]
            mask = im[:, w//2:]
        return patch, mask