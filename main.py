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
from src.TableItems import User, Goods
from src.DatabaseEngine import DatabaseEngine


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
            self.current_selected_user_id = \
            self.current_selected_user_name = \
            self.current_selected_month = \
            self.arrow_image = \
            self.graphic_image = \
            self.diagram_image = \
            self.MONTH = None
        self.current_selected_goods = 0
        self.menu_bar = tk.Menu(root)
        self.root.config(menu=self.menu_bar)
        self.init_main()
        self.view_table_users()

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

        self.MONTH = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
                      'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
        self.combobox_month = ttk.Combobox(values=self.MONTH, width=10)
        self.combobox_month.bind("<<ComboboxSelected>>", self.callback)
        self.combobox_month.current(0)
        self.combobox_month.place(x=210, y=557)

        # *************************** Кнопки между таблицами *****************************************************
        self.arrow_image = tk.PhotoImage(file='image/arrow.png')  # Allowed PPM, PNG, JPEG, GIF, TIFF, and BMP.
        button_show = tk.Button(command=lambda: [self.view_table_user_goods(self.table_users.item(item)['values'][0])
                                                 for item in self.table_users.selection()], image=self.arrow_image, bd=0)
        button_show.place(x=525, y=110)

        self.graphic_image = tk.PhotoImage(file='image/graphic.png')
        button_show = tk.Button(image=self.graphic_image, bd=0)
        button_show.place(x=530, y=200)

        self.diagram_image = tk.PhotoImage(file='image/diagram.png')
        button_show = tk.Button(image=self.diagram_image, bd=0)
        button_show.place(x=530, y=310)

        # **************************** Кнопки под ЛЕВОЙ таблицей ********************************************
        button_add_user = tk.Button(text='Добавить клиента', command=lambda: AddUser(self.root))
        button_add_user.place(x=20, y=420)

        button_edit_user = tk.Button(text='Редактировать', command=lambda: self.edit_user(self.root))
        button_edit_user.place(x=150, y=420)

        button_delete_user = tk.Button(text='Удалить запись', command=self.delete_user)
        button_delete_user.place(x=300, y=420)

        # **************************** Кнопки под ПРАВОЙ таблицей ********************************************
        button_add_goods = tk.Button(text='Добавить товар',
                                     command=lambda: self.add_goods())
        button_add_goods.place(x=650, y=360)

        button_edit_goods = tk.Button(text='Редактировать', command=self.edit_goods)
        button_edit_goods.place(x=750, y=360)

        button_delete_goods = tk.Button(text='Обнулить  запись', command=self.reset_goods)
        button_delete_goods.place(x=844, y=360)

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
        # 'Файл'
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Открыть...")
        file_menu.add_command(label="Сохранить...")
        file_menu.add_command(label="Выход", command=self.on_exit)
        self.menu_bar.add_cascade(label='Файл', menu=file_menu)

        # 'Редактировать'
        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label='Добавить клиента', command=lambda: AddUser(self.root))
        edit_menu.add_command(label='Добавить товар', command=lambda: self.add_goods())

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

        # ***************************** Выводим информацию итого ***************************************************
        self.update_label()
        self.update_total_goods_per_month(self.combobox_month.get())

    def callback(self, event):
        self.update_total_goods_per_month(self.combobox_month.get())

    def update_label(self):
        self.label_total_user_info['text'] = len(self.db.session.query(User).filter().all())

    def update_total_goods_per_month(self, month):
        res = 0
        for item in self.db.session.query(Goods).filter(Goods.month == month).all():
            res += int(item.goods)
        self.label_total_goods_per_month['text'] = res

    def delete_user(self):
        # Getting id's of selected users and delete them
        for item in self.table_users.selection():
            user_id = self.table_users.item(item)['values'][0]
            self.db.delete_user(user_id)
            self.db.delete_goods(user_id)
            if self.current_selected_user_id == user_id:
                [self.table_goods.delete(i) for i in self.table_goods.get_children()]
                self.current_selected_user_id = \
                    self.current_selected_user_name = \
                    self.current_selected_month = None
                self.current_selected_goods = 0
        self.update_label()
        self.update_total_goods_per_month(self.combobox_month.get())
        self.view_table_users()

    def view_table_users(self):
        [self.table_users.delete(i) for i in self.table_users.get_children()]
        [self.table_users.insert('', 'end', values=(user.id, user.last_name, user.first_name, user.birthday))
         for user in self.db.session.query(User).filter().all()]

    def view_table_user_goods(self, user_id):
        [self.table_goods.delete(i) for i in self.table_goods.get_children()]
        [self.table_goods.insert('', 'end', values=(goods.id, goods.user_id, goods.month, goods.goods))
         for goods in self.db.session.query(Goods).filter(Goods.user_id == user_id).all()]

        # Присваиваем значения глобальным переменным в зависимости от клика в таблицах
        self.current_selected_user_id = user_id
        self.current_selected_month = None
        self.current_selected_goods = 0

        for user in self.db.session.query(User).filter(User.id == user_id).all():
            self.current_selected_user_name = user.last_name + ' ' + user.first_name

    def reset_goods(self):
        for goods in self.table_goods.selection():
            goods_id = self.table_goods.item(goods)['values'][0]
            user_id = self.table_goods.item(goods)['values'][1]
            self.db.reset_goods(goods_id)
            self.view_table_user_goods(user_id)
        self.update_total_goods_per_month(self.combobox_month.get())

    def add_goods(self):
        if self.current_selected_user_id is not None:
            if self.table_goods.selection() != ():
                for item in self.table_goods.selection():
                    self.current_selected_month = self.table_goods.item(item)['values'][2]

            AddGoods(self.root)

    def edit_goods(self):
        if self.current_selected_user_id is not None:
            if self.table_goods.selection() != ():
                # Нужно эти переменные передать в EditGoods в кач-ве переменных(возможно, они могут быть локальными)
                for item in self.table_goods.selection():
                    self.current_selected_month = self.table_goods.item(item)['values'][2]
                    self.current_selected_goods = self.table_goods.item(item)['values'][3]

            EditGoods(self.root)

    def on_exit(self):
        self.quit()

    def edit_user(self, my_root):
        if self.table_users.selection() != ():
            print(self.table_users.selection())
            EditUser(my_root)

#!
class AddUser(tk.Toplevel):
    def __init__(self, my_root):
        super().__init__(my_root)
        self.birthday = None
        self.view = app
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

        entry_last_name = tk.Entry(self, width=29)
        entry_last_name.place(x=150, y=50)

        # **************************************** row 3 ********************************************
        label_birthday = tk.Label(self, text='ДАТА РОЖДЕНИЯ:')
        label_birthday.place(x=30, y=80)

        combobox_days = ttk.Combobox(self, values=[x for x in range(1, 32)], width=2)
        combobox_days.current(0)
        combobox_days.place(x=150, y=80)

        combobox_month = ttk.Combobox(self, values=self.view.MONTH, width=10)
        combobox_month.current(0)
        combobox_month.place(x=188, y=80)

        combobox_year = ttk.Combobox(self, values=[x for x in range(1950, 2010)], width=5)
        combobox_year.current(30)
        combobox_year.place(x=275, y=80)

        # **************************************** row 4 ********************************************
        boxes = [combobox_days, combobox_month, combobox_year]
        button_edit = tk.Button(self, text='Добавить', padx=5, pady=5, width=15, bg='light gray',
                                command=lambda: self.insert_user(entry_last_name,
                                                                 self.entry_first_name,
                                                                 boxes))
        button_edit.place(x=40, y=120)

        button_cancel = tk.Button(self, text='Отмена', padx=5, pady=5, width=15, bg='light gray',
                                  command=lambda: self.cancel())
        button_cancel.place(x=200, y=120)

    def insert_user(self, entry_last, entry_first, boxes):
        name = entry_first.get() + entry_last.get()

        if name:
            birthday = "/".join([item.get() for item in boxes])
            user = User(entry_last.get().strip(),
                        entry_first.get().strip(),
                        birthday)
            self.view.db.record_user(user)
            self.view.view_table_users()
            self.destroy()
        self.view.update_label()
        self.view.update_total_goods_per_month(self.view.combobox_month.get())

    def cancel(self):
        self.destroy()


class AddGoods(tk.Toplevel):
    def __init__(self, my_root):
        super().__init__(my_root)
        self.label_client_info = \
            self.entry_goods = \
            self.combobox_month = None
        self.view = app
        self.init_ui()
        self.grab_set()

    def init_ui(self):
        self.title('Добавить товар...')
        self.geometry('360x180+400+400')
        self.resizable(False, False)

        # **************************************** row 1 ********************************************
        label_client = tk.Label(self, text='КЛИЕНТ:')
        label_client.place(x=30, y=20)

        self.label_client_info = tk.Label(self, text=self.view.current_selected_user_name,
                                          font=('Adobe Clean Light', 11, 'italic'), fg='gray')
        self.label_client_info.place(x=115, y=20)

        # **************************************** row 2 ********************************************
        label_goods = tk.Label(self, text='МЕСЯЦ:')
        label_goods.place(x=30, y=55)

        self.combobox_month = ttk.Combobox(self, values=self.view.MONTH, width=10)
        if self.view.current_selected_month is not None:
            self.combobox_month.current(self.view.MONTH.index(self.view.current_selected_month))
        else:
            self.combobox_month.current(0)
        self.combobox_month.place(x=115, y=55)

        # **************************************** row 3 ********************************************
        label_month = tk.Label(self, text='ТОВАР (+/-):')
        label_month.place(x=30, y=90)

        self.entry_goods = tk.Entry(self, width=13)
        self.entry_goods.place(x=115, y=90)

        # **************************************** row 4 ********************************************
        button_edit = tk.Button(self, text='Добавить', padx=5, pady=5, width=15, bg='light gray',
                                command=lambda: self.update_goods(self.view.current_selected_user_id,
                                                                  self.combobox_month,
                                                                  self.entry_goods))
        button_edit.place(x=40, y=130)

        button_cancel = tk.Button(self, text='Отмена', padx=5, pady=5, width=15, bg='light gray',
                                  command=lambda: self.cancel())
        button_cancel.place(x=200, y=130)

    def update_goods(self, user_id, combobox_month, entry_goods):
        def is_int(s):
            if s != '':
                if s[0] in ('-', '+'):
                    return s[1:].isdigit()
                return s.isdigit()

        if is_int(entry_goods.get()) and self.view.current_selected_user_id is not None:
            self.view.db.add_goods(user_id, combobox_month.get(), int(entry_goods.get()))
            self.view.view_table_user_goods(user_id)
            self.destroy()
        self.view.update_total_goods_per_month(self.view.combobox_month.get())

    def cancel(self):
        self.destroy()


class EditGoods(tk.Toplevel):
    def __init__(self, my_root):
        super().__init__(my_root)
        self.view = app
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
            self.view.view_table_user_goods(user_id)
            self.view.update_total_goods_per_month(self.view.combobox_month.get())
            self.destroy()

    def cancel(self):
        self.destroy()


class EditUser(AddUser):
    def __init__(self, my_root):
        super().__init__(my_root)
        self.init_ui()

    def init_ui(self):
        self.title('Редактировать...')






if __name__ == "__main__":
    root = tk.Tk()
    db = DatabaseEngine()
    app = Main(root)
    app.pack()
    root.title("Warehouse Interface")
    root.geometry("1000x650+100+50")
    root.resizable(False, False)
    root.mainloop()
