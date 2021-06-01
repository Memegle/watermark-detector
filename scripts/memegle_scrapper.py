import urllib.request, json 
import argparse
from os.path import exists, isdir, isfile, join, abspath
from os import mkdir
import random

parser = argparse.ArgumentParser()
parser.add_argument('-o', '--output_dir', default='../data/original_images')
parser.add_argument('-i', '--start_index', default='0')
parser.add_argument('-n', '--num_pics', default='0')
parser.add_argument('-r', '--random_pics', action='store_true')
args = parser.parse_args()

DOWNLOAD_FOLDER = abspath(args.output_dir)
URL = "https://memegle.live:8080/all"
TIMES_RUN = 0
START_INDEX = int(args.start_index)
NUM_PICS = int(args.num_pics)
RANDOM = args.random_pics
success = 0

def download_img(data, ind):
    global TIMES_RUN
    global success
    img = data[ind]
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

if not isdir(DOWNLOAD_FOLDER):
    print('Folder {} not found, creating...'.format(DOWNLOAD_FOLDER))
    mkdir(DOWNLOAD_FOLDER)

with urllib.request.urlopen(URL) as url:
    data = json.loads(url.read().decode())
    if (NUM_PICS != 0) and RANDOM:
        randNums = set()
        while (len(randNums) < NUM_PICS):
            randNums.add(random.randint(0, len(data)))
        for i in randNums:
            download_img(data, i)
    elif (NUM_PICS != 0):
        for i in range(START_INDEX, START_INDEX+NUM_PICS):
            download_img(data, i)
    else:        
        for i in range(START_INDEX, len(data)):
            download_img(data, i)

print('successfully downloaded {} images out of {}'.format(success, TIMES_RUN-success))
