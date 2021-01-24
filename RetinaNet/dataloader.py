from google.colab import auth
import urllib
from oauth2client.client import GoogleCredentials
import getpass
from google.colab import drive  

class Dataloader: 
    def loaddata_colab(url, mydrive): 
        """
        arguments: 
            url should be in the format of: /content/drive
            mydrive usually called 'My Drive'

        """
        # Load the Drive helper and mount

        # This will prompt for authorization.
        drive.mount(url)
        !ls "url + '/' + mydrive"  

    def loaddata_local(): 
        ## the commented code needs to run in the terminal
        
        ## !apt-get install -y -qq software-properties-common python-software-properties module-init-tools
        ## !add-apt-repository -y ppa:alessandro-strada/ppa 2>&1 > /dev/null
        ## !apt-get update -qq 2>&1 > /dev/null
        ## !apt-get -y install -qq google-drive-ocamlfuse fuse
        auth.authenticate_user()
        creds = GoogleCredentials.get_application_default()

        ## the next two commented code needs verification code provided by URL to fill in
        ##!google-drive-ocamlfuse -headless -id={creds.client_id} -secret={creds.client_secret} < /dev/null 2>&1 | grep URL
        vcode = getpass.getpass()
        ##!echo {vcode} | google-drive-ocamlfuse -headless -id={creds.client_id} -secret={creds.client_secret}

        ## check if the files has been created
        print('Files in Drive:')
        ##!ls drive/      

'''
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
'''


