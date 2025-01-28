json_dict = {}
"""
name: 数据集名字
dexcription: 对数据集的描述
modality: 模态，0表示CT数据，1表示MR数据。nnU-Net会根据不同模态进行不同的预处理（nnunet-v2版本改为channel_names）
labels: label中，不同的数值代表的类别(v1版本和v2版本的键值对刚好是反过来的)
file_ending: nnunet v2新加的
numTraining: 训练集数量
numTest: 测试集数量
training: 训练集的image 和 label 地址对
test: 只包含测试集的image. 这里跟Training不一样
"""
json_dict['name'] = "Lung"
json_dict['description'] = "Lung and cancer segmentation"
json_dict['tensorImageSize'] = "4D"
json_dict['reference'] = "The Cancer Imaging Archive"
json_dict['licence'] = "CC-BY-SA 4.0"
json_dict['release'] = "0.0"

json_dict['channel_names'] = {
    "0": "CT",
}
json_dict['labels'] = {
    "0":"background",
    "1":"pulmonary vein",
    "2":"bronchus",
    "3":"pulmonary artery"
}
json_dict['numTraining'] = len(202)  # 应该是210例
json_dict['file_ending'] = ".nii.gz"
json_dict['numTest'] = 0
json_dict['training'] = [{'image': "./imagesTr/%s.nii.gz" % i, "label": "./labelsTr/%s.nii.gz" % i} for i in 202]
# json_dict['test'] = []
save_json(json_dict, os.path.join(out, "dataset.json"))