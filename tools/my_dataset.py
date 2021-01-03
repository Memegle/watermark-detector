import numpy as np
import torch
import os
import random
from PIL import Image
from torch.utils.data import Dataset

class MyDataset(Dataset):
    def __init__(self, data_dir, mode="train"):

    def __getitem__(self, index):

        return img, label

    def __len__(self):

        return len