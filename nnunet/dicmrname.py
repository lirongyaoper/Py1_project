import os
import pydicom
from pathlib import Path


def get_dcm_info(dcm_path):
    """获取DICOM文件中的Patient ID和Patient Name"""
    try:
        ds = pydicom.dcmread(dcm_path)
        patient_id = getattr(ds, 'PatientID', 'UNKNOWN_ID')
        patient_name = getattr(ds, 'PatientName', 'UNKNOWN_NAME')

        # 处理PatientName，移除空格和其他可能的问题字符
        if isinstance(patient_name, pydicom.valuerep.PersonName):
            patient_name = str(patient_name)
        patient_name_clean = patient_name.replace(' ', '')

        return patient_id, patient_name_clean
    except Exception as e:
        print(f"Error reading {dcm_path}: {e}")
        return None, None


def rename_parent_folder(folder_path):
    """重命名包含DICOM文件的父文件夹"""
    # 查找文件夹中的DICOM文件
    dcm_files = list(Path(folder_path).glob('*.dcm')) + list(Path(folder_path).glob('*.DCM'))

    if not dcm_files:
        print(f"No DICOM files found in {folder_path}")
        return False

    # 使用第一个找到的DICOM文件获取信息
    patient_id, patient_name = get_dcm_info(dcm_files[0])

    if not patient_id or not patient_name:
        print(f"Could not get valid DICOM info from {dcm_files[0]}")
        return False

    # 构建新文件夹名
    new_folder_name = f"{patient_id}_{patient_name}"

    # 获取父目录路径
    parent_dir = Path(folder_path).parent

    # 构建新路径
    new_path = os.path.join(parent_dir, new_folder_name)

    # 如果新名称与旧名称相同，则跳过
    if os.path.normpath(folder_path) == os.path.normpath(new_path):
        print(f"Folder already has correct name: {folder_path}")
        return True

    # 重命名文件夹
    try:
        os.rename(folder_path, new_path)
        print(f"Renamed: {folder_path} -> {new_path}")
        return True
    except Exception as e:
        print(f"Error renaming {folder_path} to {new_path}: {e}")
        return False


def process_dcm_folders(root_dir):
    """处理根目录下的所有包含DICOM文件的文件夹"""
    processed = 0
    skipped = 0
    errors = 0

    # 遍历根目录下的所有子目录
    for dirpath, dirnames, filenames in os.walk(root_dir):
        # 检查当前目录是否包含DICOM文件
        dcm_files = [f for f in filenames if f.lower().endswith('.dcm')]

        if dcm_files:
            if rename_parent_folder(dirpath):
                processed += 1
            else:
                errors += 1
        else:
            skipped += 1

    print(f"\nProcessing complete:")
    print(f"- Folders processed successfully: {processed}")
    print(f"- Folders skipped (no DICOM files): {skipped}")
    print(f"- Errors encountered: {errors}")


if __name__ == "__main__":
    import sys

    if len(sys.argv) != 2:
        print("Usage: python rename_dcm_folders.py <root_directory>")
        sys.exit(1)

    root_dir = sys.argv[1]

    if not os.path.isdir(root_dir):
        print(f"Error: {root_dir} is not a valid directory")
        sys.exit(1)

    print(f"Starting processing of directory: {root_dir}")
    process_dcm_folders(root_dir)