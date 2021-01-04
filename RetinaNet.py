from tools.my_dataset import MyDataset 
from torch.utils.data import DataLoader
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

### train the net below
if __name__ == "__main__":

    """
    Load data from dataset on google drive (finish train-test split in this method)
    Split into images and labels
    num_images = number of images per label (e.g. 200 positive and 200 negative)
    """
    train_data = MyDataset(data_dir=..., mode="train")
    valid_data = MyDataset(data_dir=..., mode="valid")

    train_loader = DataLoader(dataset=train_data, batch_size=...)
    valid_loader = DataLoader(dataset=valid_data, batch_size=...)

