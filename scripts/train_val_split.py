import numpy as np

image_names = np.loadtxt("../data/VOCdevkit/VOC2012/ImageSets/Main/trainval.txt", dtype=int)
cutoff_len = int(len(image_names) * 0.7)
train = image_names[:cutoff_len]
val = image_names[cutoff_len:]
np.savetxt("../data/VOCdevkit/VOC2012/ImageSets/Main/train.txt", train, fmt="%i")
np.savetxt("../data/VOCdevkit/VOC2012/ImageSets/Main/val.txt", val, fmt="%i")
