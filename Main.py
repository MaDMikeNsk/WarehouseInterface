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
        self.main_window_current_state = {'user_id': '', 'user_name': ['', ''], 'month': '', 'goods': 0}

        self.init_main()
        self.show_table_users()

    def init_main(self):
        #  ************************************** Главное окно ******************************************************
        # Labels
        label_table_name_users = tk.Label(text='Список клиентов', font=('Adobe Clean Light', 18, 'bold'))
        label_table_name_users.place(x=160, y=20)

        label_table_name_goods = tk.Label(text='Куплено товара', font=('Adobe Clean Light', 18, 'bold'))
        label_table_name_goods.place(x=730, y=20)

        label_total_user = tk.Label(text='Всего клиентов:', font=('Adobe Clean Light', 16, 'bold'))
        label_total_user.place(x=20, y=500)

        self.label_total_user_info = tk.Label(font=('Adobe Clean Light', 14, 'italic'), fg='dark blue')
        self.label_total_user_info.place(x=200, y=502)

        label_total_goods = tk.Label(text='Куплено за месяц ', font=('Adobe Clean Light', 16, 'bold'))
        label_total_goods.place(x=20, y=550)

        self.label_total_goods_per_month = tk.Label(font=('Adobe Clean Light', 14, 'italic'), fg='dark blue')
        self.label_total_goods_per_month.place(x=310, y=553)

        # *************************** Кнопки между таблицами *****************************************************
        self.arrow_image = tk.PhotoImage(file='image/arrow.png')  # Allowed PPM, PNG, JPEG, GIF, TIFF, and BMP.
        button_show = tk.Button(command=lambda: [self.show_table_user_goods(self.table_users.item(item)['values'][0])
                                                 for item in self.table_users.selection()], image=self.arrow_image,
                                bd=0)
        button_show.place(x=525, y=110)

        self.graphic_image = tk.PhotoImage(file='image/graphic.png')
        button_show = tk.Button(image=self.graphic_image, bd=0)
        button_show.place(x=530, y=200)

        self.diagram_image = tk.PhotoImage(file='image/diagram.png')
        button_show = tk.Button(image=self.diagram_image, bd=0)
        button_show.place(x=530, y=310)

        # **************************** Кнопки под ЛЕВОЙ таблицей ********************************************
        button_add_user = tk.Button(text='Добавить клиента', command=lambda: self.show_add_user_window(self.root))
        button_add_user.place(x=20, y=420)

        button_edit_user = tk.Button(text='Редактировать', command=lambda: self.show_edit_user_window(self.root))
        button_edit_user.place(x=150, y=420)

        button_delete_user = tk.Button(text='Удалить запись', command=lambda: self.delete_user_from_db())
        button_delete_user.place(x=300, y=420)

        # **************************** Кнопки под ПРАВОЙ таблицей ********************************************
        button_add_goods = tk.Button(text='Добавить товар',
                                     command=lambda: self.show_add_goods_window())
        button_add_goods.place(x=650, y=360)

        button_edit_goods = tk.Button(text='Редактировать', command=self.show_edit_goods_window)
        button_edit_goods.place(x=750, y=360)

        button_delete_goods = tk.Button(text='Обнулить  запись', command=self.reset_goods)
        button_delete_goods.place(x=844, y=360)

        # ***************************** КНОПКА ДЛЯ
        self.combobox_month = ttk.Combobox(values=MONTH, width=10)
        self.combobox_month.bind("<<ComboboxSelected>>", lambda event: self.callback(event))
        self.combobox_month.current(0)
        self.combobox_month.place(x=210, y=557)

        # **************************************** Левая таблица *****************************************
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

        # Scrollbar <ttk.Scrollbar> on frame_users
        vsb = ttk.Scrollbar(frame_users, orient="vertical", command=self.table_users.yview)
        vsb.pack(side='right', fill='y')
        self.table_users.configure(yscrollcommand=vsb.set)

        # ***************************************** Правая таблица *******************************************
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

        # ******************************************* Конструируем 'Меню' *****************************************
        self.menu_bar = tk.Menu(self.root)
        self.root.config(menu=self.menu_bar)

        # 'Файл'
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Открыть...")
        file_menu.add_command(label="Сохранить...")
        file_menu.add_command(label="Выход", command=self.quit())
        self.menu_bar.add_cascade(label='Файл', menu=file_menu)

        # 'Редактировать'
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label='Добавить клиента', command=lambda: AddUser(self.root))
        edit_menu.add_command(label='Добавить товар', command=lambda: self.show_add_goods_window())

        # Конструируем подменю
        edit_choice = tk.Menu(edit_menu, tearoff=0)
        edit_choice.add_command(label='Данные клиента')
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

        # ***************************** ВЫВОДИМ ИНФОРМАЦИЮ 'ИТОГО' ***************************************************

        self.update_label_total_user_info()
        self.update_label_total_goods_per_month()

    # ********************************* ФУНКЦИИ ОБНОВЛЕНИЯ ДАННЫХ 'ИТОГО' ********************************************

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

    # ************************************* ФУНКЦИИ ДЛЯ ОТОБРАЖЕНИЯ ТАБЛИЦ **************************************

    def show_table_users(self):
        [self.table_users.delete(i) for i in self.table_users.get_children()]
        [self.table_users.insert('', 'end', values=(user.id, user.last_name, user.first_name, user.birthday))
         for user in self.db.session.query(User).filter().all()]

    def show_table_user_goods(self, user_id: str):
        [self.table_goods.delete(i) for i in self.table_goods.get_children()]
        [self.table_goods.insert('', 'end', values=(goods.id, goods.user_id, goods.month, goods.goods))
         for goods in self.db.session.query(Goods).filter(Goods.user_id == user_id).all()]

        # Изменяем состояние главного окна
        self.main_window_current_state['user_id'] = user_id
        for user in self.db.session.query(User).filter(User.id == user_id).all():
            self.main_window_current_state['user_name'] = [user.last_name, user.first_name]

    # ********************* ОБРАБОТКА НАЖАТИЯ КНОПОК В ГЛАВНОМ ОКНЕ = ОТОБРАЖЕНИЕ НОВЫХ ОКОН ***********************

    @staticmethod
    def show_add_user_window(my_root: tk.Tk):
        AddUser(my_root)

    def show_edit_user_window(self, my_root: tk.Tk):
        # Полготавливаем данные для передачи в класс EditUser, берем их
        if self.table_users.selection() != ():
            first_name = last_name = birthday = ''
            keys = ['last_name', 'first_name', 'day', 'month', 'year']
            for record in self.table_users.selection():
                first_name = self.table_users.item(record)['values'][1]
                last_name = self.table_users.item(record)['values'][2]
                birthday = self.table_users.item(record)['values'][3]
            birthday_list = birthday.split('/')
            values = [first_name, last_name] + birthday_list

            # Формируем данные и вызываем окно EditUser
            current_user_info = dict(zip(keys, values))
            print(current_user_info)
            EditUser(my_root, current_user_info)

    def show_add_goods_window(self, dict_state: dict):
        if self.current_selected_user_id is not None:
            if self.table_goods.selection() != ():
                for item in self.table_goods.selection():
                    self.main_window_current_state['month'] = self.table_goods.item(item)['values'][2]
            AddGoods(self.root, dict_state)

    def show_edit_goods_window(self, dict_state: dict):
        if dict_state['user_id'] != '':
            if self.table_goods.selection() != ():
                # Нужно эти переменные передать в EditGoods в кач-ве переменных(возможно, они могут быть локальными)
                for item in self.table_goods.selection():
                    self.current_selected_month = self.table_goods.item(item)['values'][2]
                    self.current_selected_goods = self.table_goods.item(item)['values'][3]

            EditGoods(self.root, dict_state)

    # Сбрасываем текущее состояние главного окна
    def reset_main_window_state(self):
        self.main_window_current_state['user_id'] = ''
        self.main_window_current_state['user_name'] = ''
        self.main_window_current_state['month'] = ['', '']
        self.main_window_current_state['goods'] = 0

    # **************************** ОБРАБОТКА НАЖАТИЯ КНОПОК В ДОЧЕРНИХ ОКНАХ = ************************************
    # ********************** = РАБОТА С БАЗОЙ ДАННЫХ + ОБНОВЛЕНИЕ ДАННЫХ ИТОГО И СОСТОЯНИЯ ГЛАВНОГО ОКНА ************

    def add_user_to_db(self, user_first_name: str, user_last_name: str, birthday: str):
        user = User(user_last_name, user_first_name, birthday)
        self.db.record_user(user)

        # Перерисовываем таблицу пользователей обновляем данные ИТОГО
        self.show_table_users()
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
            self.show_table_users()

    def edit_user_in_db(self):
        pass

    def add_goods_to_db(self):
        pass

    def edit_goods_in_db(self):
        pass



    def reset_goods(self):
        for goods in self.table_goods.selection():
            goods_id = self.table_goods.item(goods)['values'][0]
            user_id = self.table_goods.item(goods)['values'][1]
            self.db.reset_goods(goods_id)
            self.show_table_user_goods(user_id)
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

        button_add = tk.Button(self, text='Добавить', padx=5, pady=5, width=15, bg='light gray',
                               command=lambda: self.on_click())
        button_add.place(x=40, y=120)

        button_cancel = tk.Button(self, text='Отмена', padx=5, pady=5, width=15, bg='light gray',
                                  command=lambda: self.destroy())
        button_cancel.place(x=200, y=120)

    def on_click(self):
        user_first_name = self.entry_first_name.get()
        user_last_name = self.entry_last_name.get()

        if user_first_name.isalpha() and user_last_name.isalpha():
            birthday = self.combobox_days.get() + '/' + \
                       self.combobox_month.get() + '/' + \
                       self.combobox_year.get()
            self.main_window.add_user_to_db(user_first_name, user_last_name, birthday)
            self.destroy()


class EditUser(AddUser):
    def __init__(self, my_root: tk.Tk, selected_user_data: dict):  # ['last_name', 'first_name', 'day', 'month', 'year']
        super().__init__(my_root)
        self.selected_user_data = selected_user_data
        self.init_ui()

    def init_ui(self):
        self.title('Редактировать...')
        # ************ ПЕРЕОПРЕДЕЛИМ СОСТОЯНИЕ ПОЛЕЙ ВВОДА, ИСПОЛЬЗУЯ ПЕРЕМЕННУЮ self.selected_user_data ***********

        # Устанавливаем имя
        self.entry_first_name_text = tk.StringVar()
        self.entry_first_name.configure(textvariable=self.entry_first_name_text)
        self.entry_first_name_text.set(self.selected_user_data['first_name'])

        # Устанавливаем фамилию
        self.entry_last_name_text = tk.StringVar()
        self.entry_last_name.configure(textvariable=self.entry_last_name_text)
        self.entry_last_name_text.set(self.selected_user_data['last_name'])

        # Устанавливаем дату рождения
        self.combobox_days.current(DAYS.index(int(self.selected_user_data['day'])))
        self.combobox_month.current(MONTH.index(self.selected_user_data['month']))
        self.combobox_year.current(YEARS.index(int(self.selected_user_data['year'])))





if __name__ == "__main__":
    root = tk.Tk()
    db = DatabaseEngine()
    app = Main(root)
    app.pack()
    root.title("Warehouse Interface")
    root.geometry("1000x650+100+50")
    root.resizable(False, False)
    root.mainloop()