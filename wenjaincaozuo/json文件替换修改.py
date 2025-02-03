import json

# 读取 JSON 文件
with open('/home/lirongyaoper/Documents/dataset.json', 'r') as file:
    data = json.load(file)

# 遍历 training 列表中的每个字典
for item in data['training']:
    # 检查 label 字段是否包含 "_0000.nii.gz"
    if '_0000.nii.gz' in item['label']:
        # 替换 "_0000.nii.gz" 为 ".nii.gz"
        item['label'] = item['label'].replace('_0000.nii.gz', '.nii.gz')

# 将修改后的数据写回 JSON 文件
with open('/home/lirongyaoper/Documents/dataset.json', 'w') as file:
    json.dump(data, file, indent=4)

print("修改完成！")