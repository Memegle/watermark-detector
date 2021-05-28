import urllib.request, json 
import argparse
from os.path import exists, isdir, isfile, join, abspath
from os import mkdir

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--output_dir', default='../data/original_images')
parser.add_argument('-i', '--start_index', default='0')
args = parser.parse_args()

DOWNLOAD_FOLDER = abspath(args.output_dir)
URL = "https://memegle.live:8080/all"
TIMES_RUN = 0
START_INDEX = int(args.start_index)
success = 0

if not isdir(DOWNLOAD_FOLDER):
    print('Folder {} not found, creating...'.format(DOWNLOAD_FOLDER))
    mkdir(DOWNLOAD_FOLDER)

with urllib.request.urlopen(URL) as url:
    data = json.loads(url.read().decode())
    for i in range(START_INDEX, 200):#len(data)):
        img = data[i]
        try: 
            TIMES_RUN += 1
            img_url = img['media_url']
            filename = img['title'] + '.' + img['ext']
            path = join(DOWNLOAD_FOLDER, filename)
            urllib.request.urlretrieve(img_url, path)
            success += 1
            print("Success: " + filename)
            print("Finished Index: " + str(i))
        except Exception as e:
            print('failing at {} with error: {}'.format(img['media_url'], e))

print('successfully downloaded {} images out of {}'.format(success, TIMES_RUN-success))
