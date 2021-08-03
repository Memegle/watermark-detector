import os
import time
import json

import torch
from PIL import Image
import matplotlib.pyplot as plt

from torchvision import transforms
from network_files import RetinaNet
from backbone import resnet50_fpn_backbone, LastLevelP6P7
from draw_box_utils import draw_box


def create_model(num_classes):
    # resNet50+fpn+retinanet
    # 注意，这里的norm_layer要和训练脚本中保持一致
    backbone = resnet50_fpn_backbone(norm_layer=torch.nn.BatchNorm2d,
                                     returned_layers=[2, 3, 4],
                                     extra_blocks=LastLevelP6P7(256, 256))
    model = RetinaNet(backbone, num_classes)

    return model


def time_synchronized():
    torch.cuda.synchronize() if torch.cuda.is_available() else None
    return time.time()

def load_model(device):
    model = create_model(num_classes=1)
    # load train weights
    train_weights = "./save_weights/model.pth"
    assert os.path.exists(train_weights), "{} file dose not exist.".format(train_weights)
    model.load_state_dict(torch.load(train_weights, map_location=device)["model"])
    model.to(device)
    return model

def single_image_classifier(img_path):
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print("using {} device.".format(device))
    model = load_model(device)
    original_img = Image.open(img_path)
    if img_path[-4:] == '.gif': # If the input image is a gif, pick the first frame for testing
        original_img.seek(0)
    # from pil image to tensor, do not normalize image
    data_transform = transforms.Compose([transforms.ToTensor()])
    img = data_transform(original_img)
    # expand batch dimension
    img = torch.unsqueeze(img, dim=0)

    model.eval()  # 进入验证模式
    with torch.no_grad():
        # init
        img_height, img_width = img.shape[-2:]
        init_img = torch.zeros((1, 3, img_height, img_width), device=device)
        model(init_img)
        t_start = time_synchronized()
        predictions = model(img.to(device))[0]
        t_end = time_synchronized()
        print("inference+NMS time: {}".format(t_end - t_start))
        predict_boxes = predictions["boxes"].to("cpu").numpy()
        predict_classes = predictions["labels"].to("cpu").numpy()
        predict_scores = predictions["scores"].to("cpu").numpy()
        if len(predict_boxes) == 0 or max(predict_scores) < 0.5:  # Can change this value for trade-off between AP and Recall
            return False, -1.0
        else:
            return True, max(predict_scores)

def main():
    # get devices
    device = torch.device("cuda:0" if torch.cuda.is_available() else "cpu")
    print("using {} device.".format(device))

    # create model
    # 注意：不包含背景
    model = create_model(num_classes=1)

    # load train weights
    train_weights = "./save_weights/model.pth"
    assert os.path.exists(train_weights), "{} file dose not exist.".format(train_weights)
    model.load_state_dict(torch.load(train_weights, map_location=device)["model"])
    model.to(device)

    prediction_file = open("../data/predictions.txt", 'w')
    folder_path = '../data/test_images/'
    entries = os.listdir(folder_path)
    for img_name in entries:
        img_path = folder_path + img_name
        # load image
        original_img = Image.open(img_path)
        if img_path[-4:] == '.gif': # If the input image is a gif, pick the first frame for testing
            original_img.seek(0)
        # from pil image to tensor, do not normalize image
        data_transform = transforms.Compose([transforms.ToTensor()])
        img = data_transform(original_img)
        # expand batch dimension
        img = torch.unsqueeze(img, dim=0)

        model.eval()  # 进入验证模式
        with torch.no_grad():
            # init
            img_height, img_width = img.shape[-2:]
            init_img = torch.zeros((1, 3, img_height, img_width), device=device)
            model(init_img)

            t_start = time_synchronized()
            predictions = model(img.to(device))[0]
            t_end = time_synchronized()
            print("inference+NMS time: {}".format(t_end - t_start))

            predict_boxes = predictions["boxes"].to("cpu").numpy()
            predict_classes = predictions["labels"].to("cpu").numpy()
            predict_scores = predictions["scores"].to("cpu").numpy()

            if len(predict_boxes) == 0 or max(predict_scores) < 0.5:  # Can change this value for trade-off between AP and Recall
                prediction_file.write("{}, {}, {}\n".format(img_name, "False", -1.0))
            else:
                prediction_file.write("{}, {}, {}\n".format(img_name, "True", max(predict_scores)))
                
    prediction_file.close()


if __name__ == '__main__':
    main()

