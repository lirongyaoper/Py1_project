import os
import shutil
rootdir = '/media/lirongyaoper/350142ad-6ead-4db5-b07c-25bd698ad3c7_lry/lungCT/合并203/merge203/202'
list = os.listdir(rootdir)
for i in range(0,len(list)):     #遍历目录下的所有文件夹
    path=os.path.join(rootdir,list[i],'stl')
    shutil.rmtree(path)