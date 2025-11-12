class Animal:
   
    def speak(self):
        print("This animal makes a sound.")


class Dog(Animal):
    
    def speak(self):
        print("Woof! Woof!")



a = Animal()
d = Dog()

a.speak()  
d.speak()  
