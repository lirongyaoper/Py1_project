import os
import shutil
def move_files(src_directory,dest_directory,file_extension=None):
    if not os.path.exists(dest_directory):
        os.makedirs(dest_directory)
    for dirpath,_, filenames in os.walk(src_directory):
        for filename in filenames:
            print(filename)
            # if file_extension is None or filename.endswith(file_extension):
            #     source_file = os.path.join(dirpath,filename)
            #     destination_file = os.path.join(dest_directory,filename)
            #     shutil.move(source_file,destination_file)
            #     print(f"已移动{source_file}文件到{destination_file}")
if __name__ == "__main__":
    source_dir = "/media/lirongyaoper/350142ad-6ead-4db5-b07c-25bd698ad3c7/lungCT/257/images/case97"
    destination_dir = "/media/lirongyaoper/350142ad-6ead-4db5-b07c-25bd698ad3c7/lungCT/257/images/case97zip"
    file_ext = ".zip"
    move_files(source_dir,destination_dir,file_ext)