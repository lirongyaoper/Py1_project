from monai.apps.nnunet import nnUNetV2Runner



basename ="/home/lirongyaoper/Softwares/input.yaml"
# 创建 nnUNetV2Runner 实例
runner = nnUNetV2Runner(input_config =basename)

# 调用 convert_dataset 方法
runner.convert_dataset()