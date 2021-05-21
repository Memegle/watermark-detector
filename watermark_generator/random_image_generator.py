import os

from PIL import Image, ImageDraw, ImageFont
from random import randint, random, sample
from tqdm import tqdm

class RandomImageGenerator():

    def __init__(self, filepath=None, count=None):
        # Default path
        if filepath == None:
            filepath = "../data/original_images/"
        
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
        self.output_path = "../data/watermarked_images/"
        self.output_label = max([int(name[:-4]) for name in os.listdir(self.output_path)] + [0]) + 1
        self.output_type = "png"
    
    def __image_iterator(self, filepath, count):
        # Format Alignment
        if filepath[-1] != "/":
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
        
        bbox = [str(top_left_corner_x), str(top_left_corner_x + text_size_x), str(top_left_corner_y), str(top_left_corner_y + text_size_y)]
        return image_with_text, bbox

    def __add_watermark_to_image(self, image, watermark):
        rgba_image = image.convert('RGBA')
        rgba_watermark = watermark.convert('RGBA')
  
        image_x, image_y = rgba_image.size
        watermark_x, watermark_y = rgba_watermark.size
  
        scale = randint(4, 8)
        watermark_scale = max(image_x / (scale * watermark_x), image_y / (scale * watermark_y))
        new_size = (int(watermark_x * watermark_scale), int(watermark_y * watermark_scale))
        rgba_watermark = rgba_watermark.resize(new_size, resample=Image.ANTIALIAS)
        rgba_watermark_mask = rgba_watermark.convert("L").point(lambda x: min(x, 180))
        #rgba_watermark.putalpha(rgba_watermark_mask)
  
        watermark_x, watermark_y = rgba_watermark.size

        if random() > 0.5: # Random half
            rgba_image.paste(rgba_watermark, (image_x - watermark_x, image_y - watermark_y), rgba_watermark_mask) # bot-right
            bbox = [str(image_x - watermark_x), str(image_x), str(image_y - watermark_y), str(image_y)]
        else:
            rgba_image.paste(rgba_watermark, (image_x - watermark_x, 0), rgba_watermark_mask) # top-right
            bbox = [str(image_x - watermark_x), str(image_x), str(0), str(watermark_y)]
        return rgba_image, bbox

    def english_generator(self, place="random"):
        if place not in ["random", "corner"]:
            raise ValueError
        for image in tqdm(self.images):
            text = self.__text_generator(self.english_char)
            processed_image, bbox = self.__add_text_to_image("en", image, text, place)
            processed_image.save("{}/{}.{}".format(self.output_path, self.output_label, self.output_type))
            with open("{}/{}.txt".format(self.output_path, self.output_label), "w") as f:
                f.write(", ".join(bbox))
            self.output_label += 1
        print("DONE")
            
    def chinese_generator(self, place="random"):
        if place not in ["random", "corner"]:
            raise ValueError
        for image in tqdm(self.images):
            text = self.__text_generator(self.chinese_char)
            processed_image, bbox = self.__add_text_to_image("ch", image, text, place)
            processed_image.save("{}/{}.{}".format(self.output_path, self.output_label, self.output_type))
            with open("{}/{}.txt".format(self.output_path, self.output_label), "w") as f:
                f.write(", ".join(bbox))
            self.output_label += 1
        print("DONE")
    
    def ascii_generator(self, place="random"):
        if place not in ["random", "corner"]:
            raise ValueError
        for image in tqdm(self.images):
            text = self.__text_generator(self.ascii_char)
            processed_image, bbox = self.__add_text_to_image("asc", image, text, place)
            processed_image.save("{}/{}.{}".format(self.output_path, self.output_label, self.output_type))
            with open("{}/{}.txt".format(self.output_path, self.output_label), "w") as f:
                f.write(", ".join(bbox))
            self.output_label += 1
        print("DONE")

    def image_generator(self):
        watermarks = self.__watermark_generator()
        for image in tqdm(self.images):
            processed_image, bbox = self.__add_watermark_to_image(image, next(watermarks))
            processed_image.save("{}/{}.{}".format(self.output_path, self.output_label, self.output_type))
            with open("{}/{}.txt".format(self.output_path, self.output_label), "w") as f:
                f.write(" ".join(bbox))
            self.output_label += 1
        print("DONE")
        
if __name__ == "__main__":
    rig = RandomImageGenerator()
    rig.image_generator()
