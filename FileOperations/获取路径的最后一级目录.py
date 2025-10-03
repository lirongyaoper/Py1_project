import os

def get_last_directory(path):
    dir_path, file_name = os.path.split(path)
    last_dir = os.path.basename(dir_path)
    return last_dir

path = "/path/to/some/file.txt"
last_dir = get_last_directory(path)
print(last_dir)