#!/bin/bash

# Remove Previously Created Files
rm -r ../data/original_images
rm -r ../data/watermarked_images
rm -r ../data/test_images
rm -r ../data/VOCdevkit/VOC2012/Annotations
rm -r ../data/VOCdevkit/VOC2012/JPEGImages
rm -r ../retinaNet/save_weights

# Create New Folders
mkdir ../data/original_images
mkdir ../data/watermarked_images
mkdir ../data/test_images
mkdir ../data/VOCdevkit/VOC2012/Annotations
mkdir ../data/VOCdevkit/VOC2012/JPEGImages
mkdir ../retinaNet/save_weights

# Download Memes from DB
python3 memegle_scrapper.py

# Attach Watermarks
cd ../watermark_generator
python3 random_image_generator.py
python3 generate_XML.py

# Train Val Split
cd ../scripts
python3 train_val_split.py

# Train
cd ../retinaNet
python3 train.py
