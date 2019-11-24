import tkinter as tk
from tkinter import ttk


class AddUser(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.init_ui()
        # self.grab_set()

    def init_ui(self):
        self.title('Добавить клиента')
        self.geometry('360x170+700+400')
        self.resizable(False, False)

        # **************************************** row 1 ********************************************
        label_first_name = tk.Label(self, text='ИМЯ:')
        label_first_name.place(x=30, y=20)

        entry_first_name = tk.Entry(self, width=29)
        entry_first_name.place(x=150, y=20)

        # **************************************** row 2 ********************************************
        label_last_name = tk.Label(self, text='ФАМИЛИЯ:')
        label_last_name.place(x=30, y=50)

        entry_last_name = tk.Entry(self, width=29)
        entry_last_name.place(x=150, y=50)

        # **************************************** row 3 ********************************************
        label_birthday = tk.Label(self, text='ДАТА РОЖДЕНИЯ:')
        label_birthday.place(x=30, y=80)

        combobox_days = ttk.Combobox(self, values=[x for x in range(1, 32)], width=2)
        combobox_days.current(0)
        combobox_days.place(x=150, y=80)

        month = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
                 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
        combobox_month = ttk.Combobox(self, values=month, width=10)
        combobox_month.current(0)
        combobox_month.place(x=188, y=80)

        combobox_year = ttk.Combobox(self, values=[x for x in range(1950, 2010)], width=5)
        combobox_year.current(30)
        combobox_year.place(x=275, y=80)

        # **************************************** row 4 ********************************************
        button_edit = tk.Button(self, text='Добавить', padx=5, pady=5, width=15, bg='light gray')
        button_edit.place(x=40, y=120)

        button_cancel = tk.Button(self, text='Отмена', padx=5, pady=5, width=15, bg='light gray',
                                  command=lambda: self.cancel())
        button_cancel.place(x=200, y=120)

    def cancel(self):
        self.destroy()

