from pathlib import Path
import os
def batch_rename(images_dir, labels_dir, start_index):
    # 使用pathlib创建路径对象
    images_path = Path(images_dir)
    labels_path = Path(labels_dir)

    # 生成文件名映射字典（保留双扩展名）
    def get_name_map(folder_path):
        return {f.stem.split('.')[0]: f for f in folder_path.glob('*.*.*')}  # 匹配双扩展名文件

    images_map = get_name_map(images_path)
    labels_map = get_name_map(labels_path)
    print(images_map)
    # 获取同名文件列表
    common_names = set(images_map.keys()) & set(labels_map.keys())

    # 按顺序处理每个文件
    for idx, name in enumerate(sorted(common_names), start=start_index):
        # 处理images文件
        img_file = images_map[name]
        new_img_name = f"{name}_{idx:04d}_0000{''.join(img_file.suffixes)}"
        new_img_path = images_path / new_img_name
        # os.rename(img_file, new_img_path)
        # 处理labels文件
        lbl_file = labels_map[name]
        new_lbl_name = f"{name}_{idx:04d}{''.join(lbl_file.suffixes)}"
        new_lbl_path = labels_path / new_lbl_name
        # os.rename(lbl_file, new_lbl_path)
        # print(f"重命名完成：\n{img_file.name} -> {new_img_name}\n{lbl_file.name} -> {new_lbl_name}\n")
# 使用示例
if __name__ == "__main__":
    images_folder = "/mnt/data/new500/images"
    labels_folder = "/mnt/data/new500/labels"
    start_num = 1004  # 起始序号
    batch_rename(images_folder, labels_folder, start_num)

