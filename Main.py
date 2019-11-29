"""
реализовать GUI программу:
a)таблица с 4мя колонками- имя, фамилия, год рождения, I'd
b)таблица с 4мя колонками- I'd, I'd пользователя из прошлой таблицы, месяц, количество купленного товара
c) добавить интерфейс создания, обновления, удаления записей в эти таблицы
d)интерфейс,который выводит записи из таблицы на экран(примерно, как было в последнем задании только теперь две таблицы)
e)вывести на экран характеристики - всего пользователей, всего куплено товара в этом месяце
f)реализовать поиск по имени/месяцу - вводим имя или месяца, а на экране отображаются результаты фильтрации
g) С помощью библиотеки matplotlib(на их сайте есть примеры, как интегрировать в tkinter) сделать вывод графиков.
Для отрисовки графиков мы выбираем пользователей и в окне появляются графики, сколько товаров они купили по месяцам.
oX- дата, oY- кол-во товара.
Дополнительно:
a) реализовать график для товара - выбираем месяца, а в окне появляются столбчатые диаграммы с суммарным количеством
товара в этом месяце
b)динамически обновлять графики - если изменилась таблица, меняем содержимое графика в реальном времени
c) менять диапазон времени для графиков -  меню, где можно задать oX min и oX max
"""
import tkinter as tk
from tkinter import ttk
from src.DatabaseEngine import DatabaseEngine
from src.TableItems import User, Goods

DAYS = [x for x in range(1, 32)]
MONTH = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
         'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
YEARS = [x for x in range(1950, 2010)]


class Main(tk.Frame):
    def __init__(self, my_root):
        super().__init__(my_root)
        self.root = my_root
        self.db = db
        self.table_users = \
            self.table_goods = \
            self.combobox_month = \
            self.label_total_user_info = \
            self.label_total_goods_per_month = \
            self.arrow_image = \
            self.graphic_image = \
            self.diagram_image = None
        self.main_window_current_state = {'user_id': 'None',          # user_id
                                          'user_name': [],        # [first_name, last_name]
                                          'birthday': [],         # [day: str, month: str, year: str]
                                          'selected_month': '',   # selected month in table 'Goods'
                                          'goods_amount': 0}      # goods amount in selected month

        self.init_main()
        self.display_table_users()

    def init_main(self):
        # ==============================================================================================================
        #                                            МЕТКИ ГЛАВНОГО ОКНА
        # ==============================================================================================================

        label_table_name_users = tk.Label(text='Список клиентов', font=('Adobe Clean Light', 18, 'bold'))
        label_table_name_users.place(x=160, y=20)

        label_table_name_goods = tk.Label(text='Куплено товара', font=('Adobe Clean Light', 18, 'bold'))
        label_table_name_goods.place(x=730, y=20)

        label_total_user = tk.Label(text='Всего клиентов:', font=('Adobe Clean Light', 16, 'bold'))
        label_total_user.place(x=20, y=500)

        label_total_goods = tk.Label(text='Куплено за месяц ', font=('Adobe Clean Light', 16, 'bold'))
        label_total_goods.place(x=20, y=550)

        self.label_total_user_info = tk.Label(font=('Adobe Clean Light', 14, 'italic'), fg='dark blue')
        self.label_total_user_info.place(x=200, y=502)

        self.label_total_goods_per_month = tk.Label(font=('Adobe Clean Light', 14, 'italic'), fg='dark blue')
        self.label_total_goods_per_month.place(x=310, y=553)

        # ==============================================================================================================
        #                                        ТАБЛИЦА ПОЛЬЗОВАТЕЛЕЙ (СЛЕВА)
        # ==============================================================================================================

        frame_users = tk.Frame()
        frame_users.place(x=20, y=80)

        self.table_users = ttk.Treeview(frame_users, columns=('ID', 'last_name', 'first_name', 'birthday'),
                                        height=15, show='headings', selectmode='browse')
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

        button_add_user = tk.Button(text='Добавить клиента', command=lambda: self.display_add_user_window())
        button_add_user.place(x=20, y=420)

        button_edit_user = tk.Button(text='Редактировать', command=lambda: self.display_edit_user_window())
        button_edit_user.place(x=150, y=420)

        button_delete_user = tk.Button(text='Удалить запись', command=lambda: self.delete_user_from_db())
        button_delete_user.place(x=300, y=420)

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

        button_add_goods = tk.Button(text='Добавить товар', command=lambda: self.display_add_goods_window())
        button_add_goods.place(x=650, y=360)

        button_edit_goods = tk.Button(text='Редактировать', command=lambda: self.create_edit_goods_window())
        button_edit_goods.place(x=750, y=360)

        button_delete_goods = tk.Button(text='Обнулить  запись', command=self.reset_goods)
        button_delete_goods.place(x=844, y=360)

        # ==============================================================================================================
        #                                          КНОПКИ МЕЖДУ ТАБЛИЦАМИ
        # ==============================================================================================================

        self.arrow_image = tk.PhotoImage(file='image/arrow.png')  # Allowed PPM, PNG, JPEG, GIF, TIFF, and BMP.
        button_show = tk.Button(command=lambda: self.on_click_arrow_button(), image=self.arrow_image, bd=0)
        button_show.place(x=525, y=110)

        self.graphic_image = tk.PhotoImage(file='image/graphic.png')
        button_show = tk.Button(image=self.graphic_image, bd=0)
        button_show.place(x=530, y=200)

        self.diagram_image = tk.PhotoImage(file='image/diagram.png')
        button_show = tk.Button(image=self.diagram_image, bd=0)
        button_show.place(x=530, y=310)

        # ==============================================================================================================
        #                                    КНОПКА ДЛЯ ОТОБРАЖЕНИЯ ДАННЫХ 'ИТОГО'
        # ==============================================================================================================

        self.combobox_month = ttk.Combobox(values=MONTH, width=10)
        self.combobox_month.bind("<<ComboboxSelected>>", lambda event: self.callback(event))
        self.combobox_month.current(0)
        self.combobox_month.place(x=210, y=557)

        # ==============================================================================================================
        #                                            КОНСТРУИРУЕМ 'МЕНЮ'
        # ==============================================================================================================

        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # 'Файл'
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Открыть...")
        file_menu.add_command(label="Сохранить...")
        file_menu.add_command(label="Выход", command=self.quit)
        self.menu_bar.add_cascade(label='Файл', menu=file_menu)

        # 'Редактировать'
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label='Добавить клиента', command=lambda: self.display_add_user_window())
        edit_menu.add_command(label='Добавить товар')

        # Конструируем подменю меню 'Редактировать'
        edit_choice = tk.Menu(edit_menu, tearoff=0)
        edit_choice.add_command(label='Данные клиента', command=lambda: self.display_edit_user_window())
        edit_choice.add_command(label='Товар клиента')
        edit_menu.add_cascade(label='Редактировать', menu=edit_choice)
        self.menu_bar.add_cascade(label='Редактировать', menu=edit_menu)

        # 'График'
        graphic_menu = tk.Menu(self.menu_bar, tearoff=0)
        graphic_menu.add_command(label='График товаров')
        graphic_menu.add_command(label='Диаграмма товаров')
        self.menu_bar.add_cascade(label='График', menu=graphic_menu)

        # 'Справка'
        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label='О программе')
        self.menu_bar.add_cascade(label='Справка', menu=help_menu)

        # ***************************** ВЫВОДИМ ИНФОРМАЦИЮ 'ИТОГО' *****************************************************

        self.update_label_total_user_info()
        self.update_label_total_goods_per_month()

    # ********************************* ФУНКЦИИ ОБНОВЛЕНИЯ ДАННЫХ 'ИТОГО' **********************************************

    def callback(self, event):
        self.update_label_total_goods_per_month()

    def update_label_total_user_info(self):
        self.label_total_user_info.config(text=len(self.db.session.query(User).filter().all()))

    def update_label_total_goods_per_month(self):
        if self.label_total_user_info['text'] != '0':
            res = 0
            month = self.combobox_month.get()
            for item in self.db.session.query(Goods).filter(Goods.month == month).all():
                res += int(item.goods)
            self.label_total_goods_per_month.config(text=res)
        else:
            self.label_total_goods_per_month.config(text='0')

    # ************************************* ВСПОМОГАТЕЛЬНЫЕ ФУНКЦИИ **************************************
    def on_click_arrow_button(self):
        if self.table_users.selection() != ():
            user_id = first_name = last_name = birthday = ''
            name = []
            for item in self.table_users.selection():
                self.main_window_current_state['user_id'] = self.table_users.item(item)['values'][0]

                name.append(self.table_users.item(item)['values'][2])
                name.append(self.table_users.item(item)['values'][1])
                self.main_window_current_state['user_name'] = name
                birthday = self.table_users.item(item)['values'][3]
                self.main_window_current_state['birthday'] = birthday.split('/')
        self.display_table_user_goods(self.main_window_current_state['user_id'])

        print(self.main_window_current_state)

    def update_current_state_from_users_selection(self):
        if self.table_users.selection() != ():
            name = []
            for item in self.table_users.selection():
                self.main_window_current_state['user_id'] = self.table_users.item(item)['values'][0]
                name.append(self.table_users.item(item)['values'][2])
                name.append(self.table_users.item(item)['values'][1])
                self.main_window_current_state['user_name'] = name
                birthday = self.table_users.item(item)['values'][3]
                self.main_window_current_state['birthday'] = birthday.split('/')

    """def set_main_window_current_state(self, user_id: str = None,
                                      user_name: list = None,
                                      birthday: list = None,
                                      selected_month: str = None,
                                      goods_amount: int = None):
        self.main_window_current_state['user_id'] = user_id
        self.main_window_current_state['user_name'] = user_name
        self.main_window_current_state['birthday'] = birthday
        self.main_window_current_state['selected_month'] = selected_month
        self.main_window_current_state['goods_amount'] = goods_amount"""


    # ************************************* ФУНКЦИИ ДЛЯ ОТОБРАЖЕНИЯ ТАБЛИЦ **************************************

    def display_table_users(self):
        [self.table_users.delete(i) for i in self.table_users.get_children()]
        [self.table_users.insert('', 'end', values=(user.id, user.last_name, user.first_name, user.birthday))
         for user in self.db.session.query(User).filter().all()]

    def display_table_user_goods(self, user_id: str):
        [self.table_goods.delete(i) for i in self.table_goods.get_children()]
        [self.table_goods.insert('', 'end', values=(goods.id, goods.user_id, goods.month, goods.goods))
         for goods in self.db.session.query(Goods).filter(Goods.user_id == user_id).all()]

        # Изменяем состояние главного окна
        self.main_window_current_state['user_id'] = user_id
        for user in self.db.session.query(User).filter(User.id == user_id).all():
            self.main_window_current_state['user_name'] = [user.last_name, user.first_name]

    # ********************* ОБРАБОТКА НАЖАТИЯ КНОПОК В ГЛАВНОМ ОКНЕ = ОТОБРАЖЕНИЕ НОВЫХ ОКОН ***********************

    def display_add_user_window(self):
        AddUser(self.root)

    def display_edit_user_window(self):
        # Подготавливаем данные для передачи в класс EditUser
        if self.table_users.selection() != ():
            user_id = first_name = last_name = birthday = ''
            name = []
            for item in self.table_users.selection():
                self.main_window_current_state['user_id'] = self.table_users.item(item)['values'][0]

                name.append(self.table_users.item(item)['values'][2])
                name.append(self.table_users.item(item)['values'][1])
                self.main_window_current_state['user_name'] = name
                birthday = self.table_users.item(item)['values'][3]
                self.main_window_current_state['birthday'] = birthday.split('/')

            print(self.main_window_current_state)
            EditUser(self.root, self.main_window_current_state)

    def display_add_goods_window(self):
        if self.main_window_current_state['user_id'] != '':
            if self.table_goods.selection() == ():
                AddGoods(self.root, current_user_info=None)
            else:
                for item in self.table_goods.selection():
                    self.main_window_current_state['selected_month'] = self.table_goods.item(item)['values'][2]
                    self.main_window_current_state['goods_amount'] = int(self.table_goods.item(item)['values'][3])
                AddGoods(self.root, self.main_window_current_state)

    """ def display_edit_goods_window(self, dict_state: dict):
        if dict_state['user_id'] != '':
            if self.table_goods.selection() != ():
                # Нужно эти переменные передать в EditGoods в кач-ве переменных(возможно, они могут быть локальными)
                for item in self.table_goods.selection():
                    dict_state['month'] = self.table_goods.item(item)['values'][2]
                    dict_state['goods'] = self.table_goods.item(item)['values'][3]
            EditGoods(self.root, dict_state)"""

    # Сбрасываем текущее состояние главного окна
    def reset_main_window_state(self):
        self.main_window_current_state['user_id'] = ''
        self.main_window_current_state['user_name'] = []
        self.main_window_current_state['birthday'] = []
        self.main_window_current_state['selected_month'] = ''
        self.main_window_current_state['goods_amount'] = 0

    # **************************** ОБРАБОТКА НАЖАТИЯ КНОПОК В ДОЧЕРНИХ ОКНАХ = ************************************
    # ********************** = РАБОТА С БАЗОЙ ДАННЫХ + ОБНОВЛЕНИЕ ДАННЫХ ИТОГО И СОСТОЯНИЯ ГЛАВНОГО ОКНА ************

    def add_user_to_db(self, user_first_name: str, user_last_name: str, birthday: str):

        user = User(user_last_name.strip(), user_first_name.strip(), birthday)
        self.db.record_user(user)

        # Перерисовываем таблицу пользователей обновляем данные ИТОГО
        self.display_table_users()
        self.update_label_total_user_info()
        self.update_label_total_goods_per_month()

    def delete_user_from_db(self):
        if self.table_users.selection() != ():
            # Получаем ID выделенного пользователя и удаляем записи в базах по этому ID
            for item in self.table_users.selection():
                user_id = self.table_users.item(item)['values'][0]
                self.db.delete_user(user_id)
                self.db.delete_goods(user_id)

                # Если отображалась таблица его товаров - удаляем её и обнуляем текущее состоянее главного окна
                if self.main_window_current_state['user_id'] == user_id:
                    [self.table_goods.delete(i) for i in self.table_goods.get_children()]
                    self.reset_main_window_state()

            # Пересчитываем параметры ИТОГО и выводим обновлённую таблицу пользователей
            self.update_label_total_user_info()
            self.update_label_total_goods_per_month()
            self.display_table_users()

    def edit_user_in_db(self, user_id, first_name, last_name, birthday):
        self.db.update_user(user_id, first_name, last_name, birthday)
        self.display_table_users()

    def add_goods_to_db(self):
        pass

    def edit_goods_in_db(self):
        pass

    def reset_goods(self):
        for goods in self.table_goods.selection():
            goods_id = self.table_goods.item(goods)['values'][0]
            user_id = self.table_goods.item(goods)['values'][1]
            self.db.reset_goods(goods_id)
            self.display_table_user_goods(user_id)
        self.update_label_total_goods_per_month()


class AddUser(tk.Toplevel):
    def __init__(self, my_root):
        super().__init__(my_root)
        self.birthday = None
        self.main_window = app
        self.init_window()
        self.grab_set()

    def init_window(self):
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

        self.combobox_days = ttk.Combobox(self, values=DAYS, width=2)
        self.combobox_days.current(0)
        self.combobox_days.place(x=150, y=80)

        self.combobox_month = ttk.Combobox(self, values=MONTH, width=10)
        self.combobox_month.current(0)
        self.combobox_month.place(x=188, y=80)

        self.combobox_year = ttk.Combobox(self, values=YEARS, width=5)
        self.combobox_year.current(30)
        self.combobox_year.place(x=275, y=80)

        # **************************************** row 4 ********************************************
        self.user_birthday = [self.combobox_days.get(), self.combobox_month.get(), self.combobox_year.get()]

        self.button_add = tk.Button(self, text='Добавить', padx=5, pady=5, width=15, bg='light gray',
                                    command=lambda: self.on_click())
        self.button_add.place(x=40, y=120)

        button_cancel = tk.Button(self, text='Отмена', padx=5, pady=5, width=15, bg='light gray',
                                  command=lambda: self.destroy())
        button_cancel.place(x=200, y=120)

    def on_click(self):
        user_first_name = self.entry_first_name.get().strip()
        user_last_name = self.entry_last_name.get().strip()

        if user_first_name.isalpha() and user_last_name.isalpha():
            birthday = self.combobox_days.get() + '/' + \
                       self.combobox_month.get() + '/' + \
                       self.combobox_year.get()
            self.main_window.add_user_to_db(user_first_name, user_last_name, birthday)
            self.destroy()


class EditUser(AddUser):
    def __init__(self, my_root: tk.Tk, current_user_info: dict):
        super().__init__(my_root)
        self.current_user_info = current_user_info
        self.init_ui()

    def init_ui(self):
        self.title('Редактировать...')
        # ************ ПЕРЕОПРЕДЕЛИМ СОСТОЯНИЕ ПОЛЕЙ ВВОДА, ИСПОЛЬЗУЯ ПЕРЕМЕННУЮ self.current_user_info ***********

        # Устанавливаем имя
        self.entry_first_name_text = tk.StringVar()
        self.entry_first_name.configure(textvariable=self.entry_first_name_text)
        self.entry_first_name_text.set(self.current_user_info['user_name'][0])

        # Устанавливаем фамилию
        self.entry_last_name_text = tk.StringVar()
        self.entry_last_name.configure(textvariable=self.entry_last_name_text)
        self.entry_last_name_text.set(self.current_user_info['user_name'][1])

        # Устанавливаем дату рождения
        self.combobox_days.current(DAYS.index(int(self.current_user_info['birthday'][0])))
        self.combobox_month.current(MONTH.index(self.current_user_info['birthday'][1]))
        self.combobox_year.current(YEARS.index(int(self.current_user_info['birthday'][2])))

        self.button_add.config(text = 'Редактировать', command=self.on_click)

    def on_click(self):
        # Формируем данные для передачи в главное окно
        user_id = self.current_user_info['user_id']
        first_name = self.entry_first_name.get()
        last_name = self.entry_last_name.get()
        birthday = self.combobox_days.get() + '/' + self.combobox_month.get() + '/' + self.combobox_year.get()

        if first_name + last_name != '':
            self.main_window.edit_user_in_db(user_id, first_name, last_name, birthday)
            self.main_window.display_table_users()
            self.destroy()






if __name__ == "__main__":
    root = tk.Tk()
    db = DatabaseEngine()
    app = Main(root)
    app.pack()
    root.title("Warehouse Interface")
    root.geometry("1000x650+100+50")
    root.resizable(False, False)
    root.mainloop()
