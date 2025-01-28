import  os
import  SimpleITK as sitk
data_dir = "/home/lirongyaoper/Softwares/work_dir/nnUNet_raw_data_base/Dataset001_imagesTr/imagesTr/"
for filename in os.listdir(data_dir):
    if filename.endswith(".nii.gz"):
        try:
            image = sitk.ReadImage(os.path.join(data_dir,filename))
            print(f"{filename}: {image.GetSize()}")
        except Exception as e:
            print(f"Error reading {filename}:{e}")
