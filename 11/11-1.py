import random
class Person:
    def __init__(self, name, age):  
        self.name = name
        self.age = age

    def display_info(self):
        print(f"Name: {self.name}, Age: {self.age}")


class Student(Person):
    def __init__(self, name, age, student_id):  
        super().__init__(name, age) 
        self.student_id = student_id

    def display_info(self):
        print(f"Name: {self.name}, Age: {self.age}, ID: {self.student_id}")


name=input('Name:')
age=input('age:')
id=random.randint(1000,9999)
id_q=(f'ID: ST{id}')

std1=Student(name,age,id_q)
std1.display_info()


