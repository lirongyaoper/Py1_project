import os
import shutil

def delete_specific_folder(root_dir, target_folder_name):
    for dirpath, dirnames, filenames in os.walk(root_dir):
        if target_folder_name in dirnames:
            target_path = os.path.join(dirpath, target_folder_name)
            try:
                shutil.rmtree(target_path)  # 删除整个目录及其内容
                print(f"已删除文件夹: {target_path}")
            except Exception as e:
                print(f"删除文件夹 {target_path} 时出错: {e}")

# 示例使用
if __name__ == "__main__":
    root_directory = "/mnt/data/lung_labels_data_nii_seg/"  # 替换为您要搜索的根目录路径
    folder_to_delete = "stl"  # 替换为您要删除的文件夹名称

    delete_specific_folder(root_directory, folder_to_delete)
