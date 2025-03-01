import os

from sympy import print_glsl


def rename_last_level_directories(src):
    # 遍历源目录
    for root, dirs, files in os.walk(src):
        # 如果当前目录没有子目录，说明是最后一级目录——lry
        if not dirs:
            #获取文件之前的所有目录路径——lry
            current_dir = root #/media/lirongyaoper/350142ad-6ead-4db5-b07c-25bd698ad3c7/lungCT/300yuanshi/DI_AV15788847/slices
            # print(current_dir)
            #获取上一级目录的路径——lry
            parent_dir = os.path.dirname(current_dir)
            #对目录路径使用("/")进行分割——lry
            name_all = parent_dir.split('/')#['', 'media', 'lirongyaoper', '350142ad-6ead-4db5-b07c-25bd698ad3c7', 'lungCT', '300yuanshi', 'DI_TK96907975']
            last_level_dir_name = os.path.basename(current_dir)#slicer
            # print(name_all)
            if name_all[-1] =="nii":

                #提取路径中的某一目录名称——lry
                new_dir_name =name_all[-2]
                #合成全新的路径名——lry
                new_dir_path = os.path.join(parent_dir, new_dir_name)
                print(new_dir_path)
                # 修改全路径——lry
                # os.rename(current_dir, new_dir_path)
                # print(f"重命名目录: {current_dir} 到 {new_dir_path}")

if __name__ == "__main__":
    # 使用示例
    source_directory = '/media/lirongyaoper/350142ad-6ead-4db5-b07c-25bd698ad3c7/shuju500/300标注数据'  # 源目录路径

    rename_last_level_directories(source_directory)