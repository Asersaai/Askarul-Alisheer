from abc import ABC, abstractmethod

class Logger(ABC):
    def start(self):
        print("=== ЛОГ БАСТАЛДЫ ===")

    @abstractmethod
    def log(self, msg): pass


class FileLogger(Logger):
    def log(self, msg):
        with open("log.txt", "a") as f:
            f.write(msg + "\n")
        print("Файлға жазылды.")


class ConsoleLogger(Logger):
    def log(self, msg):
        print("Консоль:", msg)


log_type = input("Логгер түрін таңдаңыз (file/console): ")
msg = input("Хабар жазыңыз: ")

logger = FileLogger() if log_type == "file" else ConsoleLogger()

logger.start()
logger.log(msg)