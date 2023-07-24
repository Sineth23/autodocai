import os

def traverse_file_system(root_dir, process_file, process_folder, ignore=None):
    if ignore is None:
        ignore = []

    for root, dirs, files in os.walk(root_dir):
        for file in files:
            file_path = os.path.join(root, file)
            if not any(path in file_path for path in ignore):
                process_file(file_path)

        for folder in dirs:
            folder_path = os.path.join(root, folder)
            if not any(path in folder_path for path in ignore):
                process_folder(folder_path)
