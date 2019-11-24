import tkinter as tk
from tkinter import ttk


class AddGoods(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.label_client_info = None
        self.combobox_month = None
        self.init_ui()

    def init_ui(self):
        self.title('Добавить товар')
        self.geometry('360x180+700+400')
        self.resizable(False, False)

        # **************************************** row 1 ********************************************
        label_client = tk.Label(self, text='КЛИЕНТ:')
        label_client.place(x=30, y=20)

        self.label_client_info = tk.Label(self, text='OK')
        self.label_client_info.place(x=115, y=20)

        # **************************************** row 2 ********************************************
        label_goods = tk.Label(self, text='МЕСЯЦ:')
        label_goods.place(x=30, y=55)

        month = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
                 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
        self.combobox_month = ttk.Combobox(self, values=month, width=10)
        self.combobox_month.current(0)
        self.combobox_month.place(x=115, y=55)

        # **************************************** row 3 ********************************************
        label_month = tk.Label(self, text='ТОВАР (+/-):')
        label_month.place(x=30, y=90)

        entry_goods = tk.Entry(self, width=13)
        entry_goods.place(x=115, y=90)

        # **************************************** row 4 ********************************************
        button_edit = tk.Button(self, text='Добавить', padx=5, pady=5, width=15, bg='light gray')
        button_edit.place(x=40, y=130)

        button_cancel = tk.Button(self, text='Отмена', padx=5, pady=5, width=15, bg='light gray',
                                  command=lambda: self.cancel())
        button_cancel.place(x=200, y=130)

    def cancel(self):
        self.destroy()
