'''
predict.py有几个注意点
1、无法进行批量预测，如果想要批量预测，可以利用os.listdir()遍历文件夹，利用Image.open打开图片文件进行预测。
2、如果想要保存，利用r_image.save("img.jpg")即可保存。
3、如果想要获得框的坐标，可以进入detect_image函数，读取top,left,bottom,right这四个值。
4、如果想要截取下目标，可以利用获取到的top,left,bottom,right这四个值在原图上利用矩阵的方式进行截取。
'''
from keras.layers import Input
from PIL import Image
import os

from retinanet import Retinanet

retinanet = Retinanet()

predictions = open("predictions.txt", 'w')
folder_path = 'predict_images/'
entries = os.listdir(folder_path)
for img in entries:
    img_path = folder_path + img
    try:
        image = Image.open(img_path)
    except:
        print('Open Error! Try again!')
        continue
    else:
        r_image, detection_output = retinanet.detect_image(image)
        #r_image.show()
        predictions.write(img + ", " + str(detection_output) + "\n")
predictions.close()
retinanet.close_session()
    