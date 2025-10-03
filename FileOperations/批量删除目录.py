import os
import shutil


def rf_rm(rootdir):
    list = os.listdir(rootdir)
    for i in range(0, len(list)):  # 遍历目录下的所有文件夹
        path = os.path.join(rootdir, list[i], 'stl')
        shutil.rmtree(path)
if __name__ =="__main__":
    rootdir = '/media/lirongyaoper/350142ad-6ead-4db5-b07c-25bd698ad3c7/shuju500/300标注数据'
    rf_rm(rootdir)