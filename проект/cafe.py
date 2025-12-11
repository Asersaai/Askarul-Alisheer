from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QListWidget, QPushButton, QVBoxLayout, QHBoxLayout, QComboBox, QInputDialog, QMessageBox
from datetime import datetime

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
        self.setWindowTitle("Кафе")
        self.resize(800, 450)

        self.menu = [
            MenuItem("Кофе", 3),
            MenuItem("Чай", 2.5),
            MenuItem("Сэндвич", 5),
            MenuItem("Торт", 4)
        ]
        self.waiters = [Waiter("Алишер"), Waiter("Айдана")]
        self.order = []
        self.all_orders = []

        self.menu_list = QListWidget()
        for item in self.menu:
            self.menu_list.addItem(f"{item.name} - {item.price} $")

        self.order_list = QListWidget()

        self.waiter_combo = QComboBox()
        for w in self.waiters:
            self.waiter_combo.addItem(w.name)

        self.table_combo = QComboBox()
        for i in range(1, 11):
            self.table_combo.addItem(f"Стол {i}")

        self.add_button = QPushButton("Добавить в заказ")
        self.remove_button = QPushButton("Удалить из заказа")
        self.total_button = QPushButton("Рассчитать итог")
        self.report_button = QPushButton("Показать отчёт")

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
        order_layout.addWidget(QLabel("Стол"))
        order_layout.addWidget(self.table_combo)
        order_layout.addWidget(self.total_button)
        order_layout.addWidget(self.report_button)

        main_layout = QHBoxLayout()
        main_layout.addLayout(menu_layout)
        main_layout.addLayout(order_layout)
        self.setLayout(main_layout)

        self.add_button.clicked.connect(self.add_item)
        self.remove_button.clicked.connect(self.remove_item)
        self.total_button.clicked.connect(self.calculate_total)
        self.report_button.clicked.connect(self.show_report)

    def add_item(self):
        selected = self.menu_list.currentRow()
        if selected >= 0:
            quantity, ok = QInputDialog.getInt(
                self, "Количество",
                f"Введите количество для {self.menu[selected].name}:",
                1, 1, 100
            )
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
            table = self.table_combo.currentText()
            QMessageBox.information(
                self,
                "Итог",
                f"Официант: {waiter}\nСтол: {table}\nОбщая сумма: {total_after_discount:.2f} $"
            )
            current_order = self.order.copy()
            self.save_receipt(waiter, table, total, discount, total_after_discount, current_order)
            self.all_orders.append({
                "waiter": waiter,
                "table": table,
                "total": total_after_discount
            })
            self.order = []
            self.order_list.clear()

    def save_receipt(self, waiter, table, total, discount, total_after_discount, order_items):
        now = datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
        filename = f"receipt_{now}.txt"
        with open(filename, "w", encoding="utf-8") as f:
            f.write("==== ЧЕК ====\n")
            f.write(f"Дата: {datetime.now()}\n")
            f.write(f"Стол: {table}\n")
            f.write(f"Официант: {waiter}\n\n")
            f.write("Заказ:\n")
            for item, qty in order_items:
                f.write(f"- {item.name} x{qty} = {item.price * qty}$\n")
            f.write(f"\nСумма без скидки: {total}$\n")
            f.write(f"Скидка: {discount}%\n")
            f.write(f"Итоговая сумма: {total_after_discount}$\n")
            f.write("=================\n")
        QMessageBox.information(self, "Сохранено", f"Чек сохранён как:\n{filename}")

    def show_report(self):
        if not self.all_orders:
            QMessageBox.information(self, "Отчёт", "Нет заказов для отчёта")
            return
        total_income = sum(o["total"] for o in self.all_orders)
        waiter_income = {w.name: 0 for w in self.waiters}
        for o in self.all_orders:
            waiter_income[o["waiter"]] += o["total"]
        report_text = f"Общий доход кафе: {total_income:.2f} $\n\nДоход по официантам:\n"
        for w, income in waiter_income.items():
            report_text += f"- {w}: {income:.2f} $\n"
        QMessageBox.information(self, "Отчёт", report_text)

if __name__ == "__main__":
    app = QApplication([])
    window = CafeApp()
    window.show()
    app.exec()
