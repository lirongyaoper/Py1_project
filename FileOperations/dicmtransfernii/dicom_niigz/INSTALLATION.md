# DICOM到NIfTI转换工具安装指南

## 系统要求

- **操作系统**: Linux (推荐 Ubuntu 18.04+), macOS, Windows (WSL2)
- **Python版本**: 3.7或更高版本
- **内存**: 至少4GB RAM（推荐8GB+）
- **存储空间**: 确保有足够空间存储转换后的NIfTI文件

## 环境设置

### 1. 安装Conda

如果尚未安装Conda，请先安装Miniconda或Anaconda：

```bash
# 下载Miniconda (Linux)
wget https://repo.anaconda.com/miniconda/Miniconda3-latest-Linux-x86_64.sh
bash Miniconda3-latest-Linux-x86_64.sh

# 重新加载bashrc或重启终端
source ~/.bashrc
```

### 2. 创建并激活nnU-Net环境

```bash
# 创建nnunet环境
conda create -n nnunet python=3.8

# 激活环境
conda activate nnunet
```

### 3. 安装必要依赖

#### 安装dcm2niix工具

```bash
# 方法1: 使用conda安装 (推荐)
conda install -c conda-forge dcm2niix

# 方法2: 使用apt安装 (Ubuntu/Debian)
sudo apt-get update
sudo apt-get install dcm2niix

# 方法3: 从源码编译
git clone https://github.com/rordenlab/dcm2niix.git
cd dcm2niix
mkdir build && cd build
cmake ..
make
sudo make install
```

#### 安装nnU-Net (可选)

如果需要使用nnU-Net进行深度学习：

```bash
# 安装PyTorch (根据您的CUDA版本选择)
conda install pytorch torchvision torchaudio pytorch-cuda=11.8 -c pytorch -c nvidia

# 安装nnU-Net
pip install nnunet
```

### 4. 验证安装

```bash
# 验证dcm2niix
dcm2niix --version

# 验证Python环境
python --version

# 验证nnU-Net (如果已安装)
nnUNet_plan_and_preprocess -h
```

## 工具安装

### 下载转换工具

```bash
# 克隆或下载项目文件
git clone <your-repository>
cd <project-directory>/FileOperations/dicmtransfernii/

# 或手动下载以下文件:
# - dicom_niigz.py (简化版本)
# - dicom_niigz_optimized.py (完整版本)
# - config.py (配置文件)
# - example_usage.py (使用示例)
```

### 设置权限

```bash
# 给脚本添加执行权限
chmod +x dicom_niigz.py
chmod +x dicom_niigz_optimized.py
chmod +x example_usage.py
```

## 配置设置

### 1. 环境变量配置 (可选)

```bash
# 添加到 ~/.bashrc 或 ~/.zshrc
export NNUNET_ENV="nnunet"
export DCM2NIIX_PATH="/usr/local/bin/dcm2niix"

# 重新加载配置
source ~/.bashrc
```

### 2. 路径配置

编辑 `config.py` 文件，设置您的默认路径：

```python
# 修改默认路径
DEFAULT_SOURCE_PATH = "/your/dicom/data/path"
DEFAULT_DEST_DIR = "/your/nifti/output/path"
```

### 3. nnU-Net环境配置 (如果使用nnU-Net)

```bash
# 设置nnU-Net环境变量
export nnUNet_raw_data_base="/path/to/nnunet/raw"
export nnUNet_preprocessed="/path/to/nnunet/preprocessed"
export RESULTS_FOLDER="/path/to/nnunet/results"
```

## 快速测试

### 1. 基本功能测试

```bash
# 激活环境
conda activate nnunet

# 测试脚本（使用测试数据）
python dicom_niigz.py --help

# 运行示例
python example_usage.py
```

### 2. 小规模测试

```bash
# 创建测试目录结构
mkdir -p test_data/dicom/patient001
mkdir -p test_data/output

# 如果有测试DICOM文件，放入test_data/dicom/patient001/
# 然后运行转换
python dicom_niigz.py test_data/dicom test_data/output
```

## 故障排除

### 常见问题及解决方案

#### 1. dcm2niix命令未找到

```bash
# 检查安装
which dcm2niix

# 重新安装
conda install -c conda-forge dcm2niix --force-reinstall
```

#### 2. 权限错误

```bash
# 检查目录权限
ls -la /path/to/your/data

# 修改权限
sudo chown -R $USER:$USER /path/to/your/data
chmod -R 755 /path/to/your/data
```

#### 3. 内存不足

```bash
# 监控内存使用
htop

# 清理系统缓存
sudo sh -c 'echo 3 > /proc/sys/vm/drop_caches'
```

#### 4. DICOM文件格式问题

```bash
# 检查DICOM文件
file /path/to/dicom/file

# 使用dcm2niix直接测试单个文件夹
dcm2niix -o /tmp/test -z y /path/to/dicom/folder
```

### 调试模式

```bash
# 启用详细日志
python dicom_niigz_optimized.py --log-level DEBUG

# 检查日志文件
tail -f dicom_conversion.log
```

## 性能优化

### 1. 存储优化

```bash
# 使用SSD存储以提高I/O性能
# 确保有足够的临时空间
df -h /tmp
```

### 2. 系统资源

```bash
# 监控系统资源使用
iostat -x 1
iotop
```

### 3. 并行处理 (未来版本)

目前版本为串行处理，未来版本将支持并行转换以提高效率。

## 升级和维护

### 更新工具

```bash
# 更新dcm2niix
conda update dcm2niix

# 更新nnU-Net
pip install --upgrade nnunet
```

### 清理旧文件

```bash
# 清理转换日志
rm -f dicom_conversion.log*

# 清理临时文件
rm -rf /tmp/dcm2niix*
```

## 支持和帮助

### 获取帮助

```bash
# 查看脚本帮助
python dicom_niigz.py --help
python dicom_niigz_optimized.py --help

# 查看dcm2niix帮助
dcm2niix -h
```

### 报告问题

如果遇到问题，请收集以下信息：

1. 操作系统版本: `uname -a`
2. Python版本: `python --version`
3. dcm2niix版本: `dcm2niix --version`
4. 错误日志: `cat dicom_conversion.log`
5. 示例DICOM文件信息

### 有用的命令

```bash
# 检查系统信息
uname -a
lsb_release -a

# 检查磁盘空间
df -h

# 检查内存使用
free -h

# 检查环境变量
env | grep -i nnunet
conda env list

# 测试DICOM文件
dcm2niix -h
file your_dicom_file.dcm
```

---

**注意**: 安装完成后，建议先在小规模测试数据上验证工具的正确性，然后再处理大批量的生产数据。
