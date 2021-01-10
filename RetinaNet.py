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

        return None
    
    """
    Helper method for training
    """
    def __resize_image(self, img_path, width=200, height=200):
        img = Image.open(img_path)
        old_width, old_height = img.size
        w_ratio = float(width)/old_width
        h_ratio = float(height)/old_height
        ratio = min(w_ratio, h_ratio)
        new_size = (int(ratio*old_width), int(ratio*old_height))
        img = img.resize(new_size, Image.ANTIALIAS)
        new_img = Image.new("RGB", (width, height))
        new_img.paste(img, ((width-new_size[0])//2, (height-new_size[1])//2))
        return new_img

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

