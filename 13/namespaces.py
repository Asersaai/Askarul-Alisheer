x = "global"   # Глобальная переменная

def outer():
    x = "enclosing"   # Переменная в замыкании

    def inner():
        x = "local"   # Локальная переменная
        print("Inner:", x)

    inner()
    print("Outer:", x)

outer()
print("Global:", x)
