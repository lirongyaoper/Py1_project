import os


def show_files(path):
    # 首先遍历当前目录所有文件及文件夹
    file_list = os.listdir(path)
    # 准备循环判断每个元素是否是文件夹还是文件，是文件的话，把名称传入list，是文件夹的话，递归
    for file in file_list:
        # 利用os.path.join()方法取得路径全名，并存入cur_path变量，否则每次只能遍历一层目录
        cur_path = os.path.join(path, file)
        # 判断是否是文件夹
        if os.path.isdir(cur_path):
            show_files(cur_path)
        else:
            name_all = cur_path.split('/')
            if name_all[-1].startswith('merge.'):
                # print(name_all[-4])

                os.rename(cur_path,'/media/lirongyaoper/350142ad-6ead-4db5-b07c-25bd698ad3c7/lungCT/300labelnii/'+name_all[-4]+'.nii.gz')



# 传入空的list接收文件名
show_files("/media/lirongyaoper/350142ad-6ead-4db5-b07c-25bd698ad3c7/lungCT/300label")
# 循环打印show_files函数返回的文件名列表
# for content in contents:
#     print(content)