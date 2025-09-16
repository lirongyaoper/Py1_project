#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DICOM到NIfTI批量转换工具 - 简化版本
适用于nnU-Net等医学影像深度学习框架的数据预处理

作者: 医学影像处理工具
版本: 1.1 (改进版)
环境: conda nnunet
"""

import os
import sys
import time
from pathlib import Path


def check_environment():
    """检查运行环境"""
    # 检查conda环境
    conda_env = os.environ.get('CONDA_DEFAULT_ENV', 'unknown')
    if 'nnunet' not in conda_env.lower():
        print(f"警告: 当前环境 '{conda_env}' 可能不是nnU-Net环境")
        print("建议使用: conda activate nnunet")
    
    # 检查dcm2niix工具
    if os.system('which dcm2niix > /dev/null 2>&1') != 0:
        print("错误: dcm2niix工具未找到")
        print("请安装: conda install -c conda-forge dcm2niix")
        return False
    
    return True


def dcm_niigz(source_path, dest_dir):
    """
    DICOM到NIfTI批量转换函数
    
    Args:
        source_path (str): 源DICOM目录路径
        dest_dir (str): 目标NIfTI目录路径
    
    Returns:
        dict: 转换结果统计
    """
    start_time = time.time()
    
    # 验证源路径
    if not os.path.exists(source_path):
        print(f"错误: 源目录不存在 - {source_path}")
        return {"success": 0, "failed": 0, "total": 0}
    
    if not os.path.isdir(source_path):
        print(f"错误: 源路径不是目录 - {source_path}")
        return {"success": 0, "failed": 0, "total": 0}
    
    # 创建目标目录
    try:
        if not os.path.exists(dest_dir):
            os.makedirs(dest_dir)
            print(f"已创建目标目录: {dest_dir}")
    except PermissionError:
        print(f"错误: 无法创建目标目录（权限不足） - {dest_dir}")
        return {"success": 0, "failed": 0, "total": 0}
    
    # 获取DICOM文件夹列表
    try:
        folder_list = [item for item in os.listdir(source_path) 
                      if os.path.isdir(os.path.join(source_path, item))]
    except PermissionError:
        print(f"错误: 无法读取源目录（权限不足） - {source_path}")
        return {"success": 0, "failed": 0, "total": 0}
    
    if not folder_list:
        print(f"警告: 在源目录中未找到任何子文件夹 - {source_path}")
        return {"success": 0, "failed": 0, "total": 0}
    
    print(f"找到 {len(folder_list)} 个DICOM文件夹")
    print(f"源目录: {source_path}")
    print(f"目标目录: {dest_dir}")
    print("-" * 50)
    
    # 开始批量转换
    successful = 0
    failed = 0
    
    for i, folder_name in enumerate(folder_list):
        try:
            # 创建目标文件夹路径
            folder_path = os.path.join(dest_dir, folder_name)
            source_folder_path = os.path.join(source_path, folder_name)
            
            # 检查是否已存在（可选：跳过已存在的）
            if os.path.exists(folder_path):
                print(f"跳过已存在的文件夹: {folder_name}")
                continue
            
            # 创建目标文件夹
            os.makedirs(folder_path, exist_ok=True)
            
            print(f"[{i+1}/{len(folder_list)}] 正在转换: {folder_name}")
            print(f"  源路径: {source_folder_path}")
            
            # 执行dcm2niix转换
            cmd = f'dcm2niix -o "{folder_path}/" -z y "{source_folder_path}"'
            result = os.system(cmd)
            
            if result == 0:
                successful += 1
                print(f"  ✓ 转换成功")
            else:
                failed += 1
                print(f"  ✗ 转换失败 (退出码: {result})")
            
            # 显示进度
            progress = ((i + 1) / len(folder_list)) * 100
            print(f"  进度: {i+1}/{len(folder_list)} ({progress:.1f}%)")
            print("-" * 30)
            
        except Exception as e:
            failed += 1
            print(f"  ✗ 处理异常: {e}")
            print("-" * 30)
    
    # 转换结果统计
    end_time = time.time()
    total_time = end_time - start_time
    
    result = {
        "success": successful,
        "failed": failed, 
        "total": len(folder_list),
        "time": total_time
    }
    
    print("=" * 50)
    print("转换完成!")
    print(f"成功转换: {successful} 个文件夹")
    print(f"转换失败: {failed} 个文件夹")
    print(f"总计处理: {len(folder_list)} 个文件夹")
    print(f"总耗时: {total_time:.2f} 秒")
    
    if failed > 0:
        print(f"警告: 有 {failed} 个文件夹转换失败")
    
    return result


def main():
    """主函数"""
    print("DICOM到NIfTI批量转换工具 v1.1")
    print("适用于nnU-Net医学影像深度学习框架")
    print("=" * 50)
    
    # 检查运行环境
    if not check_environment():
        sys.exit(1)
    
    # 配置路径 - 可根据需要修改
    # source_path = "/media/lirongyaoper/350142ad-6ead-4db5-b07c-25bd698ad3c7/lungCT/yuanshi184_unzip"
    source_path = "/mnt/data/new500/100/image100"
    dest_dir = "/mnt/data/new500/100/imageniigz/"
    
    # 支持命令行参数
    if len(sys.argv) >= 3:
        source_path = sys.argv[1]
        dest_dir = sys.argv[2]
        print(f"使用命令行参数:")
        print(f"  源路径: {source_path}")
        print(f"  目标路径: {dest_dir}")
    else:
        print(f"使用默认配置:")
        print(f"  源路径: {source_path}")
        print(f"  目标路径: {dest_dir}")
        print(f"提示: 也可以使用命令行参数: python {sys.argv[0]} <源路径> <目标路径>")
    
    print("-" * 50)
    
    # 确认继续
    try:
        confirm = input("是否继续执行转换? (y/N): ").strip().lower()
        if confirm not in ['y', 'yes', '是']:
            print("转换已取消")
            sys.exit(0)
    except KeyboardInterrupt:
        print("\n转换已取消")
        sys.exit(0)
    
    # 执行转换
    try:
        result = dcm_niigz(source_path, dest_dir)
        
        # 根据结果设置退出码
        if result["failed"] > 0:
            sys.exit(1)  # 有失败的转换
        else:
            sys.exit(0)  # 全部成功
            
    except KeyboardInterrupt:
        print("\n用户中断转换过程")
        sys.exit(1)
    except Exception as e:
        print(f"程序执行错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()