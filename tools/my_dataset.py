import numpy as np
import keras

class DataGenerator(keras.utils.Sequence):
    'Generates data for Keras'
    def __init__(self, list_IDs, labels, batch_size=32, dim=(32,32,32), n_channels=1,
                 n_classes=10, shuffle=True):
        'Initialization'

    def __len__(self):
        'Denotes the number of batches per epoch'
        return len

    def __getitem__(self, index):
        'Generate one batch of data

        return img, label
## reference: https://stanford.edu/~shervine/blog/keras-how-to-generate-data-on-the-fly