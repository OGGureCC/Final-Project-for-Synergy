import sqlite3
import tkinter as tk
from tkinter import ttk

# Класс главного окна
class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.init_main()
        self.db = db
        self.view_records()


    # Cоздание и работа с главным окном
    def init_main(self):
        toolbar = tk.Frame(bg='#d7d7d7', bd=2)  # Создаем панель инструментов
        toolbar.pack(side=tk.TOP, fill=tk.X)  # Упаковываем панель инструментов

        # Открытие нового окна по кнопке Добавить
        self.add_img = tk.PhotoImage(file = './img/add.png')
        btn_add = tk.Button(toolbar, bg = '#d7d7d7', bd = 0, width = 72,
                            image = self.add_img, command = self.add_child)
        btn_add.pack(side = tk.LEFT, padx = 27)

        # Открытие нового окна по кнопке Редактировать
        # Редактирование выбранной записи
        self.edit_img = tk.PhotoImage(file = './img/edit.png')
        btn_edit = tk.Button(toolbar, bg = '#d7d7d7', bd = 0, width = 72,
                             image = self.edit_img, command = self.edit_child)
        btn_edit.pack(side = tk.LEFT, padx = 27)

        # Удаление выбранных записей
        self.delete_img = tk.PhotoImage(file = './img/delete.png')
        btn_delete = tk.Button(toolbar, bg = '#d7d7d7', bd = 0, width = 72,
                               image = self.delete_img, command = self.delete_record)
        btn_delete.pack(side = tk.LEFT, padx = 27)

        # Открытие нового окна по кнопке Поиск
        self.search_img = tk.PhotoImage(file = './img/search.png')
        btn_search = tk.Button(toolbar, bg = '#d7d7d7', bd = 0, width = 72,
                               image = self.search_img, command = self.search_child)
        btn_search.pack(side = tk.LEFT, padx = 27)

        # Обновить список записей
        self.refresh_img = tk.PhotoImage(file = './img/refresh.png')
        btn_refresh = tk.Button(toolbar, bg = '#d7d7d7', bd = 0, width = 72,
                               image = self.refresh_img, command = self.view_records)
        btn_refresh.pack(side = tk.LEFT, padx = 27)

        # Добавляем Treeview
        self.tree = ttk.Treeview(self, columns= ('id_user', 'name', 'phone', 'email', 'salary'),
                                 height = 45, show = 'headings')
        
        # Добавляем параметры колонкам
        self.tree.column('id_user', width = 30, anchor = tk.CENTER)
        self.tree.column('name', width = 250, anchor = tk.CENTER)
        self.tree.column('phone', width = 100, anchor = tk.CENTER)
        self.tree.column('email', width = 150, anchor = tk.CENTER)
        self.tree.column('salary', width = 100, anchor = tk.CENTER)

        # Подписи колонок
        self.tree.heading('id_user', text = 'ID')
        self.tree.heading('name', text = 'ФИО')
        self.tree.heading('phone', text = 'Телефон')
        self.tree.heading('email', text = 'E-mail')
        self.tree.heading('salary', text = 'Зарплата')

        # Упаковка Treeview
        self.tree.pack(side = tk.LEFT)

        # Скроллбар для таблицы
        scroll = tk.Scrollbar(self, command=self.tree.yview)
        scroll.pack(side=tk.LEFT, fill=tk.Y)
        self.tree.configure(yscrollcommand=scroll.set)

    # Создание окна по центру экрана
    def center_window(self, width, height):
        screen_width = self.winfo_screenwidth()
        screen_height = self.winfo_screenheight()
        x = (screen_width - width) // 2
        y = (screen_height - height) // 2
        return f'{width}x{height}+{x}+{y}'
    
    # Запись в БД
    def records(self, name, phone, email, salary):
        self.db.insert_data(name, phone, email, salary)
        self.view_records()

    # Отображение данных из БД в Treeview
    def view_records(self):
        self.db.cursor.execute(
            '''
            SELECT * FROM Employees
            '''
        )
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values = row)
         for row in self.db.cursor.fetchall()]
        
    # Редактирование записей
    def edit_record(self, name, phone, email, salary):
        # Записывает id выбранной записи
        # self.tree.selection() возвращает список выбранных элементов, 
        # но благодаря [0] это будет первый (и единственный) выбранный элемент в виджете
        # self.tree.set() используется для получения значения в указанном столбце, т.е в 1 столбце --> id
        id = self.tree.set(self.tree.selection()[0], '#1')
        self.db.cursor.execute(
            '''
            UPDATE Employees SET name = ?, phone = ?, email = ?, salary = ? WHERE id_employee = ?
            ''', (name, phone, email, salary, id)
        )
        self.db.connection.commit()
        self.view_records()

    # Удаление из БД
    def delete_record(self):
        for selection_item in self.tree.selection():
            self.db.cursor.execute(
                '''
                DELETE FROM Employees WHERE id_employee = ?
                ''', (self.tree.set(selection_item, '#1'), ))
        self.db.connection.commit()
        self.view_records()

    # Поиск записей
    def search_records(self, sname):
        name = (f'%{sname}%')
        self.db.cursor.execute(
            '''
            SELECT * FROM Employees WHERE name LIKE (?)
            ''', (name, )
        )
        [self.tree.delete(i) for i in self.tree.get_children()]
        [self.tree.insert('', 'end', values = row)
         for row in self.db.cursor.fetchall()]

    # Вызовы дочерних окон
    def add_child(self):
        Child()

    def edit_child(self):
        Edit()

    def search_child(self):
        Search()

# Главный класс для всех дочерних окон + класс окна добавления записей
class Child(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.view = app
        self.init_child()

    # Cоздание и работа с дочерним окном
    def init_child(self):
        self.title('Добавить сотрудника')
        # Устанавливаем размер и центрируем дочернее окно
        child_width = 400
        child_height = 200
        child_geometry = self.view.center_window(child_width, child_height)
        self.geometry(child_geometry)
        self.resizable(width = False, height = False)

        # Перехват всех событий и фокуса в приложении
        self.grab_set()
        self.focus_set()

        # Подписи к полям
        # .place позволяет прописать точные координаты виджета
        # в отличие от .pack() или .grid(), в последнем координаты созданной сетки разве что
        label_name = tk.Label(self, text = 'ФИО:')
        label_name.place(x = 50, y = 30)
        label_phone = tk.Label(self, text = 'Телефон:')
        label_phone.place(x = 50, y = 60)
        label_email = tk.Label(self, text = 'E-mail:')
        label_email.place(x = 50, y = 90)
        label_salary = tk.Label(self, text = 'Зарплата:')
        label_salary.place(x = 50, y = 120)

        # Поля для ввода имени, email и телефона
        self.entry_name = ttk.Entry(self)
        self.entry_name.place(x = 200, y = 30, width = 146)
        self.entry_phone = ttk.Entry(self)
        self.entry_phone.place(x = 200, y = 60, width = 146)
        self.entry_email = ttk.Entry(self)
        self.entry_email.place(x = 200, y = 90, width = 146)
        self.entry_salary = ttk.Entry(self)
        self.entry_salary.place(x = 200, y = 120, width = 146)

        # Кнопка закрытия дочернего окна
        # Не понимаю смысла этой кнопки, если есть кнопка Х у самого окна, я бы её закомментил просто, а лучше вообще не добавлял,
        # но если надо, то пускай остается
        self.btn_cancel = ttk.Button(self, text = 'Закрыть', command = self.destroy)
        self.btn_cancel.place(x = 280, y = 170)

        # Кнопка добавления записи
        self.btn_add = ttk.Button(self, text = 'Добавить')
        self.btn_add.place(x = 200, y = 170)
        self.btn_add.bind('<Button-1>', lambda event: self.view.records(self.entry_name.get(),
                                                                        self.entry_phone.get(),
                                                                        self.entry_email.get(),
                                                                        self.entry_salary.get()))
        # Очистка полей ввода после добавления записи
        # add = '+' позваляет на одну кнопку вешать более одного события
        self.btn_add.bind('<Button-1>', lambda event: self.entry_name.delete(0, tk.END), add = '+')
        self.btn_add.bind('<Button-1>', lambda event: self.entry_phone.delete(0, tk.END), add = '+')
        self.btn_add.bind('<Button-1>', lambda event: self.entry_email.delete(0, tk.END), add = '+')
        self.btn_add.bind('<Button-1>', lambda event: self.entry_salary.delete(0, tk.END), add = '+')


# Класс окна редактирования записей
# Считаю, что для редактирования подходит edit, а не update, т.к это прямой перевод слова.
class Edit(Child):
    def __init__(self):
        super().__init__()
        self.init_edit()
        self.db = db
        self.default_data()

    def init_edit(self):
        self.title('Редактировать сотрудника')
        self.btn_add.destroy()
        self.btn_edit = ttk.Button(self, text = 'Редактировать')
        self.btn_edit.bind('<Button-1>', lambda event: self.view.edit_record(self.entry_name.get(),
                                                                              self.entry_phone.get(),
                                                                              self.entry_email.get(),
                                                                              self.entry_salary.get()))
        # Закрыть окно после редактирования
        self.btn_edit.bind('<Button-1>', lambda event: self.destroy(), add = '+')
        self.btn_edit.place(x = 200, y = 170)
        self.btn_cancel.place(x = 294, y = 170)

    def default_data(self):
        # См. 102-105 строки
        id = self.view.tree.set(self.view.tree.selection()[0], '#1')
        self.db.cursor.execute(
            '''
            SELECT * FROM Employees WHERE id_employee = ?
            ''', (id, )
            )
        row = self.db.cursor.fetchone()
        self.entry_name.insert(0, row[1])
        self.entry_phone.insert(0, row[2])
        self.entry_email.insert(0, row[3])
        self.entry_salary.insert(0, row[4])

class Search(tk.Toplevel):
    def __init__(self):
        super().__init__(root)
        self.view = app
        self.init_search()

    def init_search(self):
        self.title('Поиск по сотрудникам')
        # Устанавливаем размер и центрируем окно
        search_width = 300
        search_height = 100
        search_geometry = self.view.center_window(search_width, search_height)
        self.geometry(search_geometry)
        self.resizable(width = False, height = False)

        # Перехват всех событий и фокуса в приложении
        self.grab_set()
        self.focus_set()

        # Название
        label_search = tk.Label(self, text='Поиск')
        label_search.place(x = 47.5, y = 20)
        
        # Поле
        self.entry_search = ttk.Entry(self)
        self.entry_search.place(x = 92.5, y = 20, width = 155)

        # Кнопки
        btn_cancel = ttk.Button(self, text='Закрыть', command = self.destroy)
        btn_cancel.place(x = 172.5, y = 50)

        btn_search = ttk.Button(self, text='Поиск')
        # Пришлось писать 92.4, а не 92.5, потому что кнопка была на пиксель левее,
        # а теперь всё ровно и идеально по центру
        btn_search.place(x = 92.4, y = 50)
        btn_search.bind('<Button-1>', 
                        lambda event: self.view.search_records(self.entry_search.get()))
        btn_search.bind('<Button-1>', 
                        lambda event: self.destroy(), add='+')


# Класс БД
class DB:
    def __init__(self):
        self.connection = sqlite3.connect('employees.db')
        self.cursor = self.connection.cursor()
        self.cursor.execute(
            '''
                            CREATE TABLE IF NOT EXISTS Employees (
                            id_employee INTEGER PRIMARY KEY,
                            name TEXT NOT NULL,
                            phone TEXT NOT NULL,
                            email TEXT NOT NULL,
                            salary INTEGER
                            )
            '''
        )
        self.connection.commit()

    # Запись в БД
    def insert_data(self, name, phone, email, salary):
        self.cursor.execute(
            '''
            INSERT INTO Employees (name, phone, email, salary)
            VALUES (?, ?, ?, ?)
            ''', (name, phone, email, salary)
        )
        self.connection.commit()


# Создание окна
# if __name__ == '__main__': позволяет запускать код из этого блока только если файл запущен напрямую
# Если файл импортирован куда-то, то этот кусок кода игнорируется
if __name__ == '__main__':
    root = tk.Tk()
    db = DB()
    app = Main(root)
    app.pack()
    root.title('Список сотрудников компании')
    # Устанавливаем размер и центрируем главное окно
    main_width = 645
    main_height = 450
    root.geometry(app.center_window(main_width, main_height))
    root.resizable(width = False, height = False)
    root.configure(bg = '#ffffff')
    root.mainloop()