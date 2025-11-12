import hashlib
import getpass


users = {
    "admin": {
        "password": hashlib.sha256("admin123".encode()).hexdigest(),
        "role": "Admin"
    },
    "Aslan": {
        "password": hashlib.sha256("python2025".encode()).hexdigest(),
        "role": "User"
    },
    "Alisher": {
        "password": hashlib.sha256("guestpass".encode()).hexdigest(),
        "role": "User"
    }
}

def hash_password(password: str) -> str:
    
    return hashlib.sha256(password.encode()).hexdigest()

def register_user():
    print("\n=== Регистрация нового пользователя ===")
    while True:
        username = input("Введите имя пользователя: ").strip()
        if not username:
            print("Имя пользователя не может быть пустым.")
            continue
        if username in users:
            print("Пользователь с таким именем уже существует. Попробуйте другое имя.")
            continue
        break

    
    while True:
        password = getpass.getpass("Введите пароль: ")
        password_confirm = getpass.getpass("Подтвердите пароль: ")
        if password != password_confirm:
            print("Пароли не совпадают. Попробуйте снова.")
            continue
        if not password:
            print("Пароль не может быть пустым.")
            continue
        break

    
    roles = ["Admin", "User"]
    print("Выберите роль:")
    for i, r in enumerate(roles, start=1):
        print(f" {i}. {r}")
    while True:
        choice = input("Введите номер роли (1/2): ").strip()
        if choice not in ("1", "2"):
            print("Неверный выбор. Введите 1 или 2.")
            continue
        role = roles[int(choice) - 1]
        break

    users[username] = {
        "password": hash_password(password),
        "role": role
    }
    print(f"Пользователь '{username}' зарегистрирован с ролью '{role}'.")

def login():
    print("\n=== Вход ===")
    username = input("Имя пользователя: ").strip()
    password = getpass.getpass("Пароль: ")
    hashed_input = hash_password(password)

    if username in users:
        if users[username]["password"] == hashed_input:
            role = users[username]['role']
            print(f"Вход успешен. Добро пожаловать, {role} ({username})!")
            return role
        else:
            print("Неверный пароль.")
    else:
        print("Неверное имя пользователя.")
    return None

def list_users(show_hash=True):
    print("\n=== Список пользователей ===")
    if not users:
        print("Пользователей нет.")
        return
    for name, info in users.items():
        if show_hash:
            print(f"- {name} | role: {info['role']} | hash: {info['password']}")
        else:
            print(f"- {name} | role: {info['role']}")

def main_menu():
    while True:
        print("\n=== Меню ===")
        print("1. Зарегистрировать пользователя")
        print("2. Войти")
        print("3. Показать всех пользователей (с хэшами)")
        print("4. Показать пользователей (без хэшей)")
        print("5. Выход")
        choice = input("Выберите действие (1-5): ").strip()

        if choice == "1":
            register_user()
        elif choice == "2":
            login()
        elif choice == "3":
            list_users(show_hash=True)
        elif choice == "4":
            list_users(show_hash=False)
        elif choice == "5":
            print("Выход!")
            break
        else:
            print("Неверный выбор. Попробуйте снова.")

if __name__ == "__main__":
    main_menu()
