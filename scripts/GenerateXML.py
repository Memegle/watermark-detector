import xml.etree.ElementTree as gfg
import os
import numpy as np
from PIL import Image

def false_image_loader():
    for f in os.listdir("temp_input_images/original_images/train"):
        file_name = f[:-4]
        im = Image.open("temp_input_images/original_images/train/{}".format(f))
        width, height = im.size
        segmented = 0
        generate_XML(file_name, width, height, segmented)
        im.save("retinanet_keras/VOCdevkit/VOC2007/JPEGImages/{}.jpg".format(file_name))

def true_image_loader():
    for f in os.listdir("temp_input_images/watermarked_images/train"):
        if f[-4:] =='.txt':
            continue
        file_name = f[:-4]
        im = Image.open("temp_input_images/watermarked_images/train/{}".format(f))
        width, height = im.size
        segmented = 1
        bbx = np.loadtxt("temp_input_images/watermarked_images/train/{}.txt".format(file_name))
        x_min = int(np.floor(bbx[2] * width))
        y_min = int(np.floor(bbx[3] * height))
        x_max = int(np.ceil(bbx[4] * width))
        y_max = int(np.ceil(bbx[5] * height))
        generate_XML(file_name, width, height, segmented, x_min, y_min, x_max, y_max)
        im = im.convert("RGB")
        im.save("retinanet_keras/VOCdevkit/VOC2007/JPEGImages/{}.jpg".format(file_name))

def generate_XML(file_name, width, height, segmented, x_min=None, y_min=None, x_max=None, y_max=None):

    root = gfg.Element("annotation") 
    
    fd = gfg.SubElement(root, "folder")
    fd.text = "folder"

    fn = gfg.SubElement(root, "filename")
    fn.text = "{}.jpg".format(file_name)

    sc = gfg.SubElement(root, "source")
    sc.text = "Large_Scale_Watermark_Dataset"

    size = gfg.Element("size")
    root.append(size)

    wd = gfg.SubElement(size, "width")
    wd.text = str(width)

    ht = gfg.SubElement(size, "height")
    ht.text = str(height)

    dp = gfg.SubElement(size, "depth")
    dp.text = str(3)

    seg = gfg.SubElement(root, "segmented")
    seg.text = str(segmented)

    if segmented:
        obj = gfg.Element("object")
        root.append(obj)
        nm = gfg.SubElement(obj, "name")
        nm.text = "watermark"
        ps = gfg.SubElement(obj, "pose")
        ps.text = "Frontal"
        tc = gfg.SubElement(obj, "truncated")
        tc.text = str(0)
        df = gfg.SubElement(obj, "difficult")
        df.text = str(0)
        bbx = gfg.Element("bndbox")
        obj.append(bbx)
        xmin = gfg.SubElement(bbx, "xmin")
        xmin.text = str(x_min)
        ymin = gfg.SubElement(bbx, "ymin")
        ymin.text = str(y_min)
        xmax = gfg.SubElement(bbx, "xmax")
        xmax.text = str(x_max)
        ymax = gfg.SubElement(bbx, "ymax")
        ymax.text = str(y_max)
        
    tree = gfg.ElementTree(root) 
    
    with open ("retinanet_keras/VOCdevkit/VOC2007/Annotations/{}.xml".format(file_name), "wb") as f:
        tree.write(f)
  
# Driver Code 
if __name__ == "__main__":
    false_image_loader()
    true_image_loader()