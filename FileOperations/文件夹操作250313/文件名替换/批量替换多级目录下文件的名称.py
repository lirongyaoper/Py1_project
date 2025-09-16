#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
批量重命名多级目录下的文件 - 通用文件重命名工具

功能说明:
基于文件名前缀进行重命名，自动保持原文件后缀
将多级目录下的A.xxx文件修改为pulmonary artery.xxx，
将B.xxx文件修改为bronchus.xxx ，
将V.xxx文件修改为pulmonary veins.xxx 
支持任意文件后缀(.nii.gz, .jpg, .png, .txt等)，同时该脚本具有批量处理多个子文件夹的能力

作者: 医学影像处理工具
版本: 2.1 (通用版)
"""

import os
import sys
import time
from pathlib import Path
from typing import Dict, Tuple

# ========== 路径配置区域 ==========
# 使用说明:
# 1. 修改 TARGET_DIRECTORIES 列表来配置批量处理的目录
# 2. 修改 DEFAULT_DIRECTORY 来设置默认的单个处理目录
# 3. 运行脚本时会提供交互式选择界面

TARGET_DIRECTORIES = [
    "/mnt/data/n500last/297/nii",           # 批量处理路径1
    "/home/lirongyaoper/Downloads/test",     # 批量处理路径2  
    # "/path/to/your/directory3",            # 可添加更多路径（去掉注释即可启用）
    # "/path/to/your/directory4",            # 支持任意数量的目录
]

# 默认单个目录路径（单目录模式时使用）
DEFAULT_DIRECTORY = "/home/lirongyaoper/Downloads/3dCT"

# 支持的处理模式:
# 模式1: 单个目录模式 - 处理一个目录
# 模式2: 批量目录模式 - 处理上述 TARGET_DIRECTORIES 中的所有目录  
# 模式3: 手动输入路径 - 运行时手动输入要处理的目录
# ================================


class UniversalFileRenamer:
    """通用文件重命名器类"""
    
    def __init__(self, dry_run: bool = False):
        """
        初始化重命名器
        
        Args:
            dry_run: 是否为试运行模式（不实际执行重命名）
        """
        self.dry_run = dry_run
        # 基于文件名前缀的重命名规则，自动保持原文件后缀
        self.rename_rules = {
            '肺动脉': 'pulmonary_artery',
            '支气管': 'bronchus', 
            '肺静脉': 'pulmonary_veins',
            '左肺': 'left_lung',
            '右肺': 'right_lung',
            '结节': 'nodule',
            '上腔静脉': 'superior_vena_cava',
            '胸主动脉': 'aorta'
        }
        self.stats = {
            'total_files_scanned': 0,
            'files_renamed': 0,
            'files_skipped': 0,
            'errors': 0,
            'directories_processed': 0
        }
        
    def validate_directory(self, directory_path: str) -> bool:
        """
        验证目录是否存在且可访问
        
        Args:
            directory_path: 目录路径
            
        Returns:
            bool: 目录是否有效
        """
        if not os.path.exists(directory_path):
            print(f"错误: 目录不存在 - {directory_path}")
            return False
            
        if not os.path.isdir(directory_path):
            print(f"错误: 路径不是目录 - {directory_path}")
            return False
            
        if not os.access(directory_path, os.R_OK):
            print(f"错误: 没有读取权限 - {directory_path}")
            return False
            
        return True
        
    def check_write_permission(self, directory_path: str) -> bool:
        """
        检查目录是否有写入权限
        
        Args:
            directory_path: 目录路径
            
        Returns:
            bool: 是否有写入权限
        """
        return os.access(directory_path, os.W_OK)
        
    def get_file_prefix_and_suffix(self, filename: str) -> tuple[str, str]:
        """
        解析文件名，获取前缀和后缀
        
        Args:
            filename: 文件名
            
        Returns:
            tuple: (前缀, 后缀)
        """
        # 处理多重后缀，如 .nii.gz, .tar.gz 等
        parts = filename.split('.')
        if len(parts) == 1:
            return parts[0], ''
        
        # 如果文件名只有一个点
        if len(parts) == 2:
            return parts[0], '.' + parts[1]
        
        # 处理多重后缀的情况
        prefix = parts[0]
        suffix = '.' + '.'.join(parts[1:])
        
        return prefix, suffix
        
    def should_rename_file(self, filename: str) -> tuple[bool, str, str]:
        """
        检查文件是否需要重命名
        
        Args:
            filename: 文件名
            
        Returns:
            tuple: (是否需要重命名, 新前缀, 后缀)
        """
        prefix, suffix = self.get_file_prefix_and_suffix(filename)
        
        if prefix in self.rename_rules:
            new_prefix = self.rename_rules[prefix]
            return True, new_prefix, suffix
            
        return False, '', ''
        
    def rename_single_file(self, old_file_path: str, new_file_path: str) -> bool:
        """
        重命名单个文件
        
        Args:
            old_file_path: 原文件路径
            new_file_path: 新文件路径
            
        Returns:
            bool: 重命名是否成功
        """
        try:
            if self.dry_run:
                print(f"[试运行] 将重命名: {old_file_path} -> {new_file_path}")
                return True
            else:
                os.rename(old_file_path, new_file_path)
                print(f"✓ 重命名成功: {os.path.basename(old_file_path)} -> {os.path.basename(new_file_path)}")
                print(f"  位置: {os.path.dirname(old_file_path)}")
                return True
                
        except PermissionError:
            print(f"✗ 权限错误: 无法重命名 {old_file_path}")
            return False
        except FileExistsError:
            print(f"✗ 文件已存在: {new_file_path}")
            return False
        except Exception as e:
            print(f"✗ 重命名失败: {old_file_path} - {str(e)}")
            return False
            
    def rename_files_in_subfolders(self, parent_folder: str) -> Dict[str, int]:
        """
        批量重命名多级目录下的文件（基于前缀匹配）
        
        Args:
            parent_folder: 父目录路径
            
        Returns:
            dict: 处理统计信息
        """
        print(f"{'='*60}")
        print(f"开始处理目录: {parent_folder}")
        print(f"{'='*60}")
        
        if not self.validate_directory(parent_folder):
            self.stats['errors'] += 1
            return self.stats
            
        # 遍历目录
        for root, dirs, files in os.walk(parent_folder):
            self.stats['directories_processed'] += 1
            
            # 检查当前目录的写入权限
            if not self.check_write_permission(root):
                print(f"警告: 目录没有写入权限，跳过 - {root}")
                continue
                
            print(f"\n处理目录: {root}")
            
            files_in_current_dir = 0
            for file_name in files:
                self.stats['total_files_scanned'] += 1
                
                # 检查是否是需要重命名的文件
                should_rename, new_prefix, suffix = self.should_rename_file(file_name)
                if should_rename:
                    files_in_current_dir += 1
                    old_file_path = os.path.join(root, file_name)
                    new_file_name = new_prefix + suffix
                    new_file_path = os.path.join(root, new_file_name)
                    
                    # 检查目标文件是否已存在
                    if os.path.exists(new_file_path):
                        print(f"- 跳过 (目标文件已存在): {file_name}")
                        self.stats['files_skipped'] += 1
                        continue
                        
                    # 执行重命名
                    if self.rename_single_file(old_file_path, new_file_path):
                        self.stats['files_renamed'] += 1
                    else:
                        self.stats['errors'] += 1
                        
            if files_in_current_dir == 0:
                print("- 未找到需要重命名的文件")
                
        return self.stats
        
    def print_summary(self):
        """打印处理结果摘要"""
        print(f"\n{'='*60}")
        print(f"处理完成 - 结果摘要")
        print(f"{'='*60}")
        print(f"扫描目录数: {self.stats['directories_processed']}")
        print(f"扫描文件数: {self.stats['total_files_scanned']}")
        print(f"重命名成功: {self.stats['files_renamed']}")
        print(f"跳过文件数: {self.stats['files_skipped']}")
        print(f"错误次数: {self.stats['errors']}")
        
        if self.dry_run:
            print(f"\n注意: 这是试运行模式，未实际执行重命名操作")
            
        print(f"\n重命名规则 (前缀匹配，自动保持原文件后缀):")
        for old_prefix, new_prefix in self.rename_rules.items():
            print(f"  {old_prefix}.* -> {new_prefix}.*")


def select_processing_mode():
    """选择处理模式"""
    print("\n处理模式选择:")
    print("1. 单个目录模式")
    print("2. 批量目录模式")
    print("3. 手动输入路径")
    
    while True:
        try:
            choice = input("请选择模式 (1-3): ").strip()
            if choice in ['1', '2', '3']:
                return int(choice)
            else:
                print("无效选择，请输入1、2或3")
        except KeyboardInterrupt:
            print("\n操作已取消")
            sys.exit(0)


def get_target_directories():
    """获取要处理的目录列表"""
    mode = select_processing_mode()
    
    if mode == 1:  # 单个目录模式
        if len(sys.argv) >= 2:
            return [sys.argv[1]]
        
        print(f"\n默认目录: {DEFAULT_DIRECTORY}")
        use_default = input("是否使用默认目录? (Y/n): ").strip().lower()
        
        if use_default in ['', 'y', 'yes', '是']:
            return [DEFAULT_DIRECTORY]
        else:
            path = input("请输入目标目录路径: ").strip()
            return [path] if path else [DEFAULT_DIRECTORY]
            
    elif mode == 2:  # 批量目录模式
        print(f"\n批量处理目录列表:")
        valid_dirs = []
        for i, directory in enumerate(TARGET_DIRECTORIES, 1):
            if os.path.exists(directory):
                print(f"  {i}. ✓ {directory}")
                valid_dirs.append(directory)
            else:
                print(f"  {i}. ✗ {directory} (不存在)")
        
        if not valid_dirs:
            print("警告: 没有找到有效的目录")
            return get_target_directories()  # 重新选择
            
        confirm = input(f"\n确认处理这 {len(valid_dirs)} 个有效目录? (y/N): ").strip().lower()
        if confirm in ['y', 'yes', '是']:
            return valid_dirs
        else:
            return get_target_directories()  # 重新选择
            
    else:  # 手动输入路径
        paths = []
        print(f"\n手动输入目录路径 (输入空行结束):")
        while True:
            path = input(f"路径 {len(paths)+1}: ").strip()
            if not path:
                break
            if os.path.exists(path):
                paths.append(path)
                print(f"  ✓ 已添加: {path}")
            else:
                print(f"  ✗ 路径不存在: {path}")
                continue_add = input("    是否继续添加? (y/N): ").strip().lower()
                if continue_add not in ['y', 'yes', '是']:
                    break
        
        return paths if paths else [DEFAULT_DIRECTORY]


def main():
    """主函数"""
    print("通用文件批量重命名工具 v2.1")
    print("支持任意文件后缀的前缀重命名")
    print("-" * 60)
    
    # 获取要处理的目录
    target_directories = get_target_directories()
    
    if not target_directories:
        print("错误: 没有指定有效的目录")
        return
    
    print(f"\n将要处理的目录:")
    for i, directory in enumerate(target_directories, 1):
        print(f"  {i}. {directory}")
    
    # 询问是否试运行
    try:
        response = input("\n是否先进行试运行查看效果? (y/N): ").strip().lower()
        dry_run = response in ['y', 'yes', '是']
    except KeyboardInterrupt:
        print("\n操作已取消")
        return
    
    # 创建重命名器实例
    renamer = UniversalFileRenamer(dry_run=dry_run)
    
    # 显示重命名规则
    print(f"\n重命名规则 (前缀匹配，自动保持原文件后缀):")
    for old_prefix, new_prefix in renamer.rename_rules.items():
        print(f"  {old_prefix}.* -> {new_prefix}.*")
    
    # 最终确认
    if not dry_run:
        try:
            dir_count = len(target_directories)
            confirm = input(f"\n确认开始处理 {dir_count} 个目录? (y/N): ").strip().lower()
            if confirm not in ['y', 'yes', '是']:
                print("操作已取消")
                return
        except KeyboardInterrupt:
            print("\n操作已取消")
            return
    
    # 开始批量处理
    start_time = time.time()
    total_stats = {
        'total_files_scanned': 0,
        'files_renamed': 0,
        'files_skipped': 0,
        'errors': 0,
        'directories_processed': 0,
        'processed_dirs': 0,
        'failed_dirs': 0
    }
    
    try:
        for i, directory in enumerate(target_directories, 1):
            print(f"\n{'='*80}")
            print(f"处理第 {i}/{len(target_directories)} 个目录")
            print(f"{'='*80}")
            
            try:
                stats = renamer.rename_files_in_subfolders(directory)
                
                # 累计统计
                for key in ['total_files_scanned', 'files_renamed', 'files_skipped', 'errors', 'directories_processed']:
                    total_stats[key] += stats.get(key, 0)
                
                if stats.get('errors', 0) == 0:
                    total_stats['processed_dirs'] += 1
                    print(f"✓ 目录处理完成: {directory}")
                else:
                    total_stats['failed_dirs'] += 1
                    print(f"⚠ 目录处理有错误: {directory}")
                    
            except Exception as e:
                total_stats['failed_dirs'] += 1
                total_stats['errors'] += 1
                print(f"✗ 目录处理失败: {directory} - {e}")
        
        # 打印总体结果摘要
        end_time = time.time()
        processing_time = end_time - start_time
        
        print(f"\n{'='*80}")
        print(f"批量处理完成 - 总体摘要")
        print(f"{'='*80}")
        print(f"处理目录总数: {len(target_directories)}")
        print(f"成功处理目录: {total_stats['processed_dirs']}")
        print(f"失败目录数量: {total_stats['failed_dirs']}")
        print(f"扫描子目录数: {total_stats['directories_processed']}")
        print(f"扫描文件总数: {total_stats['total_files_scanned']}")
        print(f"重命名成功: {total_stats['files_renamed']}")
        print(f"跳过文件数: {total_stats['files_skipped']}")
        print(f"错误总数: {total_stats['errors']}")
        print(f"总耗时: {processing_time:.2f} 秒")
        
        if dry_run:
            print(f"\n注意: 这是试运行模式，未实际执行重命名操作")
        
        # 根据结果设置退出码
        if total_stats['errors'] > 0:
            print(f"\n警告: 处理过程中出现 {total_stats['errors']} 个错误")
            sys.exit(1)
        else:
            print(f"\n所有目录处理成功完成!")
            sys.exit(0)
            
    except KeyboardInterrupt:
        print(f"\n用户中断操作")
        sys.exit(1)
    except Exception as e:
        print(f"\n程序执行错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()
