# watermark-detector

Not official one, for my own use now:

1. Download resnet50 backbone, link found in train.py

2. Install related packages (see requirements.txt)

3. Download clean images from database, put in data/original_images

4. Set route to watermark_generator, run random_image_generator.py (default to image watermarks for now), then run generate_XML.py

5. Go to data/VOCdefkit/VOC2012/ImageSets/Main, open trainval.txt, do a manual train-val split, paste to corresponding files. (Need automation later)

6. Go to retinaNet, run train.py.

7. Run test.py with any testing image called 'test.jpg'. (Need automation for scalable output)
