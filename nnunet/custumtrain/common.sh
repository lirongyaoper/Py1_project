# 导入自定义训练器模块
import sys
sys.path.append('/path/to/custom_trainer.py')

# 使用自定义训练器进行训练
nnUNetv2_train DATASET_NAME CONFIGURATION FOLD -trainer_class_name CustomTrainer
