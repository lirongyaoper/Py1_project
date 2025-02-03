import os  # 导入os模块
from xml.dom.minidom import Document




def dcm_niigz(source_path,dest_dir):

    if not os.path.exists(dest_dir):
        os.makedirs(dest_dir)

    list = os.listdir(source_path)

    for i in range(0, len(list)):  # 遍历目录下的所有文件夹
        floder_path = os.path.join(dest_dir,list[i])

        os.makedirs(floder_path)
        path = os.path.join(source_path, list[i])
        print(path)
        os.system(f'dcm2niix -o {floder_path}/ -z y {path}')
        print(f'目前正在转换目录为{list[i]}的dcm文件夹，这是转换的第{i+1}个，已完成工作的({i+1}/{len(list)})%')
if __name__ =="__main__":
    # source_path = "/media/lirongyaoper/350142ad-6ead-4db5-b07c-25bd698ad3c7/lungCT/yuanshi184_unzip"
    source_path = "/media/lirongyaoper/350142ad-6ead-4db5-b07c-25bd698ad3c7/lungCT/257/images/di160/"
    dest_dir = "/media/lirongyaoper/350142ad-6ead-4db5-b07c-25bd698ad3c7/lungCT/257/images/di160nii/"
    dcm_niigz(source_path,dest_dir)