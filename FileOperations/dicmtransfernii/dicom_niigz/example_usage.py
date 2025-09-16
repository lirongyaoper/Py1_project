#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DICOM到NIfTI转换工具使用示例
展示不同的使用场景和最佳实践
"""

import sys
import os
from pathlib import Path

# 添加当前目录到Python路径
sys.path.append(str(Path(__file__).parent))

from dicom_niigz_optimized import DicomToNiftiConverter
from config import Config, EnvironmentConfig, EXAMPLE_CONFIGS


def example_basic_usage():
    """示例1: 基本使用方法"""
    print("=== 示例1: 基本使用方法 ===")
    
    # 创建转换器实例
    converter = DicomToNiftiConverter(log_level="INFO")
    
    # 使用默认配置进行转换
    source_path = "/mnt/data/new500/100/image100"
    dest_dir = "/mnt/data/new500/100/imageniigz/"
    
    # 执行转换
    result = converter.convert_batch(source_path, dest_dir)
    
    print(f"转换结果: {result}")
    return result


def example_custom_config():
    """示例2: 使用自定义配置"""
    print("=== 示例2: 使用自定义配置 ===")
    
    # 检查nnU-Net环境
    EnvironmentConfig.check_nnunet_environment()
    
    # 使用肺部CT配置
    lung_config = EXAMPLE_CONFIGS['lung_ct']
    
    converter = DicomToNiftiConverter(log_level="DEBUG")
    
    print(f"使用配置: {lung_config['description']}")
    print(f"源路径: {lung_config['source_path']}")
    print(f"目标路径: {lung_config['dest_dir']}")
    
    # 如果路径存在，执行转换
    if Path(lung_config['source_path']).exists():
        result = converter.convert_batch(
            lung_config['source_path'], 
            lung_config['dest_dir']
        )
        print(f"转换结果: {result}")
    else:
        print(f"路径不存在，跳过转换: {lung_config['source_path']}")


def example_command_line_usage():
    """示例3: 命令行使用方法"""
    print("=== 示例3: 命令行使用方法 ===")
    
    print("命令行使用示例:")
    print("python dicom_niigz_optimized.py /path/to/dicom /path/to/output")
    print()
    print("或使用默认路径:")
    print("python dicom_niigz_optimized.py")
    
    # 模拟命令行参数
    if len(sys.argv) >= 3:
        source_path = sys.argv[1]
        dest_dir = sys.argv[2]
        
        converter = DicomToNiftiConverter()
        result = converter.convert_batch(source_path, dest_dir)
        print(f"命令行转换结果: {result}")


def example_batch_processing():
    """示例4: 批量处理多个数据集"""
    print("=== 示例4: 批量处理多个数据集 ===")
    
    converter = DicomToNiftiConverter(log_level="INFO")
    
    # 定义多个数据集
    datasets = [
        {
            'name': '数据集1',
            'source': '/data/dataset1/dicom',
            'dest': '/data/dataset1/nifti'
        },
        {
            'name': '数据集2', 
            'source': '/data/dataset2/dicom',
            'dest': '/data/dataset2/nifti'
        }
    ]
    
    total_results = {
        'total_success': 0,
        'total_failed': 0,
        'total_time': 0
    }
    
    for dataset in datasets:
        print(f"\n处理 {dataset['name']}...")
        
        if Path(dataset['source']).exists():
            result = converter.convert_batch(dataset['source'], dataset['dest'])
            
            total_results['total_success'] += result.get('success', 0)
            total_results['total_failed'] += result.get('failed', 0)
            total_results['total_time'] += result.get('time', 0)
            
            print(f"{dataset['name']} 完成: 成功{result.get('success', 0)}, 失败{result.get('failed', 0)}")
        else:
            print(f"{dataset['name']} 路径不存在，跳过: {dataset['source']}")
    
    print(f"\n=== 批量处理总结 ===")
    print(f"总成功: {total_results['total_success']}")
    print(f"总失败: {total_results['total_failed']}")
    print(f"总耗时: {total_results['total_time']:.2f}秒")


def example_nnunet_integration():
    """示例5: nnU-Net集成示例"""
    print("=== 示例5: nnU-Net集成示例 ===")
    
    # 检查环境
    env_info = EnvironmentConfig.get_conda_env_info()
    print(f"当前环境: {env_info}")
    
    if not env_info['is_nnunet']:
        print("警告: 当前不在nnU-Net环境中")
        print("请运行: conda activate nnunet")
        return
    
    # nnU-Net典型工作流
    print("\nnnU-Net典型工作流:")
    print("1. DICOM转换为NIfTI")
    print("2. 重命名文件符合nnU-Net规范") 
    print("3. 组织数据到nnU-Net目录结构")
    print("4. 运行nnU-Net预处理")
    
    # 转换示例
    converter = DicomToNiftiConverter()
    
    # 假设的nnU-Net任务目录
    nnunet_raw = os.environ.get('nnUNet_raw_data_base', '/data/nnunet/raw')
    task_name = "Task001_ExampleTask"
    task_dir = Path(nnunet_raw) / task_name
    
    print(f"\nnnU-Net任务目录: {task_dir}")
    print("转换后需要手动组织文件到以下结构:")
    print(f"{task_dir}/")
    print("├── imagesTr/")
    print("│   ├── case_001_0000.nii.gz")
    print("│   └── case_002_0000.nii.gz")
    print("├── labelsTr/") 
    print("│   ├── case_001.nii.gz")
    print("│   └── case_002.nii.gz")
    print("└── dataset.json")


def example_error_handling():
    """示例6: 错误处理和调试"""
    print("=== 示例6: 错误处理和调试 ===")
    
    converter = DicomToNiftiConverter(log_level="DEBUG")
    
    # 测试不存在的路径
    print("测试不存在的路径...")
    try:
        result = converter.convert_batch("/nonexistent/path", "/tmp/output")
    except Exception as e:
        print(f"捕获异常: {e}")
    
    # 测试权限问题
    print("\n测试权限问题...")
    try:
        result = converter.convert_batch("/tmp", "/root/no_permission")
    except Exception as e:
        print(f"捕获异常: {e}")
    
    print("\n调试技巧:")
    print("1. 使用DEBUG日志级别查看详细信息")
    print("2. 检查dicom_conversion.log文件")
    print("3. 验证dcm2niix工具是否正确安装")
    print("4. 确保源目录包含有效的DICOM文件")


def main():
    """主函数 - 运行所有示例"""
    print("DICOM到NIfTI转换工具使用示例\n")
    
    examples = [
        ("基本使用方法", example_basic_usage),
        ("自定义配置", example_custom_config),
        ("命令行使用", example_command_line_usage),
        ("批量处理", example_batch_processing),
        ("nnU-Net集成", example_nnunet_integration),
        ("错误处理", example_error_handling),
    ]
    
    print("可用示例:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"{i}. {name}")
    
    print("\n选择要运行的示例 (1-6)，或按Enter运行所有示例:")
    
    try:
        choice = input().strip()
        
        if choice == "":
            # 运行所有示例
            for name, func in examples:
                print(f"\n{'='*50}")
                print(f"运行示例: {name}")
                print('='*50)
                try:
                    func()
                except Exception as e:
                    print(f"示例执行失败: {e}")
        else:
            # 运行指定示例
            choice_num = int(choice)
            if 1 <= choice_num <= len(examples):
                name, func = examples[choice_num - 1]
                print(f"\n运行示例: {name}")
                func()
            else:
                print("无效选择")
                
    except (ValueError, KeyboardInterrupt):
        print("\n程序退出")


if __name__ == "__main__":
    main()
