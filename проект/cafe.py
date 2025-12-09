# cafe_gui_ru.py
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QListWidget, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QInputDialog, QMessageBox

class MenuItem:
    def __init__(self, name, price):
        self.name = name
        self.price = price

class Waiter:
    def __init__(self, name):
        self.name = name

class CafeApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Система Управления Кафе")
        self.resize(700, 400)

        # --- Данные ---
        self.menu = [
            MenuItem("Кофе", 3),
            MenuItem("Чай", 2.5),
            MenuItem("Сэндвич", 5),
            MenuItem("Торт", 4)
        ]
        self.waiters = [Waiter("Алиса"), Waiter("Боб")]
        self.order = []  # список кортежей (MenuItem, quantity)

        # --- Виджеты ---
        self.menu_list = QListWidget()
        for item in self.menu:
            self.menu_list.addItem(f"{item.name} - {item.price} $")

        self.order_list = QListWidget()

        self.waiter_combo = QComboBox()
        for w in self.waiters:
            self.waiter_combo.addItem(w.name)

        self.add_button = QPushButton("Добавить в заказ")
        self.remove_button = QPushButton("Удалить из заказа")
        self.total_button = QPushButton("Рассчитать итог")

        # --- Layout ---
        menu_layout = QVBoxLayout()
        menu_layout.addWidget(QLabel("Меню"))
        menu_layout.addWidget(self.menu_list)
        menu_layout.addWidget(self.add_button)

        order_layout = QVBoxLayout()
        order_layout.addWidget(QLabel("Заказ"))
        order_layout.addWidget(self.order_list)
        order_layout.addWidget(self.remove_button)
        order_layout.addWidget(QLabel("Официант"))
        order_layout.addWidget(self.waiter_combo)
        order_layout.addWidget(self.total_button)

        main_layout = QHBoxLayout()
        main_layout.addLayout(menu_layout)
        main_layout.addLayout(order_layout)

        self.setLayout(main_layout)

        # --- События ---
        self.add_button.clicked.connect(self.add_item)
        self.remove_button.clicked.connect(self.remove_item)
        self.total_button.clicked.connect(self.calculate_total)

    def add_item(self):
        selected = self.menu_list.currentRow()
        if selected >= 0:
            # Ввод количества
            quantity, ok = QInputDialog.getInt(self, "Количество", f"Введите количество для {self.menu[selected].name}:", 1, 1, 100)
            if ok:
                self.order.append((self.menu[selected], quantity))
                self.order_list.addItem(f"{self.menu[selected].name} x{quantity} - {self.menu[selected].price * quantity} $")

    def remove_item(self):
        selected = self.order_list.currentRow()
        if selected >= 0:
            self.order.pop(selected)
            self.order_list.takeItem(selected)

    def calculate_total(self):
        if not self.order:
            QMessageBox.information(self, "Итог", "Заказ пуст")
            return

        discount, ok = QInputDialog.getInt(self, "Скидка", "Введите скидку (%)", 0, 0, 100)
        if ok:
            total = sum(item.price * quantity for item, quantity in self.order)
            total_after_discount = total - total * discount / 100
            waiter = self.waiter_combo.currentText()
            QMessageBox.information(self, "Итог", f"Официант: {waiter}\nОбщая сумма: {total_after_discount:.2f} $")

if __name__ == "__main__":
    app = QApplication([])
    window = CafeApp()
    window.show()
    app.exec()
