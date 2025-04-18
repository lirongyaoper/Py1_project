import os
import SimpleITK as sitk
image_dir = "/home/lirongyaoper/Documents/trainable/huyanchang/images/"
label_dir = "/home/lirongyaoper/Documents/trainable/huyanchang/label/"
def get_double_extension(filename):
    # 首先获取第一个后缀
    root, ext1 = os.path.splitext(filename)

    # 再尝试获取第二个后缀
    root, ext2 = os.path.splitext(root)

    if ext2:
        # 如果存在第二个后缀，说明这是双后缀
        return root ,ext2 + ext1
    else:
        # 如果不存在第二个后缀，返回单一后缀
        return root,ext1

def check_image_label(image_dir,label_dir):
    for filename in os.listdir(image_dir):
        if filename.endswith(".nii.gz"):
            # 读取图像
            image_path = os.path.join(image_dir, filename)
            image = sitk.ReadImage(image_path)
            case_id = get_double_extension(filename)[0]
            # print(case_id)

            label_path = os.path.join(label_dir, f"{case_id}.nii.gz")
            label = sitk.ReadImage(label_path)
            #
            # 检查对齐
            if image.GetOrigin() != label.GetOrigin():
                print(f"Error: Origin mismatch in {case_id}")

            if image.GetSpacing() != label.GetSpacing():
                print(f"Error: Spacing mismatch in {case_id}")






if __name__ =="__main__":
    check_image_label(image_dir,label_dir)