import tkinter as tk
from tkinter import ttk
from src.TableItems import User


DAYS = [x for x in range(1, 32)]
MONTH = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
         'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
YEARS = [x for x in range(1950, 2010)]


class AddUser(tk.Toplevel):

    def __init__(self, my_root, app):
        super().__init__(my_root)
        self.main_app = app
        self.entry_first_name = \
            self.entry_last_name = \
            self.combobox_days = \
            self.combobox_month = \
            self.combobox_year = \
            self.button_add = None
        self.init_window()
        self.grab_set()  # Установить фокус на этом окне

    # ==============================================================================================================
    #                                          ГРАФИЧЕСКИЙ ИНТЕРФЕЙС
    # ==============================================================================================================
    def init_window(self):
        self.title('Добавить клиента...')
        self.geometry('360x170+400+400')
        self.resizable(False, False)

        tk.Label(self, text='ИМЯ:').place(x=30, y=20)
        self.entry_first_name = tk.Entry(self, width=29)  # Поле ввода имени
        self.entry_first_name.place(x=150, y=20)

        tk.Label(self, text='ФАМИЛИЯ:').place(x=30, y=50)
        self.entry_last_name = tk.Entry(self, width=29)  # Поле ввода фамилии
        self.entry_last_name.place(x=150, y=50)

        # 3 кнопки для выбора даты рождения
        tk.Label(self, text='ДАТА РОЖДЕНИЯ:').place(x=30, y=80)
        self.combobox_days = ttk.Combobox(self, values=DAYS, width=2, state='readonly')
        self.combobox_days.current(0)
        self.combobox_days.place(x=150, y=80)

        self.combobox_month = ttk.Combobox(self, values=MONTH, width=10, state='readonly')
        self.combobox_month.current(0)
        self.combobox_month.place(x=188, y=80)

        self.combobox_year = ttk.Combobox(self, values=YEARS, width=5, state='readonly')
        self.combobox_year.current(30)
        self.combobox_year.place(x=275, y=80)

        # Кнопка 'Добавить'
        self.button_add = tk.Button(self, image=self.main_app.add_img, bd=0, command=lambda: self.on_click())
        self.button_add.place(x=20, y=120)

        # Кнопка 'Отмена'
        tk.Button(self, image=self.main_app.cancel_img, bd=0, command=lambda: self.destroy()).place(x=185, y=120)
        # ==============================================================================================================
        #
        # ==============================================================================================================

    # Обработка нажатия на кнопку 'Добавить'
    def on_click(self):
        user_first_name = self.entry_first_name.get().strip()
        user_last_name = self.entry_last_name.get().strip()

        # Если в оба поля ввели буквы
        if user_first_name.isalpha() and user_last_name.isalpha():
            birthday = self.combobox_days.get() + '/' + \
                       self.combobox_month.get() + '/' + \
                       self.combobox_year.get()
            # Создаём объект User и заносим его в базу данных
            user = User(user_last_name, user_first_name, birthday)
            self.main_app.db.record_user(user)
            # Перерисовываем таблицу пользователей, обновляем данные ИТОГО
            self.main_app.display_all_users_table()
            self.main_app.update_label_total_user_info()
            self.main_app.update_label_total_goods_per_month()
            self.destroy()
