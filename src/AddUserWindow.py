import tkinter as tk


class AddUserWindow(tk.Toplevel):
    def __init__(self, *args, **kwargs):
        tk.Toplevel.__init__(self, *args, *kwargs)
        self.geometry('200x200+700+300')
        #self.grab_set()
