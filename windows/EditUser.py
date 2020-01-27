import tkinter as tk
from windows.AddUser import AddUser

DAYS = [x for x in range(1, 32)]
MONTH = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
         'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
YEARS = [x for x in range(1950, 2010)]


class EditUser(AddUser):
    def __init__(self,  my_root: tk.Tk, app, current_user_info: list):
        super().__init__(my_root, app)
        self.entry_first_name_text = \
            self.entry_last_name_text = None
        self.current_user_info = current_user_info[0]
        self.main_app = app
        self.init_ui()

    def init_ui(self):
        self.title('Редактировать данные клиента')
        # ==============================================================================================================
        #                  ПЕРЕОПРЕДЕЛИМ ТЕКСТ ПОЛЕЙ ВВОДА, ИСПОЛЬЗУЯ ПЕРЕМЕННУЮ self.current_user_info
        # ==============================================================================================================
        # Устанавливаем имя
        entry_first_name_text = tk.StringVar()
        self.entry_first_name.configure(textvariable=entry_first_name_text)
        entry_first_name_text.set(self.current_user_info['user_name'][0])

        # Устанавливаем фамилию
        entry_last_name_text = tk.StringVar()
        self.entry_last_name.configure(textvariable=entry_last_name_text)
        entry_last_name_text.set(self.current_user_info['user_name'][1])

        # Устанавливаем дату рождения
        self.combobox_days.current(DAYS.index(int(self.current_user_info['birthday'][0])))
        self.combobox_month.current(MONTH.index(self.current_user_info['birthday'][1]))
        self.combobox_year.current(YEARS.index(int(self.current_user_info['birthday'][2])))

        # Меняем иконку кнопки
        self.button_add.config(image=self.main_app.edit_img)

    # Обработка нажатия на кнопку 'Редактировать' (переопределяем метод)
    def on_click(self):
        # Формируем данные для передачи в функцию update_user из базы данных
        user_id = self.current_user_info['user_id']
        first_name = self.entry_first_name.get()
        last_name = self.entry_last_name.get()
        birthday = self.combobox_days.get() + '/' + self.combobox_month.get() + '/' + self.combobox_year.get()

        # Если ввод не пустой, то редактируем запись в базе и обновляем таблицу
        if first_name + last_name != '':
            self.main_app.db.update_user(user_id, first_name, last_name, birthday)
            self.main_app.display_table_users()
            self.destroy()
