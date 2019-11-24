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
        self.init_main()
        self.db = db
        # self.view_records()

    def init_main(self):
        #  ************ Главное окно ******************
        # Labels
        label_table_name_users = tk.Label(text='Список клиентов', font=('Adobe Clean Light', 18, 'bold'))
        label_table_name_users.place(x=160, y=20)

        label_table_name_goods = tk.Label(text='Куплено товара', font=('Adobe Clean Light', 18, 'bold'))
        label_table_name_goods.place(x=730, y=20)

        label_total_user = tk.Label(text='Всего клиентов:', font=('Adobe Clean Light', 15, 'italic'))
        label_total_user.place(x=20, y=500)

        label_total_goods = tk.Label(text='Куплено за месяц ', font=('Adobe Clean Light', 15, 'italic'))
        label_total_goods.place(x=20, y=570)

        month = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
                 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
        self.combobox_month = ttk.Combobox(values=month, width=10)
        self.combobox_month.current(0)
        self.combobox_month.place(x=170, y=577)

        # Кнопки
        button_show = tk.Button(text='Отобразить данные')
        button_show.place(x=515, y=100)

        button_show = tk.Button(text='График')
        button_show.place(x=515, y=200)

        button_show = tk.Button(text='Диаграмма')
        button_show.place(x=515, y=300)

        # Кнопки под ЛЕВОЙ таблицей
        button_add_user = tk.Button(text='Добавить клиента', command=lambda: User(self.root))
        button_add_user.place(x=20, y=420)

        button_edit_user = tk.Button(text='Редактировать')
        button_edit_user.place(x=150, y=420)

        button_delete_user = tk.Button(text='Удалить запись')
        button_delete_user.place(x=300, y=420)

        # Кнопки под ПРАВОЙ таблицей
        button_add_goods = tk.Button(text='Добавить товар', command=lambda: Goods(self.root))
        button_add_goods.place(x=650, y=420)

        button_edit_goods = tk.Button(text='Редактировать')
        button_edit_goods.place(x=750, y=420)

        button_delete_goods = tk.Button(text='Удалить запись')
        button_delete_goods.place(x=844, y=420)
        # *********** Левая таблица *****************
        frame_users = tk.Frame()
        frame_users.place(x=20, y=80)

        tree_users = ttk.Treeview(frame_users, columns=('ID', 'last_name', 'first_name', 'birthday'),
                                  height=15, show='headings', selectmode='extended')
        tree_users.column("ID", width=45, anchor=tk.CENTER)
        tree_users.column("last_name", width=180, anchor=tk.CENTER)
        tree_users.column("first_name", width=150, anchor=tk.CENTER)
        tree_users.column("birthday", width=100, anchor=tk.CENTER)

        tree_users.heading("ID", text='ID')
        tree_users.heading("last_name", text='Фамилия')
        tree_users.heading("first_name", text='Имя')
        tree_users.heading("birthday", text='Дата рождения')

        tree_users.pack(side='left')

        # Scrollbar <ttk.Scrollbar> on frame_users
        vsb = ttk.Scrollbar(frame_users, orient="vertical", command=tree_users.yview)
        vsb.pack(side='right', fill='y')
        tree_users.configure(yscrollcommand=vsb.set)

        # ************ Правая таблица ****************
        frame_goods = tk.Frame()
        frame_goods.place(x=650, y=80)

        tree_goods = ttk.Treeview(frame_goods, columns=('ID', 'user_id', 'month', 'goods'),
                                  height=15, show='headings', selectmode='extended')
        tree_goods.column("ID", width=40, anchor=tk.CENTER)
        tree_goods.column("user_id", width=70, anchor=tk.CENTER)
        tree_goods.column("month", width=100, anchor=tk.CENTER)
        tree_goods.column("goods", width=100, anchor=tk.CENTER)

        tree_goods.heading("ID", text='ID')
        tree_goods.heading("user_id", text='ID Клиента')
        tree_goods.heading("month", text='Месяц')
        tree_goods.heading("goods", text='Товар')
        tree_goods.pack(side='left')

        # *********** Конструируем 'Меню' ***************
        file_menu = tk.Menu(self.menu_bar, tearoff=0)
        file_menu.add_command(label="Открыть...")
        file_menu.add_command(label="Сохранить...")
        file_menu.add_command(label="Выход", command=self.on_exit)
        self.menu_bar.add_cascade(label='Файл', menu=file_menu)

        edit_menu = tk.Menu(self.menu_bar, tearoff=0)
        edit_menu.add_command(label='Добавить клиента', command=lambda: AddUser(self.root))
        edit_menu.add_command(label='Добавить товар', command=lambda: AddGoods(self.root))
        edit_menu.add_command(label='Редактировать')
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

    def insert_user(self):
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
