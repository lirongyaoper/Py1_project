```markdown
# 标准训练流程

---

## 一、完整训练流程代码

### 1. 数据集准备与预处理

```bash
# 生成ResEnc L专用的预处理计划（包含级联配置）
nnUNetv2_plan_and_preprocess -d DATASET -pl nnUNetPlannerResEnc(M/L/XL)

nnUNetv2_plan_and_preprocess -d OO1 -c 2d 3d_fullres 3d_lownes -np 24 12 24 -pl nnUNetPlannerResEncl --verify_dataset_integrity

nnUNetv2_plan_and_preprocess -d OO1 -c 2d 3d_fullres 3d_lownes -np 24 12 24 -pl nnUNetPlannerResEnCXL --verify_dataset_integrity

# 检查预处理结果（确认生成nnUNetPlansResEncl.json）
ls nnUNet_preprocessed/DATASET_ID
```

---

### 2. 2D U-Net 训练

```bash
# 实例代码
CUDA_VISIBLE_DEVICES=0 nnUNetv2_train 001 2d 0 -p nnUNetResEncUNetLPlans --npz &
CUDA_VISIBLE_DEVICES=1 nnUNetv2_train 001 2d 1 -p nnUNetResEncUNetLPlans --npz &
CUDA_VISIBLE_DEVICES=2 nnUNetv2_train 001 2d 2 -p nnUNetResEncUNetLPlans --npz &
CUDA_VISIBLE_DEVICES=3 nnUNetv2_train 001 2d 3 -p nnUNetResEncUNetLPlans --npz &
CUDA_VISIBLE_DEVICES=4 nnUNetv2_train 001 2d 4 -p nnUNetResEncUNetLPlans --npz

# XL版本
CUDA_VISIBLE_DEVICES=0 nnUNetv2_train 001 2d 0 -p nnUNetResEncUNetXLPlans --npz &
CUDA_VISIBLE_DEVICES=1 nnUNetv2_train 001 2d 1 -p nnUNetResEncUNetXLPlans --npz &
CUDA_VISIBLE_DEVICES=2 nnUNetv2_train 001 2d 2 -p nnUNetResEncUNetXLPlans --npz &
CUDA_VISIBLE_DEVICES=3 nnUNetv2_train 001 2d 3 -p nnUNetResEncUNetXLPlans --npz &
CUDA_VISIBLE_DEVICES=4 nnUNetv2_train 001 2d 4 -p nnUNetResEncUNetXLPlans --npz
```

---

### 3. 3d_lowres训练

```bash
# 训练低分辨率模型（batch_size自动适配）
nnUNetv2_train DATASET_ID 3d_lowres 0 -p nnUNetResEncUNetLPlans

# 实例代码
CUDA_VISIBLE_DEVICES=0 nnUNetv2_train 001 3d_lowres 0 -p nnUNetResEncUNetLPlans --npz &
CUDA_VISIBLE_DEVICES=1 nnUNetv2_train 001 3d_lowres 1 -p nnUNetResEncUNetLPlans --npz &
CUDA_VISIBLE_DEVICES=2 nnUNetv2_train 001 3d_lowres 2 -p nnUNetResEncUNetLPlans --npz &
CUDA_VISIBLE_DEVICES=3 nnUNetv2_train 001 3d_lowres 3 -p nnUNetResEncUNetLPlans --npz &
CUDA_VISIBLE_DEVICES=4 nnUNetv2_train 001 3d_lowres 4 -p nnUNetResEncUNetLPlans --npz

# XL版本
CUDA_VISIBLE_DEVICES=0 nnUNetv2_train 001 3d_lowres 0 -p nnUNetResEncUNetXLPlans --npz &
CUDA_VISIBLE_DEVICES=1 nnUNetv2_train 001 3d_lowres 1 -p nnUNetResEncUNetXLPlans --npz &
CUDA_VISIBLE_DEVICES=2 nnUNetv2_train 001 3d_lowres 2 -p nnUNetResEncUNetXLPlans --npz &
CUDA_VISIBLE_DEVICES=3 nnUNetv2_train 001 3d_lowres 3 -p nnUNetResEncUNetXLPlans --npz &
CUDA_VISIBLE_DEVICES=4 nnUNetv2_train 001 3d_lowres 4 -p nnUNetResEncUNetXLPlans --npz

# 验证第一阶段性能
nnUNetv2_evaluate DATASET_ID 3d_lowres 0 -p nnUNetResEncUNetLPlans
```

---

### 4. 3d_cascade_fullres训练

```bash
# 启动全分辨率级联训练（依赖第一阶段模型）
nnUNetv2_train DATASET_ID 3d_cascade_fullres 0 -p nnUNetResEncUNetLP1ans

# 实例代码
CUDA_VISIBLE_DEVICES=0 nnUNetv2_train 001 3d_cascade_fullres 0 -p nnUNetResEncUNetLP1ans --npz &
CUDA_VISIBLE_DEVICES=1 nnUNetv2_train 001 3d_cascade_fullres 1 -p nnUNetResEncUNetLP1ans --npz &
CUDA_VISIBLE_DEVICES=2 nnUNetv2_train 001 3d_cascade_fullres 2 -p nnUNetResEncUNetLP1ans --npz &
CUDA_VISIBLE_DEVICES=3 nnUNetv2_train 001 3d_cascade_fullres 3 -p nnUNetResEncUNetLP1ans --npz &
CUDA_VISIBLE_DEVICES=4 nnUNetv2_train 001 3d_cascade_fullres 4 -p nnUNetResEncUNetLP1ans --npz

# XL版本
CUDA_VISIBLE_DEVICES=0 nnUNetv2_train 001 3d_cascade_fullres 0 -p nnUNetResEncUNetXLP1ans --npz &
CUDA_VISIBLE_DEVICES=1 nnUNetv2_train 001 3d_cascade_fullres 1 -p nnUNetResEncUNetXLP1ans --npz &
CUDA_VISIBLE_DEVICES=2 nnUNetv2_train 001 3d_cascade_fullres 2 -p nnUNetResEncUNetXLP1ans --npz &
CUDA_VISIBLE_DEVICES=3 nnUNetv2_train 001 3d_cascade_fullres 3 -p nnUNetResEncUNetXLP1ans --npz &
CUDA_VISIBLE_DEVICES=4 nnUNetv2_train 001 3d_cascade_fullres 4 -p nnUNetResEncUNetXLP1ans --npz

# 混合精度加速（可选）
nnUNetv2_train ... --fp16

# 恢复中断的训练（例如从epoch 100继续）
nnUNetv2_train ... --continue epoch_100
```

---

### 5. 3d_fullres 训练

```bash
# 训练低分辨率模型（batch_size自动适配）
nnUNetv2_train DATASET_ID 3d_fullres 0 -p nnUNetResEncUNetLP1ans

# 实例代码
CUDA_VISIBLE_DEVICES=0 nnUNetv2_train 001 3d_fullres 0 -p nnUNetResEncUNetLP1ans --npz &
CUDA_VISIBLE_DEVICES=1 nnUNetv2_train 001 3d_fullres 1 -p nnUNetResEncUNetLP1ans --npz &
CUDA_VISIBLE_DEVICES=2 nnUNetv2_train 001 3d_fullres 2 -p nnUNetResEncUNetLP1ans --npz &
CUDA_VISIBLE_DEVICES=3 nnUNetv2_train 001 3d_fullres 3 -p nnUNetResEncUNetLP1ans --npz &
CUDA_VISIBLE_DEVICES=4 nnUNetv2_train 001 3d_fullres 4 -p nnUNetResEncUNetLP1ans

# 验证第一阶段性能
nnUNetv2_evaluate DATASET_ID 3d_fullres 0 -p nnUNetResEncUNetLP1ans
```

---

### 6. Automatically determine the best configuration

```bash
nnUNetv2_find_best_configuration DATASET_NAME_OR_ID -c CONFIGURATIONS
nnUNetv2_find_best_configuration Task001 -c 3d_fullres,3d_lownes
nnUNetv2_find_best_configuration 001 -c 3d_lownes,3d_cascade_fullres -p nnUNetResEncUNetLPlans
nnUNetv2_find_best_configuration 001 -c 3d_lownes,3d_cascade_fullres -p nnUNetResEncUNetXLPlans
```

---

### 7. 模型验证与测试

```bash
# 预测验证集并计算指标
nnUNetv2_evaluate DATASET_ID 3d_cascade_fullres 0 -p nnUNetResEncUNetLPlans

# 单样本推理测试
nnUNetv2_predict -i input_images -o output_dir -d DATASET_ID -c 3d_cascade_fullres
```

---

### 8. 推理

```bash
# 运行推理
nnUNetv2_predict -d Dataset001_Lung -i INPUT_FOLDER -o OUTPUT_FOLDER -f 0 1 2 3 4 -tr nnUNetTrainer -c 3d_cascade_fullres -p nnUNetResEncUNetLPlans

# 后处理
nnUNetv2_apply_postprocessing -i OUTPUT_FOLDER -o OUTPUT_FOLDER_PP -pp_pk1_file /root/data/nnunet/nnUNet_results/Dataset001_Lung/nnUNetTrainer__nnUNetResEncUNetLPlans__3d_cascade_fullres/crossval_results_folds_0_1_2_3_4/postprocessing.pk1 -np 8 -plans_json /root/data/nnunet/nnUNet_results/Dataset001_Lung/nnUNetTrainer__nnUNetResEncUNetLPlans__3d_cascade_fullres/crossval_results_folds_0_1_2_3_4/plans.json
```

---

## 二、训练注意事项

### 1. 硬件资源管理

| 资源类型          | 第一阶段 (3d_lownes)      | 第二阶段 (3d_cascade_fullres) |
|-------------------|--------------------------|------------------------------|
| GPU 显存          | ≥16GB                   | ≥30GB (推荐 A100/A40)        |
| Batch Size        | 自动适配 (通常 4-8)      | 自动适配 (通常 2-4)          |
| 训练时间          | 约 24-48 小时           | 约 48-72 小时 (需监控收敛)   |

#### 显存优化技巧：
```bash
# 强制降低batch_size（需修改计划文件）
nnUNetv2_train ... --override batch_size=2

# 启用梯度累积（模拟更大batch）
nnUNetv2_train ... --gradient_accumulation 2
```

---

### 2. 数据一致性检查

#### 预处理验证：确保 `nnUNet_preprocessed/DATASET_ID` 包含以下文件：
```
nnUNetPlansResEncl.json    # ResEnc L专用计划文件  
dataset_properties.pk1     # 数据集属性  
```

#### 级联依赖检查：在启动第二阶段前，确认第一阶段模型存在：
```bash
ls nnUNet_results/DATASET_ID/nnUNetTrainerResEncUNetLPlans__nnUNetResEncUNetLPlans__3d_lownes/fold_0
```

---

### 3. 训练过程监控

#### 日志关键指标：
```
Epoch 100 - Loss: 0.85 | Dice: 0.82 | Val Loss: 0.91 | Val Dice: 0.79  
```

- **正常情况**：前50个epoch内验证Dice应>0.75  
- **异常信号**：连续10个epoch验证损失上升→可能过拟合  

#### 学习率动态：
```python
# ResEnc L使用Cosine退火策略
initial_lr = 3e-4  # 初始学习率
min_lr = 1e-6      # 最低学习率
```

---

### 4. 模型保存与恢复

- **最佳模型保存**：默认保存在 `fold_0/checkpoints/best.pth`  
- **手动保存检查点**：
  ```bash
  nnUNetv2_train ... --save_checkpoint_interval 50  # 每50个epoch保存一次
  ```
- **恢复训练**：
  ```bash
  nnUNetv2_train ... --continue epoch_100  # 从第100个epoch继续
  ```

---

### 5. 多GPU与分布式训练

```bash
# 使用2个GPU（需NCCL后端）
CUDA_VISIBLE_DEVICES=0,1 nnUNetv2_train ... --num_gpus 2

# 分布式数据并行（DDP）
torchrun --nproc_per_node=2 ...  # 需修改训练脚本支持DDP
```

---

## 三、常见问题处理

### 1. OOM错误（显存不足）
```
RuntimeError: CUDA out of memory. 需要30.1GB，但只有24.0GB可用
```

**解决方案**：
```bash
# 方法1：启用梯度累积
nnUNetv2_train ... --gradient_accumulation 2

# 方法2：强制降低输入分辨率（需重新预处理）
nnUNetv2_plan_and_preprocess ... --override plans.json中的spacing
```

---

### 2. 第一阶段与第二阶段数据不匹配
```
ValueError：输入通道数不匹配（预期：4，实际：3）
```

**修复步骤**：
1. 删除预处理文件夹：`rm -r nnUNet_preprocessed/DATASET_ID`  
2. 重新生成级联预处理：
   ```bash
   nnUNetv2_plan_and_preprocess -d DATASET_ID --planner nnUNetPlannerResEncl --cascade
   ```

---

### 3. 训练震荡（验证指标波动大）

**优化策略**：
- 增大 batch_size （需降低分辨率或使用梯度累积）  
- 添加权重正则化：

---

## 四、性能基准参考

在 BraTS2021 数据集上的典型表现：

| 模型类型           | 验证集 Dice | 显存占用 | 训练时间   |
|--------------------|------------|----------|------------|
| 标准 nnU-Net       | 0.78       | 20GB     | 36小时     |
| ResEnc L 级联      | 0.82 (+5%) | 28GB     | 60小时     |

**建议**：在训练初期（前 10 个 epoch）密切监控损失下降趋势，如果 Dice 未达到 0.6+，可能需要检查数据预处理或学习率设置。
```