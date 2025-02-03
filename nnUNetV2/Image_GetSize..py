import  os
import  SimpleITK as sitk

def show_files(path):
    # 首先遍历当前目录所有文件及文件夹
    file_list = os.listdir(path)
    # 准备循环判断每个元素是否是文件夹还是文件，是文件的话，把名称传入list，是文件夹的话，递归
    for file in file_list:
        # 利用os.path.join()方法取得路径全名，并存入cur_path变量，否则每次只能遍历一层目录
        cur_path = os.path.join(path, file)
        # 判断是否是文件夹
        if os.path.isdir(cur_path):
            show_files(cur_path)
        else:
            image = sitk.ReadImage(cur_path)
            print(f"{file}: {image.GetSize()}")



data_dir = "/media/lirongyaoper/350142ad-6ead-4db5-b07c-25bd698ad3c7/lungCT/合并203/lry"
# for filename in os.listdir(data_dir):
#     if filename.endswith(".nii.gz"):
#         try:
#             image = sitk.ReadImage(os.path.join(data_dir,filename))
#             print(f"{filename}: {image.GetSize()}")
#         except Exception as e:
#             print(f"Error reading {filename}:{e}")

show_files(data_dir)