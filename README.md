# watermark-detector

A computer vision component of Memegle to classify the existence of watermarks

## Order of execution:

1. Go to *root dir*.
2. Run `scripts/setup_envorinment.sh`
3. Manually download `resnet50_coco_best_v2.1.0.h5` from Memegle google drive, under `database/watermark-starter-file`, paste that under `retinanet_keras/model_data` (need to write automation code later)
4. Run `scripts/train.sh`
5. After finished everything, run `scripts/clean_up.sh`
