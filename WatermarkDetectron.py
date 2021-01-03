import os
from RetinaNet import RetinaNet

class WatermarkDetectron:

    """
    Constructor of the WatermarkDetectron
    @param pretrained: The version number of a pretrained model. If none, load 
                       the latest version. Raise error if no model is found.
    """
    def __init__(self, pretrained=None):
        
        # TODO

        self.model = self.__load_model(pretrained)

    """
    Load the model trained by RetinaNet.py from /data/model_saved
    @param None
    @return The model loaded
    """
    def __load_model(self, pretrained=None):

        # TODO

        return ...
    
    """
    Load an image from an URL address
    @param url: URL address of the image
    @return A generator of this image 
    """
    def __read_file_from_url(self, url):

        # TODO
        
        return ...

    """
    Load an image from a local path
    @param filepath: the local path of the image(s)
    @return A generator of the image(s)
    """
    def __read_file_from_local_path(self, filepath):
        # Consider two cases:
        # 1. The filepath refers directly to an image file.
        #    In this case, make a generator with only this image.
        # 2. The filepath refers to a folder containing images.
        #    In this case, make a generator with all the valid images
        #    in that folder (jpg, png, jpeg, etc.).
        
        # TODO

        return ...

    
    """
    Callable method that identifies the filepath type (url or local), then
    use the helper methods to generate the expected generator.
    @param filepath: The path of the image file(s)
    @return A generator of the image(s)
    """
    def load_image(self, filepath):
        
        # TODO

        return ...
    
    """
    Use RetinaNet.predict() to predict the position of watermarks (if any),
    then transform that into binary outputs (0=no watermark, 1=has watermark).
    @param: The generator with images
    @return List of predictions (FOR NOW)
    """
    def predict(self, images):

        # TODO

        return ...
    
    ### REMAINS TO DO: connecting to our db