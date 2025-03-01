import os                                                 #导入模块
def delete_files(path):                                           #定义函数名称
    for foldName, subfolders, filenames in os.walk(path):     #用os.walk方法取得path路径下的文件夹路径，子文件夹名，所有文件名
           for filename in filenames:                         #遍历列表下的所有文件名

              if filename.endswith('json'):                #当文件名以.txt后缀结尾时
                 os.remove(os.path.join(foldName, filename))    #删除符合条件的文件
                 print("{} deleted.".format(filename))           ##输出提示

if __name__ == '__main__':
        path = r'/mnt/data/103/imagesnii'   #运行程序前，记得修改主文件夹路径！
        delete_files(path)         #调用定义的函数，注意名称与定义的函数名一致
