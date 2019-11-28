import tkinter as tk
from tkinter import ttk

# import Main

from src.TableItems import User


class AddUser(tk.Toplevel):
    def __init__(self, my_root, main_window_current_state):
        super().__init__(my_root)
        self.birthday = None
        self.current_state = main_window_current_state
        self.init_window()
        self.grab_set()

    def init_window(self):
        import Main

        self.title('Добавить клиента...')
        self.geometry('360x170+400+400')
        self.resizable(False, False)

        # **************************************** row 1 ********************************************
        label_first_name = tk.Label(self, text='ИМЯ:')
        label_first_name.place(x=30, y=20)

        self.entry_first_name = tk.Entry(self, width=29)
        self.entry_first_name.place(x=150, y=20)

        # **************************************** row 2 ********************************************
        label_last_name = tk.Label(self, text='ФАМИЛИЯ:')
        label_last_name.place(x=30, y=50)

        self.entry_last_name = tk.Entry(self, width=29)
        self.entry_last_name.place(x=150, y=50)

        # **************************************** row 3 ********************************************
        label_birthday = tk.Label(self, text='ДАТА РОЖДЕНИЯ:')
        label_birthday.place(x=30, y=80)

        self.combobox_days = ttk.Combobox(self, values=[x for x in range(1, 32)], width=2)
        self.combobox_days.current(0)
        self.combobox_days.place(x=150, y=80)

        self.combobox_month = ttk.Combobox(self, values=Main.MONTH, width=10)
        self.combobox_month.current(0)
        self.combobox_month.place(x=188, y=80)

        self.combobox_year = ttk.Combobox(self, values=[x for x in range(1950, 2010)], width=5)
        self.combobox_year.current(30)
        self.combobox_year.place(x=275, y=80)

        # **************************************** row 4 ********************************************
        self.user_birthday = [self.combobox_days.get(), self.combobox_month.get(), self.combobox_year.get()]

        button_add = tk.Button(self, text='Добавить', padx=5, pady=5, width=15, bg='light gray',
                               command=lambda: self.add_user_to_db(self.entry_first_name.get(),
                                                                   self.entry_last_name.get(),
                                                                   self.user_birthday))
        button_add.place(x=40, y=120)

        button_cancel = tk.Button(self, text='Отмена', padx=5, pady=5, width=15, bg='light gray',
                                  command=lambda: self.destroy())
        button_cancel.place(x=200, y=120)

    def add_user_to_db(self, user_first_name: str, user_last_name: str, user_birthday_date: list):
        import Main
        if user_first_name.isalpha() and user_last_name.isalpha():
            birthday = user_birthday_date[0] + '/' + user_birthday_date[1] + '/' + user_birthday_date[2]
            user = User(user_last_name, user_first_name, birthday)
            Main.db.record_user(user)
            self.destroy()
        # Перерисовывам таблицу пользователей и обновляем данные ИТОГО
        Main.app.show_table_users()
        Main.update_label_total_user_info()
        Main.view.update_total_goods_per_month()
