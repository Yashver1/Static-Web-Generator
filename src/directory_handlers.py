import os
import shutil


def recursive_move(source_dir,dest_dir):
    if not os.path.exists(source_dir):
        raise ValueError("Invalid File Path")
    if os.path.exists(dest_dir):
        print(f"Warning: erasing {dest_dir}...")
        shutil.rmtree(dest_dir)
    os.mkdir(dest_dir)
    contents = os.listdir(source_dir)
    for content in contents:
        abs_src_path = os.path.join(source_dir,content)
        abs_dest_path = os.path.join(dest_dir,content)
        print(f"moving {abs_src_path} --> {abs_dest_path}...")

        if os.path.isfile(abs_src_path):
            shutil.copy(abs_src_path,abs_dest_path)
        else:
            recursive_move(abs_src_path,abs_dest_path)


        


        
