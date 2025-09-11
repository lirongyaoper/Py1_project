import os
import shutil


def move_matching_parent_dirs(source_root, dest_root, force_overwrite=False):
    """
    移动所有与父目录同名的末级目录

    参数：
    source_root      : 源目录根路径
    dest_root        : 目标目录根路径
    force_overwrite  : 是否覆盖已存在的目录
    """
    moved_count = 0

    for root, dirs, _ in os.walk(source_root):
        # 获取当前目录的父级名称
        parent_name = os.path.basename(root)

        # 检查是否存在与父级同名的子目录
        if parent_name in dirs:
            src_path = os.path.join(root, parent_name)

            # 验证是否为末级目录
            if is_leaf_directory(src_path):
                # 构建目标路径
                relative_path = os.path.relpath(root, source_root)
                dest_path = os.path.join(dest_root, relative_path, parent_name)

                # 处理目录已存在的情况
                if os.path.exists(dest_path):
                    if not force_overwrite:
                        print(f"⏩ 跳过已存在目录: {dest_path}")
                        continue
                    shutil.rmtree(dest_path)  # 强制删除旧目录

                # 执行移动操作
                try:
                    os.makedirs(os.path.dirname(dest_path), exist_ok=True)
                    shutil.move(src_path, dest_path)
                    print(f"✅ 移动成功: {src_path} → {dest_path}")
                    moved_count += 1
                    dirs.remove(parent_name)  # 防止后续遍历
                except Exception as e:
                    print(f"❌ 移动失败: {src_path} ({str(e)})")

    print(f"\n操作完成: 共移动 {moved_count} 个目录")


def is_leaf_directory(path):
    """检查是否为末级目录（没有子目录）"""
    try:
        return not any(
            os.path.isdir(os.path.join(path, item))
            for item in os.listdir(path)
        )
    except Exception as e:
        print(f"⚠️ 目录检查失败: {path} ({str(e)})")
        return False


if __name__ == "__main__":
    # 配置参数（修改以下路径）
    SOURCE_DIR = "/mnt/data/new500/100"  # 源目录根路径
    TARGET_DIR = "/mnt/data/new500/labelnii"  # 目标目录根路径
    FORCE_MODE = True  # 是否强制覆盖已存在目录

    # 执行移动操作
    move_matching_parent_dirs(
        source_root=SOURCE_DIR,
        dest_root=TARGET_DIR,
        force_overwrite=FORCE_MODE
    )