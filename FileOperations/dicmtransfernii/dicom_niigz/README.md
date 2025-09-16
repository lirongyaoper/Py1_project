# DICOM到NIfTI批量转换工具

## 概述

这是一个专为医学影像研究设计的DICOM到NIfTI格式批量转换工具，特别适用于nnU-Net等深度学习框架的数据预处理工作流。

## 功能特性

- 🔄 **批量转换**: 自动遍历源目录下的所有DICOM文件夹
- 📁 **目录结构保持**: 在目标目录中保持与源目录相同的文件夹结构
- 📊 **实时进度显示**: 显示转换进度和完成百分比
- 🗜️ **自动压缩**: 生成压缩的.nii.gz文件，节省存储空间
- 🔧 **nnU-Net兼容**: 生成的NIfTI文件可直接用于nnU-Net训练

## 环境要求

### Python环境
- **推荐**: Conda环境下的nnunet
- **Python版本**: 3.7+

### 系统依赖
- **dcm2niix**: DICOM到NIfTI转换工具
  ```bash
  # Ubuntu/Debian安装
  sudo apt-get install dcm2niix
  
  # 或使用conda安装
  conda install -c conda-forge dcm2niix
  
  # macOS使用Homebrew
  brew install dcm2niix
  ```

### Python包依赖
```bash
# 标准库，无需额外安装
import os
```

## 使用方法

### 1. 环境激活
```bash
# 激活nnunet conda环境
conda activate nnunet
```

### 2. 配置路径
编辑脚本中的路径配置：
```python
source_path = "/path/to/your/dicom/folders"    # DICOM文件夹路径
dest_dir = "/path/to/output/nifti/folders"     # NIfTI输出路径
```

### 3. 运行转换
```bash
python dicom_niigz.py
```

## 目录结构示例

### 输入结构 (DICOM)
```
/source_path/
├── patient_001/
│   ├── IM-0001-0001.dcm
│   ├── IM-0001-0002.dcm
│   └── ...
├── patient_002/
│   ├── IM-0002-0001.dcm
│   └── ...
└── patient_003/
    └── ...
```

### 输出结构 (NIfTI)
```
/dest_dir/
├── patient_001/
│   ├── converted_image.nii.gz
│   └── converted_image.json  # 元数据文件
├── patient_002/
│   ├── converted_image.nii.gz
│   └── converted_image.json
└── patient_003/
    └── ...
```

## nnU-Net集成指南

### 数据组织
转换后的NIfTI文件可直接用于nnU-Net：

1. **训练数据**: 将转换后的图像复制到nnU-Net的imagesTr文件夹
2. **标注数据**: 如果有分割标注，也需要相应的NIfTI格式
3. **命名规范**: 遵循nnU-Net的命名约定（例如：case_001_0000.nii.gz）

### 典型工作流
```bash
# 1. 转换DICOM到NIfTI
python dicom_niigz.py

# 2. 重命名文件以符合nnU-Net规范
# (可能需要额外的重命名脚本)

# 3. 运行nnU-Net预处理
nnUNet_plan_and_preprocess -t TASK_ID
```

## 转换参数说明

脚本使用的dcm2niix命令参数：
- `-o {output_folder}/`: 指定输出目录
- `-z y`: 启用gzip压缩，生成.nii.gz文件
- `{input_folder}`: 包含DICOM文件的源文件夹

## 故障排除

### 常见问题

1. **dcm2niix命令未找到**
   ```bash
   # 检查dcm2niix是否已安装
   which dcm2niix
   # 或
   dcm2niix --version
   ```

2. **权限错误**
   - 确保对源目录有读取权限
   - 确保对目标目录有写入权限

3. **内存不足**
   - 大型DICOM序列可能需要大量内存
   - 考虑分批处理或增加系统内存

4. **文件格式问题**
   - 确保源文件夹包含有效的DICOM文件
   - 检查DICOM文件是否损坏

### 日志检查
脚本会输出：
- 当前处理的文件夹路径
- 转换进度信息
- dcm2niix的详细输出（如果有错误）

## 性能优化建议

1. **SSD存储**: 使用SSD存储以提高I/O性能
2. **并行处理**: 对于大量数据，考虑修改脚本支持多线程
3. **内存管理**: 监控内存使用，避免内存不足
4. **批量大小**: 根据系统性能调整批量处理大小

## 医学影像注意事项

1. **患者隐私**: 确保遵守HIPAA等医疗数据隐私法规
2. **数据完整性**: 转换前后验证图像数据的完整性
3. **元数据保持**: dcm2niix会保留重要的医学影像元数据
4. **坐标系统**: 注意DICOM和NIfTI之间的坐标系统差异

## 版本信息

- **脚本版本**: 1.0
- **兼容的dcm2niix版本**: v1.0.20190902+
- **测试环境**: Ubuntu 20.04, conda nnunet环境

## 许可证

请确保遵守dcm2niix和相关医学影像处理工具的许可证要求。

---

**注意**: 本工具主要用于研究目的，临床使用前请进行充分验证。
