class niNum(Exception):
    
    def __init__(self, number):
        super().__init__(f" Ошибка: число {number} отрицательное! Введите положительное число.")

def check(number):
    if number < 0:
        raise niNum(number)
    else:
        print(f" Число {number} корректно!")

if __name__ == "__main__":
    try:
        num = float(input("Введите число: "))
        check(num)
    except ValueError:
        print(" Ошибка: введено не число.")
    except niNum as e:
        print(e)
