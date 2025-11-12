def read_file(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            content = file.read()
            print("File Contents:\n")
            print(content)
    except FileNotFoundError:
        print(f"Error: The file '{file_path}' does not exist.")
    except IOError as e:
        print(f"Error reading file: {e}")

if __name__ == "__main__":
    file_path = "sample.txt"
    read_file(file_path)
