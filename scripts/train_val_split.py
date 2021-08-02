import numpy as np

image_names = np.loadtxt("../data/VOCdevkit/VOC2012/ImageSets/Main/trainval.txt", dtype=int)
cutoff_val = int(len(image_names) * 0.7)
cutoff_test = int(len(image_names) * 0.9)
train = image_names[:cutoff_val]
val = image_names[cutoff_val:cutoff_test]
test = image_names[cutoff_test:]
np.savetxt("../data/VOCdevkit/VOC2012/ImageSets/Main/train.txt", train, fmt="%i")
np.savetxt("../data/VOCdevkit/VOC2012/ImageSets/Main/val.txt", val, fmt="%i")
np.savetxt("../data/VOCdevkit/VOC2012/ImageSets/Main/test.txt", val, fmt="%i")
