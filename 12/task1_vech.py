from abc import ABC, abstractmethod

class Vehicle(ABC):
    @abstractmethod
    def move(self): pass

    @abstractmethod
    def fuel(self): pass


class Car(Vehicle):
    def move(self):
        print("Көлік жолда жүреді.")
    def fuel(self):
        print("Көлік бензин қолданады.")


class Bicycle(Vehicle):
    def move(self):
        print("Велосипед педальмен жүреді.")
    def fuel(self):
        print("Велосипед адамның энергиясын қолданады.")


choice = input("Көлік таңдаңыз (car/bike): ")

if choice == "car":
    v = Car()
elif choice == "bike":
    v = Bicycle()
else:
    print("Қате таңдау!")
    exit()

v.move()
v.fuel()