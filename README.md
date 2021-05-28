# watermark-detector

### Instructions

#### Training

1. Download resnet50 backbone from Memegle google drive at `Memegle/database/watermark-detector-related-data/retinanet_resnet50_fpn.pth`. Put this backbone in `./retinaNet/backbone/`.

2. Download watermark logos from Memegle google drive at `Memegle/databse/watermark-detector-related-data/watermark-logos/`. Put them in `./watermark_generator/watermarks`.

3. Install related packages as per missing requirements (TODO: generate a `requirements.txt`).

4. Run the following code: `cd scripts`, then `bash ./train_from_scratch.sh`.


#### Predicting

1. Put testing images under `./data/test_images/`.

2. Run the following code: `cd retinaNet`, then `python3 predict.py`.

3. See the predictions in `./data/predictions.txt`.
