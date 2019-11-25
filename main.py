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
from tkinter import font
from src.TableItems import User, Goods
from src.DatabaseEngine import DatabaseEngine


class Main(tk.Frame):
    def __init__(self, root):
        super().__init__(root)
        self.root = root
        self.menu_bar = menu_bar
        self.tree_users = self.tree_goods = self.combobox_month = self.label_total_info = self.label_total_goods = None
        self.init_main()
        self.db = db
        self.view_table_users()
        # self.view_user_goods_table('1')

    def init_main(self):
        #  ************************************** Главное окно ******************************************************
        # Labels
        label_table_name_users = tk.Label(text='Список клиентов', font=('Adobe Clean Light', 18, 'bold'))
        label_table_name_users.place(x=160, y=20)

        label_table_name_goods = tk.Label(text='Куплено товара', font=('Adobe Clean Light', 18, 'bold'))
        label_table_name_goods.place(x=730, y=20)

        label_total_user = tk.Label(text='Всего клиентов:', font=('Adobe Clean Light', 16, 'bold'))
        label_total_user.place(x=20, y=500)

        self.label_total_info = tk.Label(text='OK', font=('Adobe Clean Light', 12, 'italic'))
        self.label_total_info.place(x=175, y=505)

        label_total_goods = tk.Label(text='Куплено за месяц ', font=('Adobe Clean Light', 16, 'bold'))
        label_total_goods.place(x=20, y=550)

        self.label_total_goods = tk.Label(text='GO', font=('Adobe Clean Light', 12, 'italic'))
        self.label_total_goods.place(x=290, y=555)

        month = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
                 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
        self.combobox_month = ttk.Combobox(values=month, width=10)
        self.combobox_month.current(0)
        self.combobox_month.place(x=195, y=557)

        # *************************** Кнопки между таблицами *****************************************************
        button_show = tk.Button(text='Отобразить данные',                 # getting user_id from selection, item -> dict
                                command=lambda: [self.view_user_goods_table(self.tree_users.item(item)['values'][0])
                                                 for item in self.tree_users.selection()])
        button_show.place(x=515, y=100)

        button_show = tk.Button(text='График')
        button_show.place(x=515, y=200)

        button_show = tk.Button(text='Диаграмма')
        button_show.place(x=515, y=300)

        # **************************** Кнопки под ЛЕВОЙ таблицей ********************************************
        button_add_user = tk.Button(text='Добавить клиента', command=lambda: AddUser(self.root))
        button_add_user.place(x=20, y=420)

        button_edit_user = tk.Button(text='Редактировать')
        button_edit_user.place(x=150, y=420)

        button_delete_user = tk.Button(text='Удалить запись', command=self.delete_user)
        button_delete_user.place(x=300, y=420)

        # **************************** Кнопки под ПРАВОЙ таблицей ********************************************
        button_add_goods = tk.Button(text='Добавить товар', command=lambda: AddGoods(self.root))
        button_add_goods.place(x=650, y=360)

        button_edit_goods = tk.Button(text='Редактировать')
        button_edit_goods.place(x=750, y=360)

        button_delete_goods = tk.Button(text='Обнулить  запись', command=self.reset_goods)
        button_delete_goods.place(x=844, y=360)

        # **************************************** Левая таблица *****************************************
        frame_users = tk.Frame()
        frame_users.place(x=20, y=80)

        self.tree_users = ttk.Treeview(frame_users, columns=('ID', 'last_name', 'first_name', 'birthday'),
                                       height=15, show='headings', selectmode='browse')
        self.tree_users.column("ID", width=45, anchor=tk.CENTER)
        self.tree_users.column("last_name", width=150, anchor=tk.CENTER)
        self.tree_users.column("first_name", width=150, anchor=tk.CENTER)
        self.tree_users.column("birthday", width=110, anchor=tk.CENTER)

        self.tree_users.heading("ID", text='ID')
        self.tree_users.heading("last_name", text='Фамилия')
        self.tree_users.heading("first_name", text='Имя')
        self.tree_users.heading("birthday", text='Дата рождения')

        self.tree_users.pack(side='left')

        # Scrollbar <ttk.Scrollbar> on frame_users
        vsb = ttk.Scrollbar(frame_users, orient="vertical", command=self.tree_users.yview)
        vsb.pack(side='right', fill='y')
        self.tree_users.configure(yscrollcommand=vsb.set)

        # ***************************************** Правая таблица *******************************************
        frame_goods = tk.Frame()
        frame_goods.place(x=650, y=80)

        self.tree_goods = ttk.Treeview(frame_goods, columns=('ID', 'user_id', 'month', 'goods'),
                                       height=12, show='headings', selectmode='browse')
        self.tree_goods.column("ID", width=40, anchor=tk.CENTER)
        self.tree_goods.column("user_id", width=70, anchor=tk.CENTER)
        self.tree_goods.column("month", width=100, anchor=tk.CENTER)
        self.tree_goods.column("goods", width=100, anchor=tk.CENTER)

        self.tree_goods.heading("ID", text='ID')
        self.tree_goods.heading("user_id", text='ID Клиента')
        self.tree_goods.heading("month", text='Месяц')
        self.tree_goods.heading("goods", text='Товар')

        self.tree_goods.pack(side='left')

        # ******************************************* Конструируем 'Меню' *****************************************
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Открыть...")
        file_menu.add_command(label="Сохранить...")
        file_menu.add_command(label="Выход", command=self.on_exit)
        self.menu_bar.add_cascade(label='Файл', menu=file_menu)

        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label='Добавить клиента', command=lambda: AddUser(self.root))
        edit_menu.add_command(label='Добавить товар', command=lambda: AddGoods(self.root))
        # Конструируем подменю
        edit_choice = tk.Menu(edit_menu, tearoff=0)
        edit_choice.add_command(label='Данные клиента')
        edit_choice.add_command(label='Товар клиента')
        edit_menu.add_cascade(label='Редактировать', menu=edit_choice)
        self.menu_bar.add_cascade(label='Редактировать', menu=edit_menu)

        graphic_menu = tk.Menu(self.menu_bar, tearoff=0)
        graphic_menu.add_command(label='График товаров')
        graphic_menu.add_command(label='Диаграмма товаров')
        self.menu_bar.add_cascade(label='График', menu=graphic_menu)

        help_menu = tk.Menu(self.menu_bar, tearoff=0)
        help_menu.add_command(label='О программе')
        self.menu_bar.add_cascade(label='Справка', menu=help_menu)

    def on_exit(self):
        self.quit()

    def delete_user(self):
        # Getting id's of selected users and delete them
        for item in self.tree_users.selection():
            user_id = self.tree_users.item(item)['values'][0]
            self.db.delete_user(user_id)
            self.db.delete_goods(user_id)
            for goods in self.tree_goods.selection():
                if self.tree_goods.item(goods)['values'][0] == user_id:
                    [self.tree_goods.delete(i) for i in self.tree_goods.get_children()]
        self.tree_users.delete()

        self.view_table_users()

    def view_table_users(self):
        [self.tree_users.delete(i) for i in self.tree_users.get_children()]
        [self.tree_users.insert('', 'end', values=(user.id, user.last_name, user.first_name, user.birthday))
         for user in self.db.session.query(User).filter().all()]

    def view_user_goods_table(self, user_id):
        [self.tree_goods.delete(i) for i in self.tree_goods.get_children()]
        [self.tree_goods.insert('', 'end', values=(goods.id, goods.user_id, goods.month, goods.goods))
         for goods in self.db.session.query(Goods).filter(Goods.user_id == user_id).all()]

    def reset_goods(self):
        for goods in self.tree_goods.selection():
            goods_id = self.tree_goods.item(goods)['values'][0]
            user_id = self.tree_goods.item(goods)['values'][1]
            self.db.reset_goods(goods_id)
            self.view_user_goods_table(user_id)

    def view_total_users(self):
        pass

    def view_total_goods(self):
        pass


class AddUser(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        # self.grab_set()
        self.birthday = None
        self.view = app
        self.init_window()

    def init_window(self):
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

        month = ['Января', 'Февраля', 'Марта', 'Апреля', 'Мая', 'Июня',
                 'Июля', 'Августа', 'Сентября', 'Октября', 'Ноября', 'Декабря']
        combobox_month = ttk.Combobox(self, values=month, width=10)
        combobox_month.current(0)
        combobox_month.place(x=188, y=80)

        combobox_year = ttk.Combobox(self, values=[x for x in range(1950, 2010)], width=5)
        combobox_year.current(30)
        combobox_year.place(x=275, y=80)

        # **************************************** row 4 ********************************************
        boxes = [combobox_days, combobox_month, combobox_year]
        button_edit = tk.Button(self, text='Добавить', padx=5, pady=5, width=15, bg='light gray',
                                command=lambda: self.insert_user(entry_last_name, entry_first_name, boxes))
        button_edit.place(x=40, y=120)

        button_cancel = tk.Button(self, text='Отмена', padx=5, pady=5, width=15, bg='light gray',
                                  command=lambda: self.cancel())
        button_cancel.place(x=200, y=120)

    def insert_user(self, entry_last, entry_first, boxes):
        name = entry_first.get() + entry_last.get()

        if name:
            birthday = "/".join([item.get() for item in boxes])
            user = User(entry_last.get().strip(), entry_first.get().strip(), birthday)
            self.view.db.record_user(user)
            self.view.view_table_users()
            self.view.view_user_goods_table(user.id)
            self.destroy()

    def cancel(self):
        self.destroy()


class AddGoods(tk.Toplevel):
    def __init__(self, root):
        super().__init__(root)
        self.label_client_info = None
        self.combobox_month = None
        self.view = app
        self.init_ui()

    def init_ui(self):
        self.title('Добавить товар')
        self.geometry('360x180+680+400')
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

    def insert_goods(self, user_id, month, amount):
        if amount:

            goods = Goods(user_id, month, amount)
            self.view.db.insert_goods(goods)
            self.view.view_user_goods_table()
            # self.destroy()
        else:
            self.destroy()

    def cancel(self):
        self.destroy()


class EditUser(tk.Toplevel):
    pass


class EditGoods(tk.Toplevel):
    pass


if __name__ == "__main__":
    root = tk.Tk()

    menu_bar = tk.Menu(root)
    root.config(menu=menu_bar)

    db = DatabaseEngine()
    app = Main(root)
    app.pack()
    root.title("Warehouse Interface")
    root.geometry("1000x800+400+100")
    root.resizable(False, False)
    root.mainloop()
