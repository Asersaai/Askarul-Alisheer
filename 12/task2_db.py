from abc import ABC, abstractmethod

class DB(ABC):
    @abstractmethod
    def connect(self): pass

    @abstractmethod
    def query(self): pass

    @abstractmethod
    def close(self): pass


class SQLite(DB):
    def connect(self):
        print("SQLite: қосылды.")
    def query(self):
        print("SQLite: сұраныс орындалды.")
    def close(self):
        print("SQLite: жабылды.")


class Postgre(DB):
    def connect(self):
        print("PostgreSQL: қосылды.")
    def query(self):
        print("PostgreSQL: сұраныс орындалды.")
    def close(self):
        print("PostgreSQL: жабылды.")


db_choice = input("Дерекқорды таңдаңыз (sqlite/pg): ")

db = SQLite() if db_choice == "sqlite" else Postgre()

db.connect()
db.query()
db.close()