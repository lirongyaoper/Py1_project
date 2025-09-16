#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
DICOM到NIfTI批量转换工具 - 优化版本
适用于nnU-Net等医学影像深度学习框架的数据预处理

作者: 医学影像处理工具
版本: 2.0
环境: conda nnunet
"""

import os
import sys
import time
import subprocess
import logging
from pathlib import Path
from typing import Union, Optional


class DicomToNiftiConverter:
    """DICOM到NIfTI转换器类"""
    
    def __init__(self, log_level: str = "INFO", max_search_depth: int = 10, skip_existing: bool = True):
        """
        初始化转换器
        
        Args:
            log_level: 日志级别 (DEBUG, INFO, WARNING, ERROR)
            max_search_depth: 递归搜索的最大深度
            skip_existing: 是否跳过已存在的输出文件夹
        """
        self.setup_logging(log_level)
        self.logger = logging.getLogger(__name__)
        self.max_search_depth = max_search_depth
        self.skip_existing = skip_existing
        
    def setup_logging(self, level: str):
        """设置日志配置"""
        logging.basicConfig(
            level=getattr(logging, level.upper()),
            format='%(asctime)s - %(levelname)s - %(message)s',
            handlers=[
                logging.StreamHandler(sys.stdout),
                logging.FileHandler('dicom_conversion.log', encoding='utf-8')
            ]
        )
        
    def check_dcm2niix_available(self) -> bool:
        """
        检查dcm2niix工具是否可用
        
        Returns:
            bool: True如果dcm2niix可用，False否则
        """
        try:
            result = subprocess.run(['dcm2niix', '-h'], 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=10)
            if result.returncode == 0:
                self.logger.info("dcm2niix工具检查通过")
                return True
            else:
                self.logger.error("dcm2niix工具不可用")
                return False
        except (subprocess.TimeoutExpired, FileNotFoundError) as e:
            self.logger.error(f"dcm2niix工具检查失败: {e}")
            return False
            
    def validate_paths(self, source_path: Union[str, Path], 
                      dest_dir: Union[str, Path]) -> tuple[Path, Path]:
        """
        验证输入和输出路径
        
        Args:
            source_path: 源DICOM目录路径
            dest_dir: 目标NIfTI目录路径
            
        Returns:
            tuple: 验证后的路径对象
            
        Raises:
            ValueError: 当路径无效时
        """
        source_path = Path(source_path)
        dest_dir = Path(dest_dir)
        
        if not source_path.exists():
            raise ValueError(f"源目录不存在: {source_path}")
            
        if not source_path.is_dir():
            raise ValueError(f"源路径不是目录: {source_path}")
            
        # 创建目标目录（如果不存在）
        try:
            dest_dir.mkdir(parents=True, exist_ok=True)
            self.logger.info(f"目标目录已创建: {dest_dir}")
        except PermissionError:
            raise ValueError(f"无法创建目标目录（权限不足）: {dest_dir}")
            
        return source_path, dest_dir
        
    def get_dicom_folders(self, source_path: Path) -> list[Path]:
        """
        递归获取源目录下的所有DICOM文件夹
        
        Args:
            source_path: 源目录路径
            
        Returns:
            list: DICOM文件夹路径列表
        """
        dicom_folders = []
        
        def _recursive_search(current_path: Path, current_depth: int = 0):
            """递归搜索DICOM文件夹"""
            if current_depth > self.max_search_depth:
                self.logger.warning(f"达到最大搜索深度 {self.max_search_depth}，跳过: {current_path}")
                return
                
            try:
                for item in current_path.iterdir():
                    if item.is_dir():
                        # 检查当前文件夹是否包含DICOM文件
                        dicom_files = list(item.glob("*.dcm")) + list(item.glob("*.DCM"))
                        
                        if dicom_files:
                            dicom_folders.append(item)
                            self.logger.debug(f"发现DICOM文件夹: {item.relative_to(source_path)} (包含{len(dicom_files)}个文件)")
                        else:
                            # 检查是否有无扩展名的DICOM文件
                            potential_dicom = [f for f in item.iterdir() 
                                             if f.is_file() and not f.suffix]
                            if potential_dicom:
                                dicom_folders.append(item)
                                self.logger.debug(f"发现可能的DICOM文件夹: {item.relative_to(source_path)}")
                            else:
                                # 如果当前文件夹不包含DICOM文件，继续递归搜索子文件夹
                                _recursive_search(item, current_depth + 1)
                                
            except PermissionError:
                self.logger.warning(f"无权限访问目录: {current_path}")
            except Exception as e:
                self.logger.warning(f"搜索目录时出错 {current_path}: {e}")
        
        self.logger.info(f"开始递归搜索DICOM文件夹，最大深度: {self.max_search_depth}")
        _recursive_search(source_path)
        
        if not dicom_folders:
            self.logger.warning(f"在{source_path}及其子目录中未找到DICOM文件夹")
        else:
            self.logger.info(f"递归搜索完成，共找到 {len(dicom_folders)} 个DICOM文件夹")
            
        return sorted(dicom_folders)
        
    def convert_single_folder(self, source_folder: Path, 
                            dest_folder: Path, source_root: Path) -> bool:
        """
        转换单个DICOM文件夹
        
        Args:
            source_folder: 源DICOM文件夹
            dest_folder: 目标NIfTI文件夹
            source_root: 源根目录，用于计算第一级目录名
            
        Returns:
            bool: 转换是否成功
        """
        try:
            # 创建目标文件夹
            dest_folder.mkdir(parents=True, exist_ok=True)
            
            # 计算第一级目录名作为输出文件名
            relative_path = source_folder.relative_to(source_root)
            first_level_dir = relative_path.parts[0] if relative_path.parts else source_folder.name
            
            # 构建dcm2niix命令
            cmd = [
                'dcm2niix',
                '-o', str(dest_folder),  # 输出目录
                '-z', 'y',               # 启用gzip压缩
                '-f', first_level_dir,   # 输出文件名前缀（第一级目录名）
                str(source_folder)       # 源目录
            ]
            
            self.logger.info(f"开始转换: {source_folder.name} -> {first_level_dir}.nii.gz")
            self.logger.debug(f"执行命令: {' '.join(cmd)}")
            
            # 执行转换
            result = subprocess.run(cmd, 
                                  capture_output=True, 
                                  text=True, 
                                  timeout=300)  # 5分钟超时
            
            if result.returncode == 0:
                self.logger.info(f"转换成功: {source_folder.name}")
                self.logger.debug(f"dcm2niix输出: {result.stdout}")
                return True
            else:
                self.logger.error(f"转换失败: {source_folder.name}")
                self.logger.error(f"错误输出: {result.stderr}")
                return False
                
        except subprocess.TimeoutExpired:
            self.logger.error(f"转换超时: {source_folder.name}")
            return False
        except Exception as e:
            self.logger.error(f"转换异常: {source_folder.name} - {e}")
            return False
            
    def convert_batch(self, source_path: Union[str, Path], 
                     dest_dir: Union[str, Path]) -> dict:
        """
        批量转换DICOM文件夹到NIfTI格式
        
        Args:
            source_path: 源DICOM目录路径
            dest_dir: 目标NIfTI目录路径
            
        Returns:
            dict: 转换结果统计
        """
        start_time = time.time()
        
        try:
            # 验证路径
            source_path, dest_dir = self.validate_paths(source_path, dest_dir)
            
            # 检查dcm2niix工具
            if not self.check_dcm2niix_available():
                raise RuntimeError("dcm2niix工具不可用，请先安装")
                
            # 获取DICOM文件夹列表
            dicom_folders = self.get_dicom_folders(source_path)
            
            if not dicom_folders:
                self.logger.warning("未找到任何DICOM文件夹")
                return {"success": 0, "failed": 0, "total": 0, "time": 0}
                
            self.logger.info(f"找到{len(dicom_folders)}个DICOM文件夹")
            
            # 开始批量转换
            successful = 0
            failed = 0
            skipped = 0
            
            for i, folder in enumerate(dicom_folders, 1):
                self.logger.info(f"处理进度: {i}/{len(dicom_folders)} ({i/len(dicom_folders)*100:.1f}%)")
                
                # 保持相对目录结构
                relative_path = folder.relative_to(source_path)
                dest_folder = dest_dir / relative_path
                
                # 检查是否跳过
                if self.skip_existing and dest_folder.exists():
                    nifti_files = list(dest_folder.glob("*.nii.gz")) + list(dest_folder.glob("*.nii"))
                    if nifti_files:
                        self.logger.info(f"跳过已存在NIfTI文件的文件夹: {relative_path}")
                        skipped += 1
                        continue
                
                if self.convert_single_folder(folder, dest_folder, source_path):
                    successful += 1
                else:
                    failed += 1
                    
        except Exception as e:
            self.logger.error(f"批量转换失败: {e}")
            return {"success": 0, "failed": 0, "total": 0, "time": 0, "error": str(e)}
            
        end_time = time.time()
        total_time = end_time - start_time
        
        # 转换结果统计
        result = {
            "success": successful,
            "failed": failed,
            "skipped": skipped,
            "total": len(dicom_folders),
            "time": total_time
        }
        
        self.logger.info(f"批量转换完成!")
        self.logger.info(f"成功: {successful}, 失败: {failed}, 跳过: {skipped}, 总计: {len(dicom_folders)}")
        self.logger.info(f"耗时: {total_time:.2f}秒")
        
        return result


def main():
    """主函数"""
    # 配置路径
    SOURCE_PATH = "/home/lirongyaoper/Downloads/3dCT"
    DEST_DIR = "/home/lirongyaoper/Downloads/imageniigz"
    
    # 可选：从命令行参数读取路径
    if len(sys.argv) >= 3:
        SOURCE_PATH = sys.argv[1]
        DEST_DIR = sys.argv[2]
    
    # 创建转换器实例
    converter = DicomToNiftiConverter(log_level="INFO")
    
    # 执行批量转换
    try:
        result = converter.convert_batch(SOURCE_PATH, DEST_DIR)
        
        if "error" in result:
            print(f"转换失败: {result['error']}")
            sys.exit(1)
        else:
            print(f"\n=== 转换完成 ===")
            print(f"成功转换: {result['success']} 个文件夹")
            print(f"转换失败: {result['failed']} 个文件夹")
            print(f"跳过已存在: {result.get('skipped', 0)} 个文件夹")
            print(f"总计发现: {result['total']} 个DICOM文件夹")
            print(f"总耗时: {result['time']:.2f} 秒")
            
            if result['failed'] > 0:
                print(f"警告: 有 {result['failed']} 个文件夹转换失败，请查看日志文件 dicom_conversion.log")
                sys.exit(1)
            
    except KeyboardInterrupt:
        print("\n用户中断转换过程")
        sys.exit(1)
    except Exception as e:
        print(f"程序执行错误: {e}")
        sys.exit(1)


if __name__ == "__main__":
    main()

