# Statistical-Significance-DefectDetection
Repo of the paper Towards Statistically Significant Results: A Methodology for Evaluating Surface Defect Detection Using Deep Learning

# Setup
The system used to evaluated this code is an Ubuntu 22.04, Python 3.10 and a NVIDIA Geforce Rtx 3090.
Follow this stepts to prepare the installation:

```
pip3 install torch==2.4.0 torchvision==0.19.0
pip3 install -U openmim
mim install mmcv
pip3 install ultralytics==8.3.3

git clone https://github.com/darioglema/Statistical-Significance-DefectDetection.git
cd Statistical-Significance-DefectDetection/

# IMPORTANT: check Python version
cp models_implementation/conv.py ../lib/python3.10/site-packages/ultralytics/nn/modules/
cp models_implementation/__init__.py ../lib/python3.10/site-packages/ultralytics/nn/modules/
cp models_implementation/tasks.py ../lib/python3.10/site-packages/ultralytics/nn/
```

# Dataset
Follow this steps to download and prepare the dataset:
```
# Download dataset from Kaggle
curl -L -o ./neu-surface-defect-database.zip https://www.kaggle.com/api/v1/datasets/download/kaustubhdikshit/neu-surface-defect-database
unzip neu-surface-defect-database.zip
rm neu-surface-defect-database.zip

# Create the folders structure
mkdir NEU-DET/all
mkdir NEU-DET/all/images
mkdir NEU-DET/all/annotations
mkdir NEU-DET/all/labels

cp NEU-DET/train/images/**/* NEU-DET/all/images/
cp NEU-DET/train/annotations/* NEU-DET/all/annotations/
cp NEU-DET/validation/images/**/* NEU-DET/all/images/
cp NEU-DET/validation/annotations/* NEU-DET/all/annotations/
rm -rf NEU-DET/train/ NEU-DET/validation/

# Transform data
python3 transform_data.py 
# rm -rf NEU-DET/all/annotations # optional
```

# Test models
Run this command to test the models. All implemented models are located in the models/ folder. As a cross-validation has been performed, four models have been generated for each implementation. To evaluate a model it is necessary to use the appropriate test set. These data are located in the data/ folder. For example, to evaluate the results of the third YOLOv8-Unet model, you would use the model models/yolov8n-unet-3.pt with the dataset data/NEU-DET-3.yaml.

```
nano ~/.config/Ultralytics/settings.json
# In dataset_dir add the path to the directory of this repository
```

```
yolo detect val model=models/<model.pt> data=data/NEU-DET-<number>.yaml 
```

# Acknowledgments
We extend our gratitude to [Ultralytics](https://github.com/ultralytics) for developing a versatile framework that facilitates modifications to object detection models.


