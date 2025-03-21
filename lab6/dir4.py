# file: line_counter.py

def count_lines_in_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            lines = file.readlines()
            return len(lines)
    except FileNotFoundError:
        print("❌ File not found:", file_path)
        return 0
    except Exception as e:
        print("❌ Error:", e)
        return 0

if __name__ == "__main__":
    path = input("Enter the path to the text file: ").strip()
    total_lines = count_lines_in_file(path)
    print(f"📄 Total number of lines: {total_lines}")
