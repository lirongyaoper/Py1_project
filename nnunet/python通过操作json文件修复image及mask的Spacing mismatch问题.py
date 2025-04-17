import os
import  json
from PIL import Image
import nibabel as nib
import SimpleITK as sitk
jsonpath = r"/home/lirongyaoper/Softwares/work_dir/nnUNet_raw_data_base/Dataset001_imagesTr/dataset.json"

with open(jsonpath,"r") as file:
    data = json.load(file)
for i in range(len(data["training"])):
    image = sitk.ReadImage(data["training"][i]["image"])

    seg = sitk.ReadImage(data["training"][i]["label"])
    seg.SetSpacing(image.GetSpacing())
    seg.SetOrigin(image.GetOrigin())
    seg.SetDirection(image.GetDirection())

    # Save corrected segmentation
    sitk.WriteImage(seg, data["training"][i]["label"])
