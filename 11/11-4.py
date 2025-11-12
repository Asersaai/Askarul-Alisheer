class Teacher:

    def role(self):
        print("Преподаёт студентам.")  

class Researcher:

    def role(self):
        print("Проводит исследования.") 

class Professor(Teacher, Researcher):

    def role(self):
        super().role() 
        Researcher.role(1) 
        
      
        print("Также управляет академическими проектами.")  

p = Professor()
p.role()