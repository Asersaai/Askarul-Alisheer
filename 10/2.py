import os

def write_to_file(filename, text, mode="a"):
    with open(filename, mode, encoding='utf-8') as file:
        file.write(text + "\n")
    print(f"Текст успешно записан в {filename}")

def read_from_file(filename):
    if not os.path.exists(filename):
        print("Файл не найден.")
        return
    with open(filename, 'r', encoding='utf-8') as file:
        content = file.read()
    print("Содержимое файла:")
    print(content)

if __name__ == "__main__":
    filename = input("Введите имя файла: ")

    if os.path.exists(filename):
        print(f"Файл '{filename}' уже существует.")
        choice = input("Выберите действие: [1] Перезаписать, [2] Добавить в конец: ")
    else:
        print(f"Файл '{filename}' не существует. Он будет создан.")
        choice = "1"

    text = input("Введите текст: ")

    if choice == "1":
        write_to_file(filename, text, mode="w")  
    elif choice == "2":
        write_to_file(filename, text, mode="a") 
    else:
        print("Неверный выбор!")

    read_from_file(filename)
