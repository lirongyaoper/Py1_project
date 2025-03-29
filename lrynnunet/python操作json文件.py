import os
import  json
from PIL import Image
import nibabel as nib
jsonpath = r"/home/lirongyaoper/Softwares/work_dir/nnUNet_raw_data_base/Dataset001_imagesTr/dataset.json"

with open(jsonpath,"r") as file:
    data = json.load(file)
for i in range(len(data["training"])):
    image = nib.load(data["training"][i]["image"])

    mask = nib.load(data["training"][i]["label"])
    if image.shape != mask.shape:
        print(data["training"][i]["image"])
