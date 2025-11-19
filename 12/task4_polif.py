from abc import ABC, abstractmethod

class Vehicle(ABC):
    @abstractmethod
    def move(self): pass


class Car(Vehicle):
    def move(self):
        print("Көлік жүреді.")


class Bicycle(Vehicle):
    def move(self):
        print("Велосипед жүреді.")


class Airplane(Vehicle):
    def move(self):
        print("Ұшақ ұшады.")


class Train(Vehicle):
    def move(self):
        print("Пойыз жүріп келеді.")


print("Көліктер тізімі: car, bike, airplane, train")
choice = input("Көлік таңдаңыз: ")

classes = {
    "car": Car,
    "bike": Bicycle,
    "airplane": Airplane,
    "train": Train
}

if choice not in classes:
    print("Қате таңдау!")
    exit()

obj = classes[choice]()
obj.move()
