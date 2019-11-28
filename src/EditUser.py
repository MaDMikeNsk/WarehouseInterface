from src.AddUser import AddUser


class EditUser(AddUser):
    def __init__(self, my_root, main_window_current_state):
        super().__init__(my_root)
        self.current_state = main_window_current_state
        self.init_ui()

    def init_ui(self):
        self.title('Редактировать...')