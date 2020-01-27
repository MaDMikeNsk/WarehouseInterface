from windows.AddUser import AddUser
from windows.EditUser import EditUser
from windows.AddGoods import AddGoods
from windows.EditGoods import EditGoods
from src.TableItems import User


class AppManager:

    def __init__(self, app, root):
        self.main_app = app
        self.root = root

    # ==================================================================================================================
    #                          ФУНКЦИИ ДЛЯ ОБРАБОТКИ НАЖАТИЯ КНОПОК В ГЛАВНОМ ОКНЕ
    # ==================================================================================================================
    # Кнопка 'Добавить' (под левой таблицей) - отображаем окно
    def display_add_user_window(self):
        AddUser(self.root, self.main_app)

    # Кнопка 'Редактировать' (под левой таблицей)
    def display_edit_user_window(self):
        if len(self.main_app.table_users.selection()) == 1:
            selected_user = self.main_app.get_data_from_user_selection()
            EditUser(self.root, self.main_app, selected_user)

    # Кнопка 'Добавить' (под правой таблицей)
    def display_add_goods_window(self):
        if self.main_app.main_window_state['user_id'] != '':
            if self.main_app.table_goods.selection() != ():
                data = self.main_app.get_data_from_goods_selection()  # dict
                AddGoods(self.root, self.main_app, data)
            else:
                AddGoods(self.root, self.main_app)

    # Кнопка 'Редактировать' (под правой таблицей)
    def display_edit_goods_window(self):
        if self.main_app.main_window_state['goods_visible']:
            if self.main_app.table_goods.selection() != ():
                selected_goods = self.main_app.get_data_from_goods_selection()
                EditGoods(self.root, self.main_app, selected_goods)
            else:
                EditGoods(self.root, self.main_app, selected_goods=None)