import tkinter as tk
from tkinter import ttk

    # from Main import app
from src.TableItems import Goods


class EditGoods(tk.Toplevel):
    def __init__(self, my_root, main_window_current_state):
        super().__init__(my_root)
        # self.view = app
        self.current_month = self.entry_text = self.entry_goods = self.combobox_month = None

        self.init_ui()
        self.grab_set()

    def init_ui(self):
        self.title('Редактировать...')
        self.geometry('360x180+400+400')
        self.resizable(False, False)

        # **************************************** row 1 ********************************************
        label_client = tk.Label(self, text='КЛИЕНТ:')
        label_client.place(x=30, y=20)

        label_client_info = tk.Label(self, text=self.view.current_selected_user_name,
                                     font=('Adobe Clean Light', 11, 'italic'), fg='gray')
        label_client_info.place(x=115, y=20)

        # **************************************** row 2 ********************************************
        label_month = tk.Label(self, text='МЕСЯЦ:')
        label_month.place(x=30, y=55)

        self.combobox_month = ttk.Combobox(self, values=self.view.MONTH, width=10)
        if self.view.current_selected_month is not None:
            self.combobox_month.current(self.view.MONTH.index(self.view.current_selected_month))
        else:
            self.combobox_month.current(0)
        self.combobox_month.bind("<<ComboboxSelected>>", self.on_click_month_box)
        self.combobox_month.place(x=115, y=55)

        # **************************************** row 3 ********************************************
        label_goods = tk.Label(self, text='ТОВАР:')
        label_goods.place(x=30, y=90)

        self.entry_text = tk.StringVar()
        self.entry_goods = tk.Entry(self, textvariable=self.entry_text, width=7)

        if self.view.table_goods.selection() != ():
            month = ''
            for record in self.view.table_goods.selection():
                month = self.view.table_goods.item(record)['values'][2]
            for item in self.view.db.session.query(Goods).filter(Goods.user_id == self.view.current_selected_user_id,
                                                                 Goods.month == month).all():
                self.entry_text.set(item.goods)
        else:
            for item in self.view.db.session.query(Goods).filter(Goods.user_id == self.view.current_selected_user_id,
                                                                 Goods.month == 'Январь').all():
                self.entry_text.set(item.goods)
        self.entry_goods.place(x=115, y=90)

        # **************************************** row 4 ********************************************
        button_edit = tk.Button(self, text='Редактировать', padx=5, pady=5, width=15, bg='light gray',
                                command=lambda: self.edit_goods(self.view.current_selected_user_id,
                                                                self.combobox_month,
                                                                self.entry_goods))
        button_edit.place(x=40, y=130)

        button_cancel = tk.Button(self, text='Отмена', padx=5, pady=5, width=15, bg='light gray',
                                  command=lambda: self.cancel())
        button_cancel.place(x=200, y=130)

    def on_click_month_box(self, event):
        current_month = self.combobox_month.get()
        for item in self.view.db.session.query(Goods).filter(Goods.user_id == self.view.current_selected_user_id,
                                                             Goods.month == current_month).all():
            self.entry_text.set(item.goods)

    def edit_goods(self, user_id, combobox_month, entry_goods):

        def is_int(s):
            if s != '':
                if s[0] in ('-', '+'):
                    return s[1:].isdigit()
                return s.isdigit()

        if is_int(entry_goods.get()):
            self.view.db.update_goods(user_id, combobox_month.get(), entry_goods.get())
            self.view.show_table_user_goods(user_id)
            self.view.update_total_goods_per_month(self.view.combobox_month.get())
            self.destroy()

    def cancel(self):
        self.destroy()