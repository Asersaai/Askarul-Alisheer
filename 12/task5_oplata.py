from abc import ABC, abstractmethod

class Payment(ABC):
    @abstractmethod
    def authorize(self): pass

    @abstractmethod
    def process(self): pass

    @abstractmethod
    def refund(self): pass


class PayPal(Payment):
    def authorize(self):
        print("PayPal: авторизация OK.")
    def process(self):
        print("PayPal: төлем орындалды.")
    def refund(self):
        print("PayPal: ақша қайтарылды.")


class Kaspi(Payment):
    def authorize(self):
        print("Kaspi: расталды.")
    def process(self):
        print("Kaspi: төлем өтті.")
    def refund(self):
        print("Kaspi: қайтарылды.")


payment_type = input("Төлем жүйесін таңдаңыз (paypal/kaspi): ")

pay = PayPal() if payment_type == "paypal" else Kaspi()

pay.authorize()
pay.process()
pay.refund()