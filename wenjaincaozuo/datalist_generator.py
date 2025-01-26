import os
import json
import random
import shutil
import tempfile
from monai.config import print_config
from monai.apps import download_and_extract

# https://github.com/Project-MONAI/tutorials/blob/main/auto3dseg/notebooks/msd_datalist_generator.ipynb
root_dir = r'/home/lirongyaoper/Softwares/Monai/datasets/Lung'
test_dir = os.path.join(root_dir, "imagesTs/")
train_dir = os.path.join(root_dir, "imagesTr/")
label_dir = os.path.join(root_dir, "labelsTr/")

datalist_json = {"testing": [], "training": []}

datalist_json["testing"] = [
    {"image": "./imagesTs/" + file} for file in os.listdir(test_dir) if (".nii.gz" in file) and ("._" not in file)
]
datalist_json["training"] = [
    {"image": "./imagesTr/" + file, "label": "./labelsTr/" + file}
    for file in os.listdir(train_dir)
    if (".nii.gz" in file) and ("._" not in file)
]
datalist_file = "dataset.json"
with open(datalist_file, "w", encoding="utf-8") as f:
    json.dump(datalist_json, f, ensure_ascii=False, indent=4)
print(f"Datalist is saved to {datalist_file}")
