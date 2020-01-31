from windows.AddUser import AddUser
from windows.EditUser import EditUser
from windows.AddGoods import AddGoods
from windows.EditGoods import EditGoods
from windows.Graphic import Graphic
from windows.Diagram import Diagram
from src.TableItems import User
from tkinter import messagebox as mb


class AppManager:

    def __init__(self, app, root):
        self.main_app = app
        self.root = root

    # ==================================================================================================================
    #                       РЕАКЦИЯ НА НАЖАТИЕ КНОПОК В ГЛАВНОМ ОКНЕ = ОТОБРАЖЕНИЕ ДОЧЕРНИХ ОКОН
    # ==================================================================================================================
    # Кнопка 'Добавить' (под левой таблицей)
    def display_add_user_window(self):
        AddUser(self.root, self.main_app)

    # Кнопка 'Редактировать' (под левой таблицей)
    def display_edit_user_window(self):
        if len(self.main_app.table_users.selection()) == 1:
            selected_user = self.main_app.get_data_from_user_selection()
            EditUser(self.root, self.main_app, selected_user)

    # Кнопка 'Добавить' (под правой таблицей)
    def display_add_goods_window(self):
        if self.main_app.main_window_state['user_id']:
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

    # Кнопка "График"
    def display_graphic(self):
        if 0 < len(self.main_app.table_users.selection()) <= 4:
            users_list = self.main_app.get_data_from_user_selection()  # list of dict (selected users)
            data_to_display = []
            for user in users_list:
                data = dict()
                data['user_name'] = user['user_name'][0] + ' ' + user['user_name'][1]
                data['values'] = self.main_app.get_goods_values_of_user(user['user_id'])  # List of goods values
                data_to_display.append(data)
            Graphic(self.root, data_to_display)
        elif len(self.main_app.table_users.selection()) > 4:
            mb.showerror("Ошибка", "Выберите не более четырех клиентов")

    # Кнопка "Диаграмма"
    def display_diagram(self):
        if 0 < len(self.main_app.table_users.selection()) <= 4:
            users_list = self.main_app.get_data_from_user_selection()  # list of dict (selected users)
            data_to_display = []
            for user in users_list:
                data = dict()
                data['user_name'] = user['user_name'][0] + ' ' + user['user_name'][1]
                data['values'] = self.main_app.get_goods_values_of_user(user['user_id'])  # List of goods values
                data_to_display.append(data)
            Diagram(self.root, data_to_display)
        elif len(self.main_app.table_users.selection()) > 4:
            mb.showerror("Ошибка", "Выберите не более четырех клиентов")

    # Кнопка "Стрелка"
    def on_click_arrow_button(self):
        if len(self.main_app.table_users.selection()) == 1:
            selected_user = self.main_app.get_data_from_user_selection()[0]
            self.main_app.display_user_goods_table(selected_user['user_id'])
            self.main_app.set_main_window_state(user_id=selected_user['user_id'],
                                                user_name=selected_user['user_name'],
                                                is_display=True)
            self.main_app.label_current_displayed_user.\
                config(text=f"{selected_user['user_name'][0]} {selected_user['user_name'][1]}")

    # Кнопка 'Удалить запись' (под левой таблицей)
    def delete_user_from_db(self):
        if len(self.main_app.table_users.selection()) > 0:
            # Получаем ID пользователей, которых выбрали в таблице
            selected_users = self.main_app.get_data_from_user_selection()

            # Удаляем из базы пользователя и все записи из 2-й таблицы по его ID
            for user in selected_users:
                self.main_app.db.delete_user(user['user_id'])
                self.main_app.db.delete_goods(user['user_id'])

                # Если отображалась таблица его товаров - удаляем её и
                # сбрасываем параметры main_window_state
                if self.main_app.main_window_state['user_id'] == user['user_id']:
                    [self.main_app.table_goods.delete(i) for i in self.main_app.table_goods.get_children()]
                    # Обнуляем состояние преременной main_window_state
                    self.main_app.set_main_window_state(user_id='', user_name=[], is_display=False)
                    # ...и скрываем метку с именем отображаемого клиента
                    self.main_app.label_current_displayed_user.config(text='')

            # Пересчитываем параметры 'ИТОГО' и удаляем записи из таблицы
            self.main_app.update_label_total_user_info()
            self.main_app.update_label_total_goods_per_month()
            for item in self.main_app.table_users.selection():
                self.main_app.table_users.delete(item)
