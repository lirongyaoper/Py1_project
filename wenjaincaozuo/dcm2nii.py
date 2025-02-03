import os
import subprocess
import nibabel as nib
import pydicom
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path


def convert_dcm_to_nii_gz(dcm_dir, output_dir):
    """
    将单个DICOM文件夹转换为NIfTI.gz格式
    :param dcm_dir: 包含DICOM文件的目录
    :param output_dir: 输出目录
    """
    try:
        # 使用dcm2niix进行转换
        cmd = [
            'dcm2niix',
            '-z', 'y',  # 压缩为.gz
            '-f', '%i_%d',  # 命名格式：StudyID_SeriesNumber
            '-o', output_dir,  # 输出目录
            dcm_dir  # 输入目录
        ]

        # 执行命令
        result = subprocess.run(cmd, check=True, capture_output=True, text=True)

        # 获取生成的.nii.gz文件路径
        output_files = [f for f in os.listdir(output_dir) if f.endswith('.nii.gz')]
        print(f"转换成功: {dcm_dir} -> {output_files}")
        return True

    except subprocess.CalledProcessError as e:
        print(f"转换失败: {dcm_dir}\n错误信息: {e.stderr}")
        return False
    except Exception as e:
        print(f"未知错误: {dcm_dir}\n{str(e)}")
        return False


def batch_convert(input_root, output_root, max_workers=8):
    """
    批量转换函数
    :param input_root: DICOM根目录
    :param output_root: 输出根目录
    :param max_workers: 并行线程数
    """
    Path(output_root).mkdir(parents=True, exist_ok=True)

    # 收集所有包含DICOM文件的目录
    dcm_dirs = []
    for root, _, files in os.walk(input_root):
        if any(f.lower().endswith('.dcm') for f in files):
            dcm_dirs.append(root)

    # 并行处理
    with ThreadPoolExecutor(max_workers=max_workers) as executor:
        futures = []
        for dcm_dir in dcm_dirs:
            # 创建对应的输出子目录
            rel_path = os.path.relpath(dcm_dir, input_root)
            output_dir = os.path.join(output_root, rel_path)
            os.makedirs(output_dir, exist_ok=True)

            # 提交任务
            futures.append(executor.submit(
                convert_dcm_to_nii_gz,
                dcm_dir,
                output_dir
            ))

        # 等待所有任务完成
        success = 0
        for future in futures:
            success += 1 if future.result() else 0

        print(f"\n转换完成: 成功 {success}/{len(dcm_dirs)}, 失败 {len(dcm_dirs) - success}")


if __name__ == "__main__":
    import argparse

    parser = argparse.ArgumentParser(description='DICOM批量转NIfTI.gz')
    parser.add_argument('-i', '--input', required=True, help='输入目录')
    parser.add_argument('-o', '--output', required=True, help='输出目录')
    parser.add_argument('-j', '--jobs', type=int, default=8, help='并行任务数')
    args = parser.parse_args()

    batch_convert(args.input, args.output, args.jobs)