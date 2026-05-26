import json
import os
import tkinter as tk
from tkinter import messagebox, ttk


class BookTrackerApp:

    def __init__(self, root):
        self.root = root
        self.root.title("Book Tracker — Трекер прочитанных книг")
        self.root.geometry("800x550")
        self.root.minsize(700, 450)

        self.file_name = "books.json"
        # Список для хранения всех книг (словари)
        self.books = []

        # Инициализация графического интерфейса
        self.create_widgets()

        # Загрузка сохраненных данных при старте программы
        self.load_data()

    def create_widgets(self):
        """Создание всех элементов GUI."""
        # --- Панель ввода данных ---
        input_frame = tk.LabelFrame(
            self.root, text=" Добавить новую книгу ", padx=15, pady=10
        )
        input_frame.pack(fill="x", padx=15, pady=10)

        tk.Label(input_frame, text="Название книги:").grid(
            row=0, column=0, sticky="w", pady=5
        )
        self.title_entry = tk.Entry(input_frame, width=25)
        self.title_entry.grid(row=0, column=1, padx=10, pady=5)

        tk.Label(input_frame, text="Автор:").grid(
            row=0, column=2, sticky="w", pady=5
        )
        self.author_entry = tk.Entry(input_frame, width=25)
        self.author_entry.grid(row=0, column=3, padx=10, pady=5)

        tk.Label(input_frame, text="Жанр:").grid(
            row=1, column=0, sticky="w", pady=5
        )
        self.genre_entry = tk.Entry(input_frame, width=25)
        self.genre_entry.grid(row=1, column=1, padx=10, pady=5)

        tk.Label(input_frame, text="Количество страниц:").grid(
            row=1, column=2, sticky="w", pady=5
        )
        self.pages_entry = tk.Entry(input_frame, width=25)
        self.pages_entry.grid(row=1, column=3, padx=10, pady=5)

        # Кнопка «Добавить книгу»
        add_btn = tk.Button(
            input_frame,
            text="Добавить книгу",
            command=self.add_book,
            bg="#4CAF50",
            fg="white",
            font=("Arial", 10, "bold"),
            padx=10,
        )
        add_btn.grid(row=0, column=4, rowspan=2, padx=15, pady=5, sticky="ns")

        # --- Панель фильтрации ---
        filter_frame = tk.LabelFrame(
            self.root, text=" Фильтрация списка ", padx=15, pady=10
        )
        filter_frame.pack(fill="x", padx=15, pady=5)

        tk.Label(filter_frame, text="По жанру:").grid(row=0, column=0, sticky="w")
        self.filter_genre_entry = tk.Entry(filter_frame, width=18)
        self.filter_genre_entry.grid(row=0, column=1, padx=10)

        tk.Label(filter_frame, text="Страниц (от):").grid(
            row=0, column=2, sticky="w"
        )
        self.filter_pages_entry = tk.Entry(filter_frame, width=10)
        self.filter_pages_entry.grid(row=0, column=3, padx=10)

        filter_btn = tk.Button(
            filter_frame,
            text="Применить фильтр",
            command=self.apply_filter,
            bg="#2196F3",
            fg="white",
        )
        filter_btn.grid(row=0, column=4, padx=10)

        reset_btn = tk.Button(
            filter_frame,
            text="Сбросить",
            command=self.reset_filter,
            bg="#f44336",
            fg="white",
        )
        reset_btn.grid(row=0, column=5, padx=5)

        # --- Таблица (Treeview) для отображения добавленных книг ---
        table_frame = tk.Frame(self.root)
        table_frame.pack(fill="both", expand=True, padx=15, pady=10)

        columns = ("title", "author", "genre", "pages")
        self.tree = ttk.Treeview(table_frame, columns=columns, show="headings")

        # Заголовки столбцов таблицы
        self.tree.heading("title", text="Название книги")
        self.tree.heading("author", text="Автор")
        self.tree.heading("genre", text="Жанр")
        self.tree.heading("pages", text="Кол-во страниц")

        # Настройка размеров столбцов
        self.tree.column("title", width=250, anchor="w")
        self.tree.column("author", width=180, anchor="w")
        self.tree.column("genre", width=140, anchor="w")
        self.tree.column("pages", width=100, anchor="center")

        # Скроллбар для прокрутки таблицы
        scrollbar = ttk.Scrollbar(
            table_frame, orient="vertical", command=self.tree.yview
        )
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    # --- Логика валидации и добавления данных ---
    def add_book(self):
        """Считывает данные полей, проверяет их корректность и добавляет книгу."""
        title = self.title_entry.get().strip()
        author = self.author_entry.get().strip()
        genre = self.genre_entry.get().strip()
        pages_raw = self.pages_entry.get().strip()

        # 1. Валидация: проверка на обязательные пустые поля
        if not (title and author and genre and pages_raw):
            messagebox.showerror(
                "Ошибка ввода", "Все поля формы должны быть заполнены!"
            )
            return

        # 2. Валидация: проверка числового типа данных для количества страниц
        try:
            pages = int(pages_raw)
            if pages <= 0:
                raise ValueError
        except ValueError:
            messagebox.showerror(
                "Ошибка ввода",
                "Поле 'Количество страниц' должно быть целым положительным числом!",
            )
            return

        # Формирование словаря новой книги
        new_book = {
            "title": title,
            "author": author,
            "genre": genre,
            "pages": pages,
        }

        self.books.append(new_book)

        # Сохранение и обновление таблицы
        self.save_data()
        self.update_table(self.books)
        self.clear_input_fields()

    def clear_input_fields(self):
        """Очищает текстовые поля после успешного добавления."""
        self.title_entry.delete(0, tk.END)
        self.author_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.pages_entry.delete(0, tk.END)

    # --- Логика фильтрации списка книг ---
    def apply_filter(self):
        """Фильтрует список книг по совпадению жанра и/или количеству страниц."""
        f_genre = self.filter_genre_entry.get().strip().lower()
        f_pages_raw = self.filter_pages_entry.get().strip()

        filtered_list = self.books

        # Фильтр по жанру (частичное совпадение букв)
        if f_genre:
            filtered_list = [
                b for b in filtered_list if f_genre in b["genre"].lower()
            ]

        # Фильтр по количеству страниц (вывод книг со страницами больше или равно значению)
        if f_pages_raw:
            try:
                min_pages = int(f_pages_raw)
                filtered_list = [
                    b for b in filtered_list if b["pages"] >= min_pages
                ]
            except ValueError:
                messagebox.showwarning(
                    "Ошибка фильтра",
                    "Критерий количества страниц должен быть целым числом!",
                )
                return

        self.update_table(filtered_list)

    def reset_filter(self):
        """Сбрасывает установленные фильтры и возвращает полный список книг."""
        self.filter_genre_entry.delete(0, tk.END)
        self.filter_pages_entry.delete(0, tk.END)
        self.update_table(self.books)

    def update_table(self, data_list):
        """Перерисовывает строки таблицы Treeview."""
        # Очистка старых данных из интерфейса
        for item in self.tree.get_children():
            self.tree.delete(item)

        # Заполнение новыми данными
        for b in data_list:
            self.tree.insert(
                "",
                tk.END,
                values=(b["title"], b["author"], b["genre"], b["pages"]),
            )

    # --- Сохранение и загрузка JSON с обработкой исключений ---
    def save_data(self):
        """Записывает актуальный список книг в файл JSON с перехватом ошибок ввода-вывода."""
        try:
            with open(self.file_name, "w", encoding="utf-8") as f:
                json.dump(self.books, f, ensure_ascii=False, indent=4)
        except IOError as e:
            messagebox.showerror(
                "Ошибка сохранения",
                f"Не удалось записать данные в файл books.json:\n{e}",
            )
        except Exception as e:
            messagebox.showerror(
                "Неизвестная ошибка", f"Произошла системная ошибка: {e}"
            )

    def load_data(self):
        """Загружает данные из файла JSON при старте программы с обработкой исключений."""
        if os.path.exists(self.file_name):
            try:
                with open(self.file_name, "r", encoding="utf-8") as f:
                    self.books = json.load(f)
                self.update_table(self.books)
            except json.JSONDecodeError:
                messagebox.showwarning(
                    "Ошибка структуры данных",
                    "Файл books.json поврежден или пуст. Создан новый список.",
                )
                self.books = []
            except PermissionError:
                messagebox.showerror(
                    "Ошибка доступа", "Недостаточно прав для чтения файла books.json!"
                )
                self.books = []
            except Exception as e:
                messagebox.showerror(
                    "Ошибка загрузки", f"Не удалось загрузить данные:\n{e}"
                )
                self.books = []


# --- Обязательная точка входа в приложение ---
if __name__ == "__main__":
    root = tk.Tk()
    app = BookTrackerApp(root)
    root.mainloop()