import os

from PIL import Image, ImageDraw, ImageFont
from random import randint, sample

class RandomImageGenerator():

    def __init__(self, filepath, count=None):
        chinese_char_file = open(
            "./data/random_image_generator_resource/chinese_characters.txt", 
            "r", 
            encoding="utf-8"
        )
        self.chinese_char = chinese_char_file.read()
        self.ascii_char = [chr(asc) for asc in range(32, 256)]
        self.images = self.__image_iterator(filepath, count)
    
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
            length = randint(2, 12)
            text = "".join([dictionary[randint(0, len(dictionary) - 1)] for i in range(length)])
            return text

    def __add_text_to_image(self, image, text):
        rgba_image = image.convert('RGBA')
        text_overlay = Image.new('RGBA', rgba_image.size, (255, 255, 255, 0))
        image_draw = ImageDraw.Draw(text_overlay) 
        text_size_x, text_size_y = image_draw.textsize(text)
 
        #text_xy = (rgba_image.size[0] - text_size_x, rgba_image.size[1] - text_size_y)  #底部
        text_xy = ((rgba_image.size[0] - text_size_x)/2, (rgba_image.size[1] - text_size_y)/2) #中间
        #size[0]是长，size[1]是宽

        image_draw.text(text_xy, text, fill=(225, 225, 225, 225))
        image_with_text = Image.alpha_composite(rgba_image, text_overlay)

        return image_with_text

    def english_generator(self):
        for image in self.images:
            text = self.__text_generator(self.ascii_char)

    def chinese_generator(self):
        print(1)

    def image_generator(self):
        print(2)