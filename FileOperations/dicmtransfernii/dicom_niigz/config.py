#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DICOM到NIfTI转换工具配置文件
用于配置转换参数和路径设置
"""

import os
from pathlib import Path

class Config:
    """配置类"""
    
    # 默认路径配置
    DEFAULT_SOURCE_PATH = "/home/lirongyaoper/Downloads/3dCT"
    DEFAULT_DEST_DIR = "/home/lirongyaoper/Downloads/imageniigz"
    
    # dcm2niix转换参数
    DCM2NIIX_PARAMS = {
        'output_format': 'nii.gz',  # 输出格式
        'compress': True,           # 是否压缩
        'bids_format': False,       # 是否使用BIDS格式
        'anonymize': False,         # 是否匿名化
        'crop': False,              # 是否裁剪
        'merge_2d': True,           # 是否合并2D切片
    }
    
    # 日志配置
    LOG_CONFIG = {
        'level': 'INFO',            # DEBUG, INFO, WARNING, ERROR
        'file_name': 'dicom_conversion.log',
        'max_file_size': 10 * 1024 * 1024,  # 10MB
        'backup_count': 5,
    }
    
    # 转换配置
    CONVERSION_CONFIG = {
        'timeout': 300,             # 单个文件夹转换超时时间（秒）
        'parallel_workers': 1,      # 并行工作进程数（暂未实现）
        'skip_existing': True,      # 是否跳过已存在的输出文件
        'verify_dicom': True,       # 是否验证DICOM文件
    }
    
    # nnU-Net特定配置
    NNUNET_CONFIG = {
        'naming_convention': '{case_id}_0000.nii.gz',  # nnU-Net命名规范
        'generate_json': True,      # 是否生成JSON元数据文件
        'modality_suffix': '_0000', # 模态后缀
    }
    
    @classmethod
    def get_dcm2niix_command_args(cls) -> list:
        """
        生成dcm2niix命令参数
        
        Returns:
            list: 命令参数列表
        """
        args = []
        
        if cls.DCM2NIIX_PARAMS['compress']:
            args.extend(['-z', 'y'])
        
        if cls.DCM2NIIX_PARAMS['bids_format']:
            args.extend(['-b', 'y'])
        
        if cls.DCM2NIIX_PARAMS['anonymize']:
            args.extend(['-ba', 'y'])
            
        if cls.DCM2NIIX_PARAMS['crop']:
            args.extend(['-x', 'y'])
            
        if not cls.DCM2NIIX_PARAMS['merge_2d']:
            args.extend(['-m', 'n'])
            
        return args
    
    @classmethod
    def validate_paths(cls, source_path: str = None, dest_dir: str = None):
        """
        验证和设置路径
        
        Args:
            source_path: 源路径
            dest_dir: 目标路径
            
        Returns:
            tuple: (验证后的源路径, 验证后的目标路径)
        """
        if source_path is None:
            source_path = cls.DEFAULT_SOURCE_PATH
            
        if dest_dir is None:
            dest_dir = cls.DEFAULT_DEST_DIR
            
        # 将相对路径转换为绝对路径
        source_path = os.path.abspath(source_path)
        dest_dir = os.path.abspath(dest_dir)
        
        return source_path, dest_dir


# 环境特定配置
class EnvironmentConfig:
    """环境特定配置"""
    
    @staticmethod
    def get_conda_env_info():
        """获取当前conda环境信息"""
        conda_env = os.environ.get('CONDA_DEFAULT_ENV', 'unknown')
        conda_prefix = os.environ.get('CONDA_PREFIX', 'unknown')
        
        return {
            'env_name': conda_env,
            'env_path': conda_prefix,
            'is_nnunet': 'nnunet' in conda_env.lower() if conda_env != 'unknown' else False
        }
    
    @staticmethod
    def check_nnunet_environment():
        """检查是否在nnU-Net环境中"""
        env_info = EnvironmentConfig.get_conda_env_info()
        
        if not env_info['is_nnunet']:
            print(f"警告: 当前环境 '{env_info['env_name']}' 可能不是nnU-Net环境")
            print("建议使用: conda activate nnunet")
            
        return env_info['is_nnunet']


# 示例配置 - 可根据需要修改
EXAMPLE_CONFIGS = {
    'lung_ct': {
        'source_path': '/data/lung_ct/dicom',
        'dest_dir': '/data/lung_ct/nifti',
        'description': '肺部CT数据转换配置'
    },
    'brain_mri': {
        'source_path': '/data/brain_mri/dicom', 
        'dest_dir': '/data/brain_mri/nifti',
        'description': '脑部MRI数据转换配置'
    },
    'cardiac_ct': {
        'source_path': '/data/cardiac/dicom',
        'dest_dir': '/data/cardiac/nifti', 
        'description': '心脏CT数据转换配置'
    }
}
