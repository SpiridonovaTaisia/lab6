import tkinter as tk
from tkinter import messagebox
import sqlite3


# Создаем базу данных и таблицу пользователей.
#Функция create_db() создает базу данных users.db и таблицу users, если они еще не существуют.
def create_db():
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('''
        CREATE TABLE IF NOT EXISTS users (
            id INTEGER PRIMARY KEY,
            username TEXT UNIQUE,
            password TEXT
        )
    ''')
    conn.commit()
    conn.close()


# Функция для регистрации пользователя
# Функция register_user() добавляет нового пользователя в базу данных.
# Если логин уже существует, выводится ошибка.
def register_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    try:
        cursor.execute('INSERT INTO users (username, password) VALUES (?, ?)', (username, password))
        conn.commit()
        messagebox.showinfo("Регистрация", "Пользователь зарегистрирован успешно!")
    except sqlite3.IntegrityError:
        messagebox.showerror("Ошибка", "Пользователь с таким логином уже существует.")
    finally:
        conn.close()


# Функция для авторизации пользователя
#Функция login_user() проверяет введенные логин и пароль.
# Если они совпадают с данными в базе, выводится сообщение об успешной авторизации.
def login_user(username, password):
    conn = sqlite3.connect('users.db')
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM users WHERE username=? AND password=?', (username, password))
    user = cursor.fetchone()
    if user:
        messagebox.showinfo("Авторизация", "Авторизация прошла успешно!")
    else:
        messagebox.showerror("Ошибка", "Неверный логин или пароль.")
    conn.close()


# Окно регистрации
# Функция open_registration_window() открывает новое окно для регистрации.
def open_registration_window():
    reg_window = tk.Toplevel(root)
    reg_window.title("Регистрация")

    tk.Label(reg_window, text="Логин").pack()
    username_entry = tk.Entry(reg_window)
    username_entry.pack()

    tk.Label(reg_window, text="Пароль").pack()
    password_entry = tk.Entry(reg_window, show='*')
    password_entry.pack()

    tk.Button(reg_window, text="Зарегистрироваться",
              command=lambda: register_user(username_entry.get(), password_entry.get())).pack()


# Основное окно авторизации
# В главном окне создаются поля для ввода логина и пароля,
# а также кнопки для авторизации и открытия окна регистрации.
root = tk.Tk()
root.title("Авторизация")

tk.Label(root, text="Логин").pack()
login_username_entry = tk.Entry(root)
login_username_entry.pack()

tk.Label(root, text="Пароль").pack()
login_password_entry = tk.Entry(root, show='*')
login_password_entry.pack()

tk.Button(root, text="Авторизоваться",
          command=lambda: login_user(login_username_entry.get(), login_password_entry.get())).pack()
tk.Button(root, text="Регистрация", command=open_registration_window).pack()

create_db()  # Создаем базу данных при запуске приложения

root.mainloop()

