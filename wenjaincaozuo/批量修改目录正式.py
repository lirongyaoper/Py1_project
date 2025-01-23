import os

def rename_last_level_directories(src):
    # 遍历源目录
    for root, dirs, files in os.walk(src):
        # 如果当前目录没有子目录，说明是最后一级目录
        if not dirs:

            current_dir = root #/media/lirongyaoper/350142ad-6ead-4db5-b07c-25bd698ad3c7/lungCT/300yuanshi/DI_AV15788847/slices

            parent_dir = os.path.dirname(current_dir)
            name_all = parent_dir.split('/')#['', 'media', 'lirongyaoper', '350142ad-6ead-4db5-b07c-25bd698ad3c7', 'lungCT', '300yuanshi', 'DI_TK96907975']

            last_level_dir_name = os.path.basename(current_dir)#slicer

            new_dir_name =name_all[-1]
            new_dir_path = os.path.join(parent_dir, new_dir_name)
            #
            #
            os.rename(current_dir, new_dir_path)
            print(f"重命名目录: {current_dir} 到 {new_dir_path}")

# 使用示例
source_directory = '/media/lirongyaoper/350142ad-6ead-4db5-b07c-25bd698ad3c7/lungCT/300yuanshi'  # 源目录路径

rename_last_level_directories(source_directory)