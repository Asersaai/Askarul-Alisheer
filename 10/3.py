def divide_numbers():
    try:
        a = float(input("Введите первое число: "))
        b = float(input("Введите второе число: "))
        result = a / b
    except ValueError:
        print(" Ошибка: введено не число.")
    except ZeroDivisionError:
        print(" Ошибка: деление на ноль невозможно.")
    else:
        print(f"Результат деления: {result}")
    finally:
        print("Программа завершена.")

if __name__ == "__main__":
    divide_numbers()
