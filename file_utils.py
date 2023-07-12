import os
import shutil

def create_directory(dir_name):
    if not os.path.exists(dir_name):
        os.makedirs(dir_name)

def move_files_to_directory(src_dir, dest_dir):
    for filename in os.listdir(src_dir):
        if filename.endswith('.md'):
            shutil.move(os.path.join(src_dir, filename), dest_dir)
