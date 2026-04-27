import tkinter as tk
from tkinter import ttk, messagebox
import json
from datetime import datetime


class ExpenseTracker:
    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker")
        self.expenses = self.load_data()

        # Поля ввода
        tk.Label(root, text="Сумма:").grid(row=0, column=0)
        self.amount_entry = tk.Entry(root)
        self.amount_entry.grid(row=0, column=1)

        tk.Label(root, text="Категория:").grid(row=1, column=0)
        self.category_cb = ttk.Combobox(root, values=["Еда", "Транспорт", "Развлечения", "Другое"])
        self.category_cb.grid(row=1, column=1)

        tk.Label(root, text="Дата (ГГГГ-ММ-ДД):").grid(row=2, column=0)
        self.date_entry = tk.Entry(root)
        self.date_entry.insert(0, datetime.now().strftime("%Y-%m-%d"))
        self.date_entry.grid(row=2, column=1)

        # Кнопки
        tk.Button(root, text="Добавить расход", command=self.add_expense).grid(row=3, column=0, columnspan=2, pady=10)

        # Таблица
        self.tree = ttk.Treeview(root, columns=("Сумма", "Категория", "Дата"), show='headings')
        self.tree.heading("Сумма", text="Сумма")
        self.tree.heading("Категория", text="Категория")
        self.tree.heading("Дата", text="Дата")
        self.tree.grid(row=4, column=0, columnspan=2)

        # Фильтры и итог
        tk.Button(root, text="Показать всё", command=self.update_table).grid(row=5, column=0)
        self.total_label = tk.Label(root, text="Итого: 0", font=('Arial', 10, 'bold'))
        self.total_label.grid(row=5, column=1)

        self.update_table()

    def add_expense(self):
        amount = self.amount_entry.get()
        category = self.category_cb.get()
        date_str = self.date_entry.get()

        # Валидация
        try:
            amount = float(amount)
            if amount <= 0: raise ValueError
            datetime.strptime(date_str, "%Y-%m-%d")
        except ValueError:
            messagebox.showerror("Ошибка", "Проверьте корректность суммы и даты (ГГГГ-ММ-ДД)")
            return

        new_expense = {"amount": amount, "category": category, "date": date_str}
        self.expenses.append(new_expense)
        self.save_data()
        self.update_table()

        # Очистка полей
        self.amount_entry.delete(0, tk.END)

    def update_table(self, data_to_show=None):
        for i in self.tree.get_children():
            self.tree.delete(i)

        display_data = data_to_show if data_to_show is not None else self.expenses
        total = 0
        for item in display_data:
            self.tree.insert("", tk.END, values=(item['amount'], item['category'], item['date']))
            total += item['amount']

        self.total_label.config(text=f"Итого: {total:.2f}")

    def save_data(self):
        with open("expenses.json", "w", encoding="utf-8") as f:
            json.dump(self.expenses, f, ensure_ascii=False, indent=4)

    def load_data(self):
        try:
            with open("expenses.json", "r", encoding="utf-8") as f:
                return json.load(f)
        except (FileNotFoundError, json.JSONDecodeError):
            return []


if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTracker(root)
    root.mainloop()