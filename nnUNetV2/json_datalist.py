import os
import json
import random
import shutil
import tempfile
from monai.config import print_config
from monai.apps import download_and_extract
def save_json(json_dict):
    datalist_file = "dataset.json"
    with open(datalist_file, "w", encoding="utf-8") as f:
        json.dump(json_dict, f, ensure_ascii=False, indent=4)
    print(f"Datalist is saved to {datalist_file}")

root_dir = r'/mnt/data/lungCT/databasebak_center/1009/'
test_dir = os.path.join(root_dir, "imagesTs/")
train_dir = os.path.join(root_dir, "imagesTr/")
label_dir = os.path.join(root_dir, "labelsTr/")
json_dict = {}
json_dict['name'] = "Lung"
json_dict['description'] = "Lung and cancer segmentation"
json_dict['tensorImageSize'] = "4D"
json_dict['reference'] = "The Cancer Imaging Archive"
json_dict['licence'] = "CC-BY-SA 4.0"
json_dict['release'] = "0.0"

json_dict['channel_names'] = {
    "0": "CT",
}
json_dict['labels'] = {
    "0":"background",
    "1":"pulmonary vein",
    "2":"bronchus",
    "3":"pulmonary artery"
}
json_dict['numTraining'] = 752  # 应该是210例
json_dict['file_ending'] = ".nii.gz"
json_dict['numTest'] = 0
json_dict["testing"] = [
    {"image": "./imagesTs/" + file} for file in os.listdir(test_dir) if (".nii.gz" in file) and ("._" not in file)
]
json_dict["training"] = [
    {"image": "./imagesTr/" + file, "label": "./labelsTr/" + file}
    for file in os.listdir(train_dir)
    if (".nii.gz" in file) and ("._" not in file)

]
save_json(json_dict)


