import os
import json


def create_dataset_json(base_dir):
    # 定义文件夹路径
    images_dir = os.path.join(base_dir, "imagesTr")
    labels_dir = os.path.join(base_dir, "labelsTr")

    # 获取 imagesTr 和 labelsTr 文件夹中的文件列表
    if not os.path.isdir(images_dir) or not os.path.isdir(labels_dir):
        print("指定的 imagesTr 或 labelsTr 文件夹不存在。")
        return

    images = os.listdir(images_dir)
    labels = os.listdir(labels_dir)

    # 创建 training 列表
    training_data = []

    for image_file in images:
        # 确保我们只处理 .nii.gz 文件
        if image_file.endswith('.nii.gz'):
            # 去掉 _0000 后缀，生成 label_file 名称
            label_file = image_file.replace('_0000.nii.gz', '.nii.gz')  # 去掉 _0000 后缀

            if label_file in labels:
                training_data.append({
                    "image": f"./imagesTr/{image_file}",
                    "label": f"./labelsTr/{label_file}"
                })

    # 构建数据集字典
    dataset_info = {
        "name": "Lung",
        "description": "Lung and cancer segmentation",
        "tensorImageSize": "4D",
        "reference": "The Cancer Imaging Archive",
        "licence": "CC-BY-SA 4.0",
        "release": "0.0",
        "channel_names": {
            0: "CT"
        },
        "labels": {
            "background": 0,
            "pulmonary artery": 1,
            "bronchus": 2,
            "pulmonary vein": 3
        },
        "numTraining": len(training_data),
        "file_ending": ".nii.gz",
        "numTest": 0,
        "testing": [],
        "training": training_data
    }

    # 保存为 dataset.json 文件
    with open(os.path.join(base_dir, "dataset.json"), "w") as json_file:
        json.dump(dataset_info, json_file, indent=4)

    print("dataset.json 文件已成功创建。")


# 使用示例
base_directory = "/mnt/data/lungCT/databasebak_center/1522"  # 替换为包含 imagesTr 和 labelsTr 的目录路径
create_dataset_json(base_directory)
