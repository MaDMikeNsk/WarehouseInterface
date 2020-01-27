import tkinter as tk

from windows.AddGoods import AddGoods


class EditGoods(AddGoods):
    def __init__(self, my_root, app, selected_goods=None):
        super().__init__(my_root, app, selected_goods)
        self.entry_text = None
        self.selected_goods = selected_goods
        self.init_ui()
        self.grab_set()

    def init_ui(self):
        self.title('Редактировать количество товара')
        self.geometry('360x180+400+400')
        self.resizable(False, False)

        # Добавляем текстовую пременную в entry_goods
        self.entry_text = tk.StringVar()
        self.entry_goods.config(textvariable=self.entry_text)

        # Обработка выбора месяца = отображение кол-ва товара в текущем месяце
        self.combobox_month.bind("<<ComboboxSelected>>", lambda event: self.on_click_month_box())

        # Определяем текст поля entry_goods
        # Если была выделена строка в таблице товаров, то в поле entry_goods установим кол-во товара из этой строки
        if self.selected_goods:
            self.entry_text.set(self.main_app.get_goods_amount(self.selected_goods['user_id'],
                                                               self.selected_goods['month']))
        else:
            # Если нет, установим по дефолту месяц 'Январь' и кол-во товара за 'Январь'
            self.entry_text.set(self.main_app.get_goods_amount(self.main_app.main_window_state['user_id'], 'Январь'))

        # Меняем иконку кнопки
        self.button_add.config(image=self.main_app.edit_img)

    # Действие при выборе месяца - отображаем кол-во товара в поле ввода для этого месяца
    def on_click_month_box(self):
        current_month = self.combobox_month.get()
        self.entry_text.set(self.main_app.get_goods_amount(self.main_app.main_window_state['user_id'], current_month))

    # Обработка нажатия на кнопку 'Редактировать'
    def on_click(self):
        goods_amount = self.entry_goods.get()
        # if self.main_app.is_int(goods_amount):  Функция не нужна, отрицательные значения не берём
        if goods_amount.isdigit():
            # Если то, что ввели, является целым числом (со знаком или без), то вызываем функции из ГЛАВНОГО окна
            self.main_app.db.update_goods(user_id=self.main_app.main_window_state['user_id'],
                                          month=self.combobox_month.get(),
                                          goods=int(goods_amount))
            self.main_app.update_label_total_goods_per_month()
            self.main_app.display_table_user_goods(self.main_app.main_window_state['user_id'])
            self.destroy()
