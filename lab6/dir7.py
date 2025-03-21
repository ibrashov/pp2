import shutil
import os

def copy_file(source_path, destination_path):
    if not os.path.exists(source_path):
        print("Source file not found:", source_path)
        return
    try:
        shutil.copy(source_path, destination_path)
        print(f"File copied to '{destination_path}'")
    except Exception as e:
        print("Error during copy:", e)

if __name__ == "__main__":
    src = input("Enter source file path: ").strip()
    dst = input("Enter destination file path: ").strip()
    copy_file(src, dst)
