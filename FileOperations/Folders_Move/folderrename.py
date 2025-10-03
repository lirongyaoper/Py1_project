import os

path = "/mnt/data/new500/100/imageniigz"  # 目标路径
prefix = ""  # 新前缀
suffix = "y"





if __name__ =='__main__':
    for folder in os.listdir(path):
        if os.path.isdir(os.path.join(path, folder)):
            new_name = prefix + folder + suffix
            os.rename(os.path.join(path, folder), os.path.join(path, new_name))