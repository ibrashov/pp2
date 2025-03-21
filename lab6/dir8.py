import os

def delete_file(path):
    if not os.path.exists(path):
        print("❌ File does not exist:", path)
        return

    if not os.path.isfile(path):
        print("❌ Path is not a file:", path)
        return

    if not os.access(path, os.W_OK):
        print("❌ No write permission to delete the file:", path)
        return

    try:
        os.remove(path)
        print("🗑️ File deleted successfully:", path)
    except Exception as e:
        print("❌ Error deleting file:", e)

if __name__ == "__main__":
    file_path = input("Enter the path of the file to delete: ").strip()
    delete_file(file_path)
