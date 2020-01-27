import tkinter as tk
from tkinter import ttk

DAYS = [x for x in range(1, 32)]
MONTH = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
         'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
YEARS = [x for x in range(1950, 2010)]


class AddGoods(tk.Toplevel):
    def __init__(self, my_root, app, data=None):
        super().__init__(my_root)
        self.entry_goods = \
            self.combobox_month = \
            self.button_edit = \
            self.button_add = None
        self.main_app = app  # Главное окно
        self.main_window_data = data

        self.init_window()
        self.grab_set()

    def init_window(self):
        self.title('Добавить товар')
        self.geometry('360x180+400+400')
        self.resizable(False, False)

        # ==============================================================================================================
        #                                              ГРАФИЧЕСКИЙ ИНТЕРФЕЙС
        # ==============================================================================================================
        # Текстовые метки
        # Клиент
        tk.Label(self, text='КЛИЕНТ:').place(x=30, y=20)
        tk.Label(self, text=self.main_app.main_window_state['user_name'][0] + ' ' +
                            self.main_app.main_window_state['user_name'][1],
                       font=('Adobe Clean Light', 13, 'bold'), fg='#227A05').place(x=115, y=15)

        # Месяц
        tk.Label(self, text='МЕСЯЦ:').place(x=30, y=55)
        self.combobox_month = ttk.Combobox(self, values=MONTH, width=10, state='readonly')
        if self.main_window_data:
            self.combobox_month.current(MONTH.index(self.main_window_data['month']))
        else:
            self.combobox_month.current(0)
        self.combobox_month.place(x=115, y=55)

        # Товар
        tk.Label(self, text='ТОВАР:').place(x=30, y=90)
        self.entry_goods = tk.Entry(self, width=13)  # Поле ввода количества товара
        self.entry_goods.place(x=115, y=90)

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
        goods_amount = self.entry_goods.get()
        if goods_amount.isdigit():
            # Если то, что ввели, является целым числом (со знаком или без), то вызываем функции из ГЛАВНОГО окна
            self.main_app.db.add_goods_for_this_month(user_id=self.main_app.main_window_state['user_id'],
                                                      month=self.combobox_month.get(),
                                                      goods=int(goods_amount))
            self.main_app.update_label_total_goods_per_month()
            self.main_app.display_table_user_goods(self.main_app.main_window_state['user_id'])
            self.destroy()
