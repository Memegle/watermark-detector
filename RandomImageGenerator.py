import os
import xml.etree.ElementTree as ET
import pickle
from os import listdir, getcwd
from os.path import join
import shutil


from PIL import Image, ImageDraw, ImageFont
from random import randint, random, sample
from tqdm import tqdm

#xml to txt
""" classes1 = ['person'] #想要筛选出来的类别
    #voc格式的xml标签文件夹路径
    xml_files1 = r'/userhome/coco128/annotations'
    #转化为yolo格式的txt标签文件夹存储路径
    save_txt_files1 = r'/userhome/coco_person/labels/train2017-t'
    #原始图片输入的文件夹路径
    imgs_in = r'/userhome/coco128/images/train2017'
    #输出满足要求图片的文件夹路径
    imgs_out = r'/userhome/coco_person/images/train2017-t'
    
    convert_annotation(xml_files1, save_txt_files1, imgs_in, imgs_out,classes1) #进行转换"""
def convert(size, box):

    x_center = (box[0]+box[1])/2.0
    y_center = (box[2]+box[3])/2.0
    x = x_center / size[0]
    y = y_center / size[1]

    w = (box[1] - box[0]) / size[0]
    h = (box[3] - box[2]) / size[1]
    
    return (x,y,w,h)

def convert_annotation(xml_files_path, save_txt_files_path, imgs_in_path, imgs_out_path, classes):
    
    img_files = os.listdir(imgs_in_path)
    img_files = [img for img in img_files if img.split('.')[-1] == 'jpg']
    
    xml_files = os.listdir(xml_files_path)
    xml_files = [xml for xml in xml_files if xml.split('.')[-1] == 'xml']
    
    for xml_name in xml_files:

        xml_file = os.path.join(xml_files_path, xml_name)
        out_txt_path = os.path.join(save_txt_files_path, xml_name.split('.')[0] + '.txt')
        
        src_path = os.path.join(imgs_in_path, xml_name.split('.')[0] + '.jpg')
        dst_path = os.path.join(imgs_out_path, xml_name.split('.')[0] + '.jpg')

        tree=ET.parse(xml_file)
        root = tree.getroot()
        size = root.find('size')
        w = int(size.find('width').text)
        h = int(size.find('height').text)

        for obj in root.iter('object'):
            difficult = obj.find('difficult').text
            cls = obj.find('name').text
            if cls not in classes or int(difficult) == 1:
                continue
            out_txt_f = open(out_txt_path, 'a')  # if obj's class not in class_list then no txt created
            cls_id = classes.index(cls)
            xmlbox = obj.find('bndbox')
            b = (float(xmlbox.find('xmin').text), float(xmlbox.find('xmax').text), float(xmlbox.find('ymin').text), float(xmlbox.find('ymax').text))
            # b=(xmin, xmax, ymin, ymax)

            bb = convert((w,h), b)
            shutil.copyfile(src_path, dst_path) #如果有class列表中的对象则将对应的图像复制出来
            out_txt_f.write(str(cls_id) + " " + " ".join([str(a) for a in bb]) + '\n')



class RandomImageGenerator():

    def __init__(self, filepath=None, count=None):
        # Default path
        if filepath == None:
            filepath = "clean_images/"
        
        # Process on all images if not specified
        if count == None:
            count = len(os.listdir(filepath))
        
        # Character Libraries
        chinese_char_file = open(
            "chinese_characters.txt", 
            "r", 
            encoding="utf-8"
        )
        self.chinese_char = chinese_char_file.read()
        chinese_char_file.close()
        self.english_char = [chr(asc) for asc in range(48, 58)] + [chr(asc) for asc in range(65, 123)]
        self.ascii_char = [chr(asc) for asc in range(32, 256)]
        # Initialization
        self.images = self.__image_iterator(filepath, count)

        # Default output configurations
        self.output_path = "images_with_watermarks/"
        self.output_label = max([int(name[:-4]) for name in os.listdir(self.output_path)] + [0]) + 1
        self.output_type = "png"
    
    def __image_iterator(self, filepath, count):
        # Format Alignment
        if filepath[-1] is not "/":
            filepath += "/"
        
        # Allow randomly select n images to save time
        image_lst = os.listdir(filepath)
        if count != None and count > 0 and count < len(image_lst):
            image_lst = sample(image_lst, count)

        # Image iterator
        for image_id in image_lst:
            image_path = "".join([filepath, image_id])
            image = Image.open(image_path)
            yield image

    def __text_generator(self, dictionary):
        length = randint(4, 12)
        text = "".join([dictionary[randint(0, len(dictionary) - 1)] for i in range(length)])
        return text
    
    def __watermark_generator(self):
        filepath = "watermarks/"
        image_lst = os.listdir(filepath)
        # Watermark iterator
        while True:
            image_id = sample(image_lst, 1)[0]
            image_path = "".join([filepath, image_id])
            image = Image.open(image_path)
            yield image

    def __add_text_to_image(self, mode, image, text, place):
        
        if mode == "ch":
            fontpath = "./simsun.ttc"  # 宋体
            font = ImageFont.truetype(fontpath, 32)
            character_special_resize = 4
        elif mode == "en":
            font = None
            character_special_resize = 1
        elif mode == "asc":
            font = None
            character_special_resize = 1
        else:
            print("mode not supported")
            print("current modes available: en=English, ch=Chinese, asc=ASCII-chars")
            raise ValueError

        rgba_image = image.convert('RGBA')
        
        # Enlarge small images, reduce big images
        if rgba_image.size[0] < 100:
            size_factor = 0.3 + random() / 2
        else:
            size_factor = 1 + random() * 2
        size_factor = size_factor / character_special_resize
        
        
        # A separate layer for watermark texts
        text_overlay = Image.new(
            'RGBA', 
            (int(rgba_image.size[0] // size_factor), int(rgba_image.size[1] // size_factor)), 
            (255, 255, 255, 0)
        )
        image_draw = ImageDraw.Draw(text_overlay)

        text_size_x, text_size_y = image_draw.textsize(text, font=font)
        if place=="random":
            top_left_corner_x = randint(0, int(rgba_image.size[0] // size_factor - text_size_x))
            top_left_corner_y = randint(0, int(rgba_image.size[1] // size_factor - text_size_y))
        elif place=="corner":
            top_left_corner_x = rgba_image.size[0] // size_factor - text_size_x
            top_left_corner_y = rgba_image.size[1] // size_factor - text_size_y
        text_xy = (top_left_corner_x, top_left_corner_y)

        # Random Color and Transparency (up to a reasonable range)
        sample_color = rgba_image.getpixel((  # Tuple
            int((top_left_corner_x + 0.5 * text_size_x) * size_factor),
            int((top_left_corner_y + 0.5 * text_size_y) * size_factor)
        ))
        
        # Background color matching check (TODO: SAMPLE MORE POINTS OR USE BOX MEAN)
        while True:
            red, green, blue = randint(0, 50), randint(0, 50), randint(0, 50)
            transparency = randint(100, 255)
            if abs(red - sample_color[0]) + abs(green - sample_color[1]) + abs(blue - sample_color[2]) > 100:
                break
            red, green, blue = 255 - red, 255 - green, 255 - blue
            if abs(red - sample_color[0]) + abs(green - sample_color[1]) + abs(blue - sample_color[2]) > 100:
                break
        
        # Overlay texts onto the image
        image_draw.text(text_xy, text, font=font, fill=(red, green, blue, transparency))
        text_overlay = text_overlay.resize(rgba_image.size)
        image_with_text = Image.alpha_composite(rgba_image, text_overlay)

        return image_with_text

    def __add_watermark_to_image(self, image, watermark):
        rgba_image = image.convert('RGBA')
        rgba_watermark = watermark.convert('RGBA')
  
        image_x, image_y = rgba_image.size
        watermark_x, watermark_y = rgba_watermark.size
  
        scale = randint(8, 12)
        watermark_scale = max(image_x / (scale * watermark_x), image_y / (scale * watermark_y))
        new_size = (int(watermark_x * watermark_scale), int(watermark_y * watermark_scale))
        rgba_watermark = rgba_watermark.resize(new_size, resample=Image.ANTIALIAS)
        rgba_watermark_mask = rgba_watermark.convert("L").point(lambda x: min(x, 180))
        rgba_watermark.putalpha(rgba_watermark_mask)
  
        watermark_x, watermark_y = rgba_watermark.size

        if random() > 0.5: # Random half
            rgba_image.paste(rgba_watermark, (image_x - watermark_x, image_y - watermark_y), rgba_watermark_mask) # bot-right
        else:
            rgba_image.paste(rgba_watermark, (image_x - watermark_x, 0), rgba_watermark_mask) # top-right
  
        return rgba_image

    def english_generator(self, place="random"):
        if place not in ["random", "corner"]:
            raise ValueError
        for image in tqdm(self.images):
            text = self.__text_generator(self.english_char)
            processed_image = self.__add_text_to_image("en", image, text, mode)
            processed_image.save("{}/{}.{}".format(self.output_path, self.output_label, self.output_type))
            self.output_label += 1
        print("DONE")
            
    def chinese_generator(self, place="random"):
        if place not in ["random", "corner"]:
            raise ValueError
        for image in tqdm(self.images):
            text = self.__text_generator(self.chinese_char)
            processed_image = self.__add_text_to_image("ch", image, text, mode)
            processed_image.save("{}/{}.{}".format(self.output_path, self.output_label, self.output_type))
            self.output_label += 1
        print("DONE")
    
    def ascii_generator(self, place="random"):
        if place not in ["random", "corner"]:
            raise ValueError
        for image in tqdm(self.images):
            text = self.__text_generator(self.ascii_char)
            processed_image = self.__add_text_to_image("asc", image, text, place)
            processed_image.save("{}/{}.{}".format(self.output_path, self.output_label, self.output_type))
            self.output_label += 1
        print("DONE")

    def image_generator(self):
        watermarks = self.__watermark_generator()
        for image in tqdm(self.images):
            processed_image = self.__add_watermark_to_image(image, next(watermarks))
            processed_image.save("{}/{}.{}".format(self.output_path, self.output_label, self.output_type))
            self.output_label += 1
        print("DONE")
