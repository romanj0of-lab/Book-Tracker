import json
import os
import tkinter as tk
from datetime import datetime
from tkinter import messagebox, ttk


class ExpenseTrackerApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Expense Tracker — Трекер расходов")
        self.root.geometry("850x650")
        self.root.minsize(800, 500)

        self.file_name = "expenses.json"
        self.expenses = []

        self.create_widgets()
        self.load_data()

    def create_widgets(self):
        """Создание элементов GUI."""
        # --- Панель ввода данных ---
        input_frame = tk.LabelFrame(
            self.root, text=" Добавить новый расход ", padx=15, pady=10
        )
        input_frame.pack(fill="x", padx=15, pady=10)

        tk.Label(input_frame, text="Сумма:").grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.amount_entry = tk.Entry(input_frame, width=20)
        self.amount_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(input_frame, text="Категория:").grid(
            row=0, column=2, sticky="w", pady=5
        )
        self.category_combobox = ttk.Combobox(
            input_frame,
            values=["Еда", "Транспорт", "Развлечения", "Коммунальные", "Другое"],
            width=17,
        )
        self.category_combobox.grid(row=0, column=3, padx=10, pady=5)
        self.category_combobox.set("Еда")

        tk.Label(input_frame, text="Дата (ДД.ММ.ГГГГ):").grid(
            row=1, column=0, sticky="w", pady=5
        )
        self.date_entry = tk.Entry(input_frame, width=20)
        self.date_entry.grid(row=1, column=1, padx=10, pady=5)
        self.date_entry.insert(0, datetime.now().strftime("%d.%m.%Y"))

        add_btn = tk.Button(
            input_frame,
            text="Добавить расход",
            command=self.add_expense,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
        )
        add_btn.grid(row=0, column=4, rowspan=2, padx=20, pady=5, sticky="ns")

        # --- Панель фильтрации ---
        filter_frame = tk.LabelFrame(
            self.root,
            text=" Фильтрация и подсчёт суммы за период ",
            padx=15,
            pady=10,
        )
        filter_frame.pack(fill="x", padx=15, pady=5)

        tk.Label(filter_frame, text="Категория:").grid(
            row=0, column=0, sticky="w", pady=2
        )
        self.filter_cat_entry = tk.Entry(filter_frame, width=15)
        self.filter_cat_entry.grid(row=0, column=1, padx=5, pady=2)

        tk.Label(filter_frame, text="Дата С (ДД.ММ.ГГГГ):").grid(
            row=0, column=2, sticky="w", pady=2
        )
        self.filter_date_start = tk.Entry(filter_frame, width=12)
        self.filter_date_start.grid(row=0, column=3, padx=5, pady=2)

        tk.Label(filter_frame, text="Дата ПО (ДД.ММ.ГГГГ):").grid(
            row=0, column=4, sticky="w", pady=2
        )
        self.filter_date_end = tk.Entry(filter_frame, width=12)
        self.filter_date_end.grid(row=0, column=5, padx=5, pady=2)

        filter_btn = tk.Button(
            filter_frame,
            text="Применить",
            command=self.apply_filter,
            bg="#2196F3",
            fg="white",
        )
        filter_btn.grid(row=0, column=6, padx=10, pady=2)

        reset_btn = tk.Button(
            filter_frame,
            text="Сбросить",
            command=self.reset_filter,
            bg="#f44336",
            fg="white",
        )
        reset_btn.grid(row=0, column=7, padx=5, pady=2)

        self.total_label = tk.Label(
            self.root,
            text="Итого расходов за выбранный период: 0.00 руб.",
            font=("Arial", 12, "bold"),
            fg="#E91E63",
        )
        self.total_label.pack(anchor="w", padx=20, pady=5)

        # --- Таблица Вывода ---
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=15, pady=10)

        columns = ("amount", "category", "date")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        self.tree.heading("amount", text="Сумма (руб.)")
        self.tree.heading("category", text="Категория")
        self.tree.heading("date", text="Дата")

        self.tree.column("amount", width=150, anchor="center")
        self.tree.column("category", width=250, anchor="w")
        self.tree.column("date", width=150, anchor="center")

        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def add_expense(self):
        amount_raw = self.amount_entry.get().strip()
        category = self.category_combobox.get().strip()
        date_raw = self.date_entry.get().strip()

        if not (amount_raw and category and date_raw):
            messagebox.showerror("Ошибка ввода", "Все поля должны быть заполнены!")
            return

        try:
            amount = float(amount_raw)
            if amount <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Ошибка ввода", "Сумма должна быть положительным числом!"
            )
            return

        try:
            valid_date = datetime.strptime(date_raw, "%d.%m.%Y").strftime(
                "%d.%m.%Y"
            )
        except ValueError:
            messagebox.showerror(
                "Ошибка ввода",
                "Некорректный формат даты! Используйте шаблон: ДД.ММ.ГГГГ",
            )
            return

        new_expense = {"amount": amount, "category": category, "date": valid_date}
        self.expenses.append(new_expense)
        self.save_data()
        self.update_ui(self.expenses)
        self.amount_entry.delete(0, tk.END)

    def apply_filter(self):
        f_cat = self.filter_cat_entry.get().strip().lower()
        f_start_raw = self.filter_date_start.get().strip()
        f_end_raw = self.filter_date_end.get().strip()

        filtered_list = self.expenses

        if f_cat:
            filtered_list = [
                e for e in filtered_list if f_cat in e["category"].lower()
            ]

        try:
            if f_start_raw:
                start_date = datetime.strptime(f_start_raw, "%d.%m.%Y")
                filtered_list = [
                    e
                    for e in filtered_list
                    if datetime.strptime(e["date"], "%d.%m.%Y") >= start_date
                ]
            if f_end_raw:
                end_date = datetime.strptime(f_end_raw, "%d.%m.%Y")
                filtered_list = [
                    e
                    for e in filtered_list
                    if datetime.strptime(e["date"], "%d.%m.%Y") <= end_date
                ]
        except ValueError:
            messagebox.showwarning(
                "Ошибка фильтра",
                "Неверный формат дат в фильтре периода! Используйте ДД.ММ.ГГГГ",
            )
            return

        self.update_ui(filtered_list)

    def reset_filter(self):
        self.filter_cat_entry.delete(0, tk.END)
        self.filter_date_start.delete(0, tk.END)
        self.filter_date_end.delete(0, tk.END)
        self.update_ui(self.expenses)

    def update_ui(self, data_list):
        for item in self.tree.get_children():
            self.tree.delete(item)

        total_sum = 0.0
        for e in data_list:
            self.tree.insert(
                "",
                tk.END,
                values=(f"{e['amount']:.2f}", e["category"], e["date"]),
            )
            total_sum += e["amount"]

        self.total_label.config(
            text=f"Итого расходов за выбранный период: {total_sum:.2f} руб."
        )

    def save_data(self):
        try:
            with open(self.file_name, "w", encoding="utf-8") as f:
                json.dump(self.expenses, f, ensure_ascii=False, indent=4)
        except IOError as e:
            messagebox.showerror(
                "Ошибка сохранения",
                f"Не удалось сохранить данные в файл expenses.json:\n{e}",
            )

    def load_data(self):
        if os.path.exists(self.file_name):
            try:
                with open(self.file_name, "r", encoding="utf-8") as f:
                    self.expenses = json.load(f)
                self.update_ui(self.expenses)
            except Exception:
                self.expenses = []


# --- Обязательная точка входа в приложение ---
if __name__ == "__main__":
    root = tk.Tk()
    app = ExpenseTrackerApp(root)
    root.mainloop()
