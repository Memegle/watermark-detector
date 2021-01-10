import os
from RetinaNet import RetinaNet
from PIL import Image
import requests
from io import BytesIO
from google.colab import drive
import validators
import tensorflow as tf

class WatermarkDetectron:

    """
    Constructor of the WatermarkDetectron
    @param pretrained: The version number of a pretrained model. If none, load 
                       the latest version. Raise error if no model is found.
    """
    def __init__(self, pretrained=None):
        
        drive.mount('/content/drive', force_remount=False)

        self.model = self.__load_model(pretrained)

    """
    Load the model trained by RetinaNet.py from /data/model_saved
    @param None
    @return The model loaded
    """
    def __load_model(self, pretrained=None):

        # TODO

        return None
    
    """
    Load an image from an URL address
    @param url: URL address of the image
    @return A generator of this image 
    """
    def __read_file_from_url(self, url):
        if url.endswith('.png'):
            img_tensor = tf.image.decode_png(requests.get(url).content, channels=3, name="png_reader")
            img_tensor = tf.image.resize(img_tensor, [200, 200])
        elif url.endswith('.jpg') or url.endswith('.jpeg'):
            img_tensor = tf.image.decode_jpeg(requests.get(url).content, channels=3, name="jpeg_reader")
            img_tensor = tf.image.resize(img_tensor, [200, 200])
        else:
            img_tensor = None
        yield img_tensor

    """
    Load an image from a local path
    @param filepath: the local path of the image(s)
    @return A generator of the image(s)
    """
    def __read_file_from_local_path(self, path):
        # Consider two cases:
        # 1. The filepath refers directly to an image file.
        #    In this case, make a generator with only this image.
        # 2. The filepath refers to a folder containing images.
        #    In this case, make a generator with all the valid images
        #    in that folder (jpg, png, jpeg, etc.).
        if os.path.isdir(path):  
            img_raw = tf.io.read_file(path)
            img_tensor = tf.image.decode_image(img_raw)
            img_tensor = tf.image.resize(img_tensor, [200, 200])
            yield img_tensor
        elif os.path.isfile(path):  
            for filename in os.listdir(path):
                if filename.endswith(".jpg") or filename.endswith(".png") or filename.endswith(".jpeg"):
                    img_raw = tf.io.read_file(path)
                    img_tensor = tf.image.decode_image(img_raw)
                    img_tensor = tf.image.resize(img_tensor, [200, 200])
                    yield img_tensor
        else:  
            yield None

    
    """
    Callable method that identifies the filepath type (url or local), then
    use the helper methods to generate the expected generator.
    @param filepath: The path of the image file(s)
    @return A generator of the image(s)
    """
    def load_image(self, path):
        img_tensor = None
        if validators.url(path):
            img_tensor = self.__read_file_from_url(path)
        else:
            img_tensor = self.__read_file_from_local_path(path)
        return img_tensor
    
    """
    Use RetinaNet.predict() to predict the position of watermarks (if any),
    then transform that into binary outputs (0=no watermark, 1=has watermark).
    @param: The generator with images
    @return List of predictions (FOR NOW)
    """
    def predict(self, images):

        # TODO

        return None
    
    ### REMAINS TO DO: connecting to our db