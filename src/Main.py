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
MONTH_TWO_LETTER = ['Ян', 'Фе', 'Мр', 'Ап', 'Мй', 'Ин', 'Ил', 'Ав', 'Се', 'Ок', 'Но', 'Де']
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
            self.menu_bar = \
            self.search_entry = None

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
        self.display_all_users_table()

    def init_main(self):
        # ==============================================================================================================
        #                                                МЕТКИ
        # ==============================================================================================================
        # Статические метки
        tk.Label(text='Список клиентов', font=('Adobe Clean Light', 18, 'bold')).place(x=140, y=20)
        tk.Label(text='Куплено товара', font=('Adobe Clean Light', 18, 'bold')).place(x=710, y=20)
        tk.Label(text='Всего клиентов:', font=('Adobe Clean Light', 16, 'bold')).place(x=20, y=500)
        tk.Label(text='Куплено за месяц ', font=('Adobe Clean Light', 16, 'bold')).place(x=20, y=550)

        # Метка для имени пользователя, чья таблица товаров в данный момент на экране
        self.label_current_displayed_user = tk.Label(font=('Adobe Clean Light', 14, 'italic'), fg='green')
        self.label_current_displayed_user.place(x=650, y=60)

        # ==============================================================================================================
        #                                           ПОИСК ПО ИМЕНИ
        # ==============================================================================================================
        tk.Label(text='Поиск:', font=('Adobe Clean Light', 14, 'italic')).place(x=25, y=60)
        # Поле ввода
        self.search_entry = tk.Entry()
        self.search_entry.place(x=85, y=67)
        # Кнопки
        tk.Button(text='Поиск', width=10, command=lambda: self.search_users()).place(x=220, y=64)
        tk.Button(text='Очистить', width=10, command=lambda: self.clear_search()).place(x=310, y=64)

        # ==============================================================================================================
        #                                    ОТОБРАЖЕНИЕ ДАННЫХ 'ИТОГО'
        # ==============================================================================================================
        # Метки данных итого
        self.label_total_user_info = tk.Label(font=('Adobe Clean Light', 17, 'italic'), fg='dark blue')
        self.label_total_user_info.place(x=200, y=500)
        self.label_total_goods_per_month = tk.Label(font=('Adobe Clean Light', 17, 'italic'), fg='dark blue')
        self.label_total_goods_per_month.place(x=310, y=550)

        # Выпадающий спиок месяцев
        self.combobox_month = ttk.Combobox(values=MONTH, width=10, state='readonly')
        self.combobox_month.bind("<<ComboboxSelected>>", lambda event: self.update_label_total_goods_per_month())
        self.combobox_month.current(0)
        self.combobox_month.place(x=215, y=557)

        # ==============================================================================================================
        #                                        ТАБЛИЦА ПОЛЬЗОВАТЕЛЕЙ (СЛЕВА)
        # ==============================================================================================================
        frame_users = tk.Frame()
        frame_users.place(x=20, y=95)

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
        # Добавить
        self.add_img = tk.PhotoImage(file='image/add.png')  # Allowed PPM, PNG, JPEG, GIF, TIFF and BMP.
        tk.Button(image=self.add_img, command=lambda: app_manager.display_add_user_window(), bd=0).place(x=15, y=430)

        # Редактировать
        self.edit_img = tk.PhotoImage(file='image/edit.png')
        tk.Button(image=self.edit_img, command=lambda: app_manager.display_edit_user_window(), bd=0).place(x=172, y=430)

        # Удалить
        self.delete_img = tk.PhotoImage(file='image/delete.png')
        tk.Button(image=self.delete_img, command=lambda: app_manager.delete_user_from_db(), bd=0).place(x=330, y=430)

        # Иконка кнопки 'Отмена'
        self.cancel_img = tk.PhotoImage(file='image/cancel.png')

        # ==============================================================================================================
        #                                        ТАБЛИЦА ТОВАРОВ (СПРАВА)
        # ==============================================================================================================
        frame_goods = tk.Frame()
        frame_goods.place(x=650, y=95)

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
        # Добавить
        btn_add_goods = tk.Button(image=self.add_img, command=lambda: app_manager.display_add_goods_window(), bd=0)
        btn_add_goods.place(x=652, y=370)

        # Редактировать
        btn_edit_goods = tk.Button(image=self.edit_img, command=lambda: app_manager.display_edit_goods_window(), bd=0)
        btn_edit_goods.place(x=810, y=370)

        # ==============================================================================================================
        #                                          КНОПКИ МЕЖДУ ТАБЛИЦАМИ
        # ==============================================================================================================
        # Arrow
        self.arrow_image = tk.PhotoImage(file='image/arrow.png')
        tk.Button(image=self.arrow_image, bd=0, command=lambda: app_manager.on_click_arrow_button()).place(x=525, y=110)

        # Graphic
        self.graphic_image = tk.PhotoImage(file='image/graphic.png')
        tk.Button(image=self.graphic_image, bd=0, command=lambda: app_manager.display_graphic()).place(x=530, y=200)

        # Diagram
        self.diagram_image = tk.PhotoImage(file='image/diagram.png')
        tk.Button(image=self.diagram_image, bd=0, command=lambda: app_manager.display_diagram()).place(x=530, y=310)

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
        edit_menu.add_command(label='Добавить клиента', command=lambda: app_manager.display_add_user_window())
        edit_menu.add_command(label='Добавить товар', command=lambda: app_manager.display_add_goods_window())

        # Конструируем подменю меню 'Редактировать'
        edit_choice = tk.Menu(edit_menu, tearoff=0)
        edit_choice.add_command(label='Данные клиента', command=lambda: app_manager.display_edit_user_window())
        edit_choice.add_command(label='Количество товара', command=lambda: app_manager.display_edit_goods_window())
        edit_menu.add_cascade(label='Редактировать', menu=edit_choice)
        self.menu_bar.add_cascade(label='Редактировать', menu=edit_menu)

        # 'График'
        graphic_menu = tk.Menu(self.menu_bar, tearoff=0)
        graphic_menu.add_command(label='График товаров', command=lambda: app_manager.display_graphic())
        graphic_menu.add_command(label='Диаграмма товаров', command=lambda: app_manager.display_diagram())
        self.menu_bar.add_cascade(label='График', menu=graphic_menu)

        # 'Справка'
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label='О программе')
        self.menu_bar.add_cascade(label='Справка', menu=help_menu)

    # ==================================================================================================================
    #                                              ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ
    # ==================================================================================================================
    # Сеттер для переменной состояния главного окна
    def set_main_window_state(self, user_id=None, user_name=None, is_display=None):
        if user_id is not None:
            self.main_window_state['user_id'] = user_id
        if user_name is not None:
            self.main_window_state['user_name'] = user_name
        if is_display is not None:
            self.main_window_state['goods_visible'] = is_display

    def reset_main_window_state(self):
        self.main_window_state['user_id'] = ''
        self.main_window_state['user_name'] = []
        self.main_window_state['goods_visible'] = False

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

    # Используем функцию при вызове окна 'Редактировать количество товара', получаем значение для вставки в поле ввода
    def get_goods_amount(self, user_id, month):
        return self.db.get_goods_amount(user_id, month)

    # Получаем лист значений кол-ва товара по месяцам для пользователя user_id, для отрисовки графика
    def get_goods_values_of_user(self, user_id) -> list:
        result = []
        for index in range(12):
            result.append(int(self.get_goods_amount(user_id, MONTH[index])))
        return result

    # Поиск по имени и отображение таблицы с найденными именами
    def search_users(self):
        search_string = self.search_entry.get()
        search_string = search_string.lower()
        founded_users = []  # Список найденных пользователей
        if search_string.isalpha():
            for user in self.db.session.query(User).filter().all():
                if search_string in user.first_name.lower() or search_string in user.last_name.lower():
                    founded_users.append(user)
        if len(founded_users) != 0:
            self.display_founded_users_table(founded_users)

    # Очистка поля ввода в поиске и возврат к исходному состоянию таблицы = отображение всех клиентов из базы
    def clear_search(self):
        self.search_entry.delete(0, 'end')
        self.display_all_users_table()

    # ==================================================================================================================
    #                                          ФУНКЦИИ ОБНОВЛЕНИЯ ДАННЫХ 'ИТОГО'
    # ==================================================================================================================
    # Метод для обновления текста метки с информацией о кол-ве клиентов
    def update_label_total_user_info(self):
        self.label_total_user_info.config(text=len(self.db.session.query(User).filter().all()))

    # Метод для обновления текста метки с информацией о кол-ве товара, купленого ВСЕМИ клиентами в выбранный месяц
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
    def display_all_users_table(self):
        [self.table_users.delete(i) for i in self.table_users.get_children()]
        [self.table_users.insert('', 'end', values=(user.id, user.last_name, user.first_name, user.birthday))
         for user in self.db.session.query(User).filter().all()]

    def display_user_goods_table(self, user_id: str):
        [self.table_goods.delete(i) for i in self.table_goods.get_children()]
        [self.table_goods.insert('', 'end', values=(goods.id, goods.user_id, goods.month, goods.goods))
         for goods in self.db.session.query(Goods).filter(Goods.user_id == user_id).all()]

    def display_founded_users_table(self, users: list):
        [self.table_users.delete(i) for i in self.table_users.get_children()]
        [self.table_users.insert('', 'end', values=(user.id, user.last_name, user.first_name, user.birthday))
         for user in users]


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
