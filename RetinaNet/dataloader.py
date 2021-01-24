from google.colab import auth
import urllib
from oauth2client.client import GoogleCredentials
import getpass
from google.colab import drive  

class RetinaNetBoxLoss: 
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


