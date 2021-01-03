import os
import re
import zipfile

import numpy as np
import tensorflow as tf
from tensorflow import keras

import matplotlib.pyplot as plt

class RetinaNet():

    def __init__(self, dataset, num_images=200, pretrained=None):
        
        # TODO
        pass

    """
    Load data from dataset on google drive (finish train-test split in this method)
    Split into images and labels
    num_images = number of images per label (e.g. 200 positive and 200 negative)
    """
    def __load_data(self, dataset, num_images=200):

        # TODO

        return ...
    
    """
    Helper method for training
    """
    def __resize_image(self, height=200, width=200):

        # TODO

        return ...

    ### DEFINE METHODS FOR TRAINING THE NET

    """
    Report the accuracy of classification
    """
    def evaluate(self, images, labels):

        # TODO

        return ...