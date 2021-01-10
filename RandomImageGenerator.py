import os

from PIL import Image, ImageDraw, ImageFont
from random import randint, sample

class RandomImageGenerator():

    def __init__(self, filepath=None, count=None):
        # Default path
        if filepath == None:
            filepath = "data/random_image_generator_resource/clean_images"
        
        if count == None:
            count = len(os.listdir(filepath))

        chinese_char_file = open(
            "./data/random_image_generator_resource/chinese_characters.txt", 
            "r", 
            encoding="utf-8"
        )
        self.chinese_char = chinese_char_file.read()
        
        self.ascii_char = [chr(asc) for asc in range(32, 256)]
        self.images = self.__image_iterator(filepath, count)
        self.output_path = "data/random_image_generator_resource/images_with_watermarks"
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

    def __add_text_to_image(self, image, text):
        rgba_image = image.convert('RGBA')
        text_overlay = Image.new('RGBA', rgba_image.size, (255, 255, 255, 0))
        image_draw = ImageDraw.Draw(text_overlay)
        #text_size_x, text_size_y = image_draw.textsize(text)
        text_size_x = randint(rgba_image.size[0] // 20, rgba_image.size[0] // 5)
        text_size_y = randint(rgba_image.size[1] // 20, rgba_image.size[1] // 5)
        # Random Place
        top_left_corner_x = randint(0, rgba_image.size[0] - text_size_x)
        top_left_corner_y = randint(0, rgba_image.size[1] - text_size_y)
        text_xy = (top_left_corner_x, top_left_corner_y)
        
        # Random Color and Transparency (up to a reasonable range)
        red = 200 + randint(0, 55)
        green = 200 + randint(0, 55)
        blue = 200 + randint(0, 55)
        transparency = 100 + randint(0, 155)

        image_draw.text(text_xy, text, fill=(red, green, blue, transparency))
        image_with_text = Image.alpha_composite(rgba_image, text_overlay)

        return image_with_text

    def english_generator(self):
        for image in self.images:
            text = self.__text_generator(self.ascii_char)
            processed_image = self.__add_text_to_image(image, text)
            processed_image.save("{}/{}.{}".format(self.output_path, self.output_label, self.output_type))
            self.output_label += 1
            
    def chinese_generator(self):
        for image in self.images:
            text = self.__text_generator(self.chinese_char)
            processed_image = self.__add_text_to_image(image, text)
            processed_image.save("{}/{}.{}".format(self.output_path, self.output_label, self.output_type))
            self.output_label += 1
    def image_generator(self):
        print("NOT IMPLEMENTED YET!")