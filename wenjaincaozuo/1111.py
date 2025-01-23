import os

def get_last_directory(path):
    file_list = os.listdir(path)

    for i in range(0, len(file_list)):
        cur_path = os.path.join(path, file_list[i])

        dir_path, file_name = os.path.split(cur_path)
        # print(dir_path)
       # name_all = dir_path.split('/')
        # print(name_all)
    # last_dir = os.path.basename(dir_path)
    # return last_dir

path = "/media/lirongyaoper/350142ad-6ead-4db5-b07c-25bd698ad3c7/lungCT/300yuanshi"
get_last_directory(path)
