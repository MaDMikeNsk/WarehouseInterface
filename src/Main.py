import tkinter as tk
from tkinter import ttk
from src.DatabaseEngine import DatabaseEngine
from src.TableItems import User, Goods
from tkinter import messagebox as mb
from windows.Graphic import Graphic
from windows.Diagram import Diagram
from src.AppManager import AppManager

DAYS = [x for x in range(1, 32)]
MONTH = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
         'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
MONTH_SHORT = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июнь',
               'Июль', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']
MONTH_ONE_LETTER = ['Ян', 'Фе', 'Мр', 'Ап', 'Мй', 'Ин', 'Ил', 'Ав', 'Се', 'Ок', 'Но', 'Де']
YEARS = [x for x in range(1950, 2010)]


class Main(tk.Frame):

    def __init__(self, my_root):
        super().__init__(my_root)
        self.root = my_root
        self.db = db  # База данных

        self.table_users = \
            self.table_goods = \
            self.combobox_month = \
            self.label_total_user_info = \
            self.label_total_goods_per_month = \
            self.menu_bar = None

        self.add_img = \
            self.edit_img = \
            self.delete_img = \
            self.cancel_img = \
            self.arrow_image = \
            self.graphic_image = \
            self.diagram_image = \
            self.label_current_displayed_user = None

        self.main_window_state = {'user_id': '',
                                  'user_name': [],
                                  'goods_visible': False}

        self.init_main()
        # Инициализация состояния главного окна при первом запуске
        self.update_label_total_user_info()
        self.update_label_total_goods_per_month()
        self.display_table_users()

    def init_main(self):
        # ==============================================================================================================
        #                                            МЕТКИ ГЛАВНОГО ОКНА
        # ==============================================================================================================
        tk.Label(text='Список клиентов', font=('Adobe Clean Light', 18, 'bold')).place(x=140, y=20)
        tk.Label(text='Куплено товара', font=('Adobe Clean Light', 18, 'bold')).place(x=710, y=20)
        tk.Label(text='Всего клиентов:', font=('Adobe Clean Light', 16, 'bold')).place(x=20, y=500)
        tk.Label(text='Куплено за месяц ', font=('Adobe Clean Light', 16, 'bold')).place(x=20, y=550)

        self.label_total_user_info = tk.Label(font=('Adobe Clean Light', 17, 'italic'), fg='dark blue')
        self.label_total_user_info.place(x=200, y=500)

        self.label_total_goods_per_month = tk.Label(font=('Adobe Clean Light', 17, 'italic'), fg='dark blue')
        self.label_total_goods_per_month.place(x=310, y=550)

        self.label_current_displayed_user = tk.Label(font=('Adobe Clean Light', 14, 'italic'), fg='green')
        self.label_current_displayed_user.place(x=650, y=50)

        # ==============================================================================================================
        #                                        ТАБЛИЦА ПОЛЬЗОВАТЕЛЕЙ (СЛЕВА)
        # ==============================================================================================================
        frame_users = tk.Frame()
        frame_users.place(x=20, y=80)

        self.table_users = ttk.Treeview(frame_users, columns=('ID', 'last_name', 'first_name', 'birthday'),
                                        height=15, show='headings', selectmode='extended')
        self.table_users.column("ID", width=45, anchor=tk.CENTER)
        self.table_users.column("last_name", width=150, anchor=tk.CENTER)
        self.table_users.column("first_name", width=150, anchor=tk.CENTER)
        self.table_users.column("birthday", width=110, anchor=tk.CENTER)

        self.table_users.heading("ID", text='ID')
        self.table_users.heading("last_name", text='Фамилия')
        self.table_users.heading("first_name", text='Имя')
        self.table_users.heading("birthday", text='Дата рождения')

        self.table_users.pack(side='left')

        # Scrollbar on frame_users
        vsb = ttk.Scrollbar(frame_users, orient="vertical", command=self.table_users.yview)
        vsb.pack(side='right', fill='y')
        self.table_users.configure(yscrollcommand=vsb.set)

        # ==============================================================================================================
        #                                      КНОПКИ ПОД ТАБЛИЦЕЙ ПОЛЬЗОВАТЕЛЕЙ
        # ==============================================================================================================
        self.add_img = tk.PhotoImage(file='image/add.png')
        tk.Button(image=self.add_img, command=lambda: app_manager.display_add_user_window(), bd=0).place(x=15, y=420)

        self.edit_img = tk.PhotoImage(file='image/edit.png')
        tk.Button(image=self.edit_img, command=lambda: app_manager.display_edit_user_window(), bd=0).place(x=172, y=420)

        self.delete_img = tk.PhotoImage(file='image/delete.png')
        tk.Button(image=self.delete_img, command=lambda: self.delete_user_from_db(), bd=0).place(x=330, y=420)

        self.cancel_img = tk.PhotoImage(file='image/cancel.png')

        # ==============================================================================================================
        #                                        ТАБЛИЦА ТОВАРОВ (СПРАВА)
        # ==============================================================================================================
        frame_goods = tk.Frame()
        frame_goods.place(x=650, y=80)

        self.table_goods = ttk.Treeview(frame_goods, columns=('ID', 'user_id', 'month', 'goods'),
                                        height=12, show='headings', selectmode='browse')
        self.table_goods.column("ID", width=40, anchor=tk.CENTER)
        self.table_goods.column("user_id", width=70, anchor=tk.CENTER)
        self.table_goods.column("month", width=100, anchor=tk.CENTER)
        self.table_goods.column("goods", width=100, anchor=tk.CENTER)

        self.table_goods.heading("ID", text='ID')
        self.table_goods.heading("user_id", text='ID Клиента')
        self.table_goods.heading("month", text='Месяц')
        self.table_goods.heading("goods", text='Товар')

        self.table_goods.pack(side='left')

        # ==============================================================================================================
        #                                        КНОПКИ ПОД ТАБЛИЦЕЙ ТОВАРОВ
        # ==============================================================================================================
        btn_add_goods = tk.Button(image=self.add_img, command=lambda: app_manager.display_add_goods_window(), bd=0)
        btn_add_goods.place(x=652, y=360)

        btn_edit_goods = tk.Button(image=self.edit_img, command=lambda: app_manager.display_edit_goods_window(), bd=0)
        btn_edit_goods.place(x=810, y=360)

        # ==============================================================================================================
        #                                          КНОПКИ МЕЖДУ ТАБЛИЦАМИ
        # ==============================================================================================================
        # Arrow button
        self.arrow_image = tk.PhotoImage(file='image/arrow.png')  # Allowed PPM, PNG, JPEG, GIF, TIFF and BMP.
        tk.Button(command=lambda: self.on_click_arrow_button(), image=self.arrow_image, bd=0).place(x=525, y=110)

        # Graphic button
        self.graphic_image = tk.PhotoImage(file='image/graphic.png')
        tk.Button(image=self.graphic_image, bd=0, command=lambda: self.display_graphic()).place(x=530, y=200)

        # Diagram button
        self.diagram_image = tk.PhotoImage(file='image/diagram.png')
        tk.Button(image=self.diagram_image, bd=0, command=lambda: self.display_diagram()).place(x=530, y=310)

        # ==============================================================================================================
        #                                    COMBOBOX ДЛЯ ОТОБРАЖЕНИЯ ДАННЫХ 'ИТОГО'
        # ==============================================================================================================
        self.combobox_month = ttk.Combobox(values=MONTH, width=10, state='readonly')
        self.combobox_month.bind("<<ComboboxSelected>>", lambda event: self.callback())
        self.combobox_month.current(0)
        self.combobox_month.place(x=215, y=557)

        # ==============================================================================================================
        #                                            КОНСТРУИРУЕМ 'МЕНЮ'
        # ==============================================================================================================
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # 'Файл'
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Открыть...")  # TODO открыть базу данных
        file_menu.add_command(label="Сохранить...")  # TODO сохранить базу данных
        file_menu.add_command(label="Выход", command=self.quit)
        self.menu_bar.add_cascade(label='Файл', menu=file_menu)

        # 'Редактировать'
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label='Добавить клиента', command=lambda: self.display_add_user_window())
        edit_menu.add_command(label='Добавить товар', command=lambda: self.display_add_goods_window())

        # Конструируем подменю меню 'Редактировать'
        edit_choice = tk.Menu(edit_menu, tearoff=0)
        edit_choice.add_command(label='Данные клиента', command=lambda: self.display_edit_user_window())
        edit_choice.add_command(label='Количество товара', command=lambda: self.display_edit_goods_window())
        edit_menu.add_cascade(label='Редактировать', menu=edit_choice)
        self.menu_bar.add_cascade(label='Редактировать', menu=edit_menu)

        # 'График'
        graphic_menu = tk.Menu(self.menu_bar, tearoff=0)
        graphic_menu.add_command(label='График товаров', command=lambda: self.display_graphic())
        graphic_menu.add_command(label='Диаграмма товаров', command=lambda: self.display_diagram())
        self.menu_bar.add_cascade(label='График', menu=graphic_menu)

        # 'Справка'
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label='О программе')
        self.menu_bar.add_cascade(label='Справка', menu=help_menu)

    # ==================================================================================================================
    #                                              ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
    # ==================================================================================================================
    # Метод для проверки поля ввода количества товара
    @staticmethod
    def is_int(string):
        if string != '':
            if string[0] in ('-', '+'):
                return string[1:].isdigit()
            return string.isdigit()

    # Клик на стрелку
    def on_click_arrow_button(self):
        if len(self.table_users.selection()) == 1:
            selected_user = self.get_data_from_user_selection()[0]
            self.display_table_user_goods(selected_user['user_id'])
            self.main_window_state['user_id'] = selected_user['user_id']
            self.main_window_state['user_name'] = selected_user['user_name']
            self.main_window_state['goods_visible'] = True
            self.label_current_displayed_user.\
                config(text=f"{selected_user['user_name'][0]} {selected_user['user_name'][1]}")

    def set_main_window_state(self, user_id=None, user_name=None, is_display=None):
        self.main_window_state['user_id'] = user_id
        self.main_window_state['user_name'] = user_name
        self.main_window_state['goods_visible'] = is_display

    # Получаем данные из выделенных пользователем строк в таблице User (слева)
    def get_data_from_user_selection(self) -> list:  # List of dicts
        if self.table_users.selection() != ():
            result = []
            for item in self.table_users.selection():
                user_data = dict()
                user_data['user_id'] = self.table_users.item(item)['values'][0]
                user_data['user_name'] = [self.table_users.item(item)['values'][2],
                                          self.table_users.item(item)['values'][1]]
                user_data['birthday'] = self.table_users.item(item)['values'][3].split('/')
                result.append(user_data)
            return result

    # Получаем данные из выделенной пользователем строки в таблице Goods (справа)
    def get_data_from_goods_selection(self) -> dict:
        if len(self.table_goods.selection()) == 1:
            data = {'user_id': None,
                    'user_name': self.main_window_state['user_name'],
                    'month': None,
                    'goods': None}
            for item in self.table_goods.selection():
                data['user_id'] = self.table_goods.item(item)['values'][1]
                data['month'] = self.table_goods.item(item)['values'][2]
                data['goods'] = self.table_goods.item(item)['values'][3]
            return data

    # ==================================================================================================================
    #                                          ФУНКЦИИ ОБНОВЛЕНИЯ ДАННЫХ 'ИТОГО'
    # ==================================================================================================================
    # Реакция на выбор месяца для вывода 'ИТОГО'
    def callback(self):
        self.update_label_total_goods_per_month()

    # Метод для обновления информации о кол-ве клиентов
    def update_label_total_user_info(self):
        self.label_total_user_info.config(text=len(self.db.session.query(User).filter().all()))

    # Метод для обновления информации о кол-ве товара, купленого ВСЕМИ клиентами в выбранный месяц
    def update_label_total_goods_per_month(self):
        if self.label_total_user_info['text'] != '0':
            res = 0
            month = self.combobox_month.get()
            for item in self.db.session.query(Goods).filter(Goods.month == month).all():
                res += int(item.goods)
            self.label_total_goods_per_month.config(text=res)
        else:
            self.label_total_goods_per_month.config(text='0')

    # ==================================================================================================================
    #                                             ФУНКЦИИ ДЛЯ ОТОБРАЖЕНИЯ ТАБЛИЦ
    # ==================================================================================================================
    def display_table_users(self):
        [self.table_users.delete(i) for i in self.table_users.get_children()]
        [self.table_users.insert('', 'end', values=(user.id, user.last_name, user.first_name, user.birthday))
         for user in self.db.session.query(User).filter().all()]

    def display_table_user_goods(self, user_id: str):
        [self.table_goods.delete(i) for i in self.table_goods.get_children()]
        [self.table_goods.insert('', 'end', values=(goods.id, goods.user_id, goods.month, goods.goods))
         for goods in self.db.session.query(Goods).filter(Goods.user_id == user_id).all()]

    # ==================================================================================================================
    #                                  ФУНКЦИИ ДЛЯ ОБРАБОТКИ НАЖАТИЯ КНОПОК ПОД ТАБЛИЦАМИ
    # ==================================================================================================================
    # Кнопка 'Добавить' (под левой таблицей)
    # def display_add_user_window(self):
    #   AddUser(self.root)

    # Кнопка 'Редактировать' (под левой таблицей)
    # def display_edit_user_window(self):
    #    if len(self.table_users.selection()) == 1:
    #        selected_user = self.get_data_from_user_selection()
    #        EditUser(self.root, selected_user)

    # Кнопка 'Удалить запись' (под левой таблицей)
    def delete_user_from_db(self):
        if len(self.table_users.selection()) != ():
            # Получаем ID пользователей, которых выбрали в таблице
            selected_users = self.get_data_from_user_selection()

            # Удаляем из базы пользователя и все записи из 2-й таблицы по его ID
            for user in selected_users:
                self.db.delete_user(user['user_id'])
                self.db.delete_goods(user['user_id'])

                # Если отображалась таблица его товаров - удаляем её и
                # сбрасываем параметры main_window_state, скрываем метку с именем отображаемого клиента
                if self.main_window_state['user_id'] == user['user_id']:
                    [self.table_goods.delete(i) for i in self.table_goods.get_children()]
                    self.set_main_window_state(user_id='', is_display=False)
                    self.label_current_displayed_user.config(text='')

            # Пересчитываем параметры 'ИТОГО' и выводим обновлённую таблицу пользователей
            self.update_label_total_user_info()
            self.update_label_total_goods_per_month()
            self.display_table_users()

    # Кнопка 'Добавить' (под правой таблицей)
    def display_add_goods_window(self):
        if self.main_window_state['user_id'] != '':
            if self.table_goods.selection() != ():
                data = self.get_data_from_goods_selection()
                AddGoods(self.root, data)
            else:
                AddGoods(self.root, self.main_window_state)

    # Кнопка 'Редактировать' (под правой таблицей)
    def display_edit_goods_window(self):
        if self.main_window_state['goods_visible']:
            if self.table_goods.selection() != ():
                selected_goods = self.get_data_from_goods_selection()
                EditGoods(self.root, selected_goods)
            else:
                EditGoods(self.root, self.main_window_state)

    # Кнопка "График"
    def display_graphic(self):
        if 0 < len(self.table_users.selection()) <= 4:
            users_list = self.get_data_from_user_selection()  # list of dict (selected users)
            data_to_display = []
            for user in users_list:
                data = dict()
                data['user_name'] = user['user_name'][0] + ' ' + user['user_name'][1]
                data['values'] = self.get_goods_values_of_user(user['user_id'])  # List of goods values
                data_to_display.append(data)
            Graphic(self.root, data_to_display)
        elif len(self.table_users.selection()) > 4:
            mb.showerror("Ошибка", "Выберите не более четырех клиентов")

    # Кнопка "Диаграмма"
    def display_diagram(self):
        if 0 < len(self.table_users.selection()) <= 4:
            users_list = self.get_data_from_user_selection()  # list of dict (selected users)
            data_to_display = []
            for user in users_list:
                data = dict()
                data['user_name'] = user['user_name'][0] + ' ' + user['user_name'][1]
                data['values'] = self.get_goods_values_of_user(user['user_id'])  # List of goods values
                data_to_display.append(data)
            Diagram(self.root, data_to_display)
        elif len(self.table_users.selection()) > 4:
            mb.showerror("Ошибка", "Выберите не более четырех клиентов")

    # ==================================================================================================================
    #                          ОБРАБОТКА НАЖАТИЯ КНОПОК В ДОЧЕРНИХ ОКНАХ - РАБОТА С БАЗОЙ ДАННЫХ
    # ==================================================================================================================
    # Кнопка 'Добавить' в окне AddGoods
    def update_goods_in_db(self, user_id, month, goods):
        self.db.add_goods_for_this_month(user_id, month, goods)
        self.update_label_total_goods_per_month()
        self.display_table_user_goods(user_id)

    # Кнопка 'Редактировать' в окне EditGoods
    def edit_goods_in_db(self, user_id, month, goods):
        self.db.update_goods(user_id, month, goods)
        self.update_label_total_goods_per_month()
        self.display_table_user_goods(user_id)

    # Используем функцию при вызове окна 'Редактировать количество товара', получаем значение для вставки в поле ввода
    def get_goods_amount(self, user_id, month):
        return self.db.get_goods_amount(user_id, month)

    # Получаем лист значений кол-ва товара по месяцам для пользователя user_id, для отрисовки графика
    def get_goods_values_of_user(self, user_id) -> list:
        result = []
        for index in range(12):
            result.append(int(self.get_goods_amount(user_id, MONTH[index])))
        return result


if __name__ == "__main__":
    root = tk.Tk()
    db = DatabaseEngine()
    app = Main(root)
    app_manager = AppManager(app, root)
    app.pack()
    root.title("Warehouse Interface")
    root.geometry("1000x650+300+100")
    root.resizable(False, False)
    root.mainloop()
