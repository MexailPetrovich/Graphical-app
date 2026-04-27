import tkinter as tk
from tkinter import ttk, messagebox
import json
import os

# ---------- Файл для хранения данных ----------
DATA_FILE = "movies.json"

# ---------- Класс приложения ----------
class MovieLibrary:
    def __init__(self, root):
        self.root = root
        self.root.title("Movie Library - Личная кинотека")
        self.root.geometry("800x500")

        # Данные
        self.movies = []
        self.load_data()

        # Виджеты
        self.create_input_frame()
        self.create_filter_frame()
        self.create_table()

        # Отобразить все фильмы
        self.refresh_table()

    # ---------- Загрузка / сохранение JSON ----------
    def load_data(self):
        if os.path.exists(DATA_FILE):
            try:
                with open(DATA_FILE, "r", encoding="utf-8") as f:
                    self.movies = json.load(f)
            except:
                self.movies = []
        else:
            self.movies = []

    def save_data(self):
        with open(DATA_FILE, "w", encoding="utf-8") as f:
            json.dump(self.movies, f, ensure_ascii=False, indent=4)

    # ---------- Форма добавления ----------
    def create_input_frame(self):
        frame = tk.LabelFrame(self.root, text="Добавить фильм", padx=10, pady=10)
        frame.pack(fill="x", padx=10, pady=5)

        # Название
        tk.Label(frame, text="Название:").grid(row=0, column=0, sticky="w")
        self.title_entry = tk.Entry(frame, width=30)
        self.title_entry.grid(row=0, column=1, padx=5)

        # Жанр
        tk.Label(frame, text="Жанр:").grid(row=0, column=2, sticky="w")
        self.genre_entry = tk.Entry(frame, width=20)
        self.genre_entry.grid(row=0, column=3, padx=5)

        # Год
        tk.Label(frame, text="Год выпуска:").grid(row=1, column=0, sticky="w")
        self.year_entry = tk.Entry(frame, width=10)
        self.year_entry.grid(row=1, column=1, padx=5)

        # Рейтинг
        tk.Label(frame, text="Рейтинг (0-10):").grid(row=1, column=2, sticky="w")
        self.rating_entry = tk.Entry(frame, width=10)
        self.rating_entry.grid(row=1, column=3, padx=5)

        # Кнопка добавления
        tk.Button(frame, text="➕ Добавить фильм", command=self.add_movie, bg="lightgreen").grid(row=1, column=4, padx=20)

    # ---------- Проверка ввода ----------
    def validate_movie_data(self, title, genre, year_str, rating_str):
        if not title or not genre:
            messagebox.showerror("Ошибка", "Название и жанр не могут быть пустыми")
            return False

        try:
            year = int(year_str)
            if year < 1888 or year > 2100:  # 1888 — первый фильм
                messagebox.showerror("Ошибка", "Год должен быть между 1888 и 2100")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Год должен быть числом")
            return False

        try:
            rating = float(rating_str)
            if rating < 0 or rating > 10:
                messagebox.showerror("Ошибка", "Рейтинг должен быть от 0 до 10")
                return False
        except ValueError:
            messagebox.showerror("Ошибка", "Рейтинг должен быть числом")
            return False

        return True

    def add_movie(self):
        title = self.title_entry.get().strip()
        genre = self.genre_entry.get().strip()
        year = self.year_entry.get().strip()
        rating = self.rating_entry.get().strip()

        if not self.validate_movie_data(title, genre, year, rating):
            return

        movie = {
            "title": title,
            "genre": genre,
            "year": int(year),
            "rating": float(rating)
        }

        self.movies.append(movie)
        self.save_data()
        self.refresh_table()

        # Очистка полей
        self.title_entry.delete(0, tk.END)
        self.genre_entry.delete(0, tk.END)
        self.year_entry.delete(0, tk.END)
        self.rating_entry.delete(0, tk.END)

        messagebox.showinfo("Успех", "Фильм добавлен!")

    # ---------- Фильтрация ----------
    def create_filter_frame(self):
        frame = tk.LabelFrame(self.root, text="Фильтрация", padx=10, pady=10)
        frame.pack(fill="x", padx=10, pady=5)

        tk.Label(frame, text="Фильтр по жанру:").grid(row=0, column=0)
        self.filter_genre_entry = tk.Entry(frame, width=20)
        self.filter_genre_entry.grid(row=0, column=1, padx=5)

        tk.Label(frame, text="Фильтр по году:").grid(row=0, column=2)
        self.filter_year_entry = tk.Entry(frame, width=10)
        self.filter_year_entry.grid(row=0, column=3, padx=5)

        tk.Button(frame, text="🔍 Применить фильтр", command=self.refresh_table).grid(row=0, column=4, padx=10)
        tk.Button(frame, text="❌ Сбросить фильтр", command=self.clear_filter).grid(row=0, column=5)

    def clear_filter(self):
        self.filter_genre_entry.delete(0, tk.END)
        self.filter_year_entry.delete(0, tk.END)
        self.refresh_table()

    def get_filtered_movies(self):
        genre_filter = self.filter_genre_entry.get().strip().lower()
        year_filter = self.filter_year_entry.get().strip()

        filtered = self.movies[:]

        if genre_filter:
            filtered = [m for m in filtered if genre_filter in m["genre"].lower()]

        if year_filter:
            try:
                year_int = int(year_filter)
                filtered = [m for m in filtered if m["year"] == year_int]
            except ValueError:
                pass  # если не число — игнорируем фильтр по году

        return filtered

    # ---------- Таблица ----------
    def create_table(self):
        self.tree_frame = tk.Frame(self.root)
        self.tree_frame.pack(fill="both", expand=True, padx=10, pady=5)

        columns = ("Название", "Жанр", "Год", "Рейтинг")
        self.tree = ttk.Treeview(self.tree_frame, columns=columns, show="headings")

        for col in columns:
            self.tree.heading(col, text=col)
            self.tree.column(col, width=150)

        scrollbar = ttk.Scrollbar(self.tree_frame, orient="vertical", command=self.tree.yview)
        self.tree.configure(yscrollcommand=scrollbar.set)

        self.tree.pack(side="left", fill="both", expand=True)
        scrollbar.pack(side="right", fill="y")

    def refresh_table(self):
        # Очистить таблицу
        for row in self.tree.get_children():
            self.tree.delete(row)

        filtered_movies = self.get_filtered_movies()

        for movie in filtered_movies:
            self.tree.insert("", "end", values=(
                movie["title"],
                movie["genre"],
                movie["year"],
                movie["rating"]
            ))

# ---------- Запуск приложения ----------
if __name__ == "__main__":
    root = tk.Tk()
    app = MovieLibrary(root)
    root.mainloop()