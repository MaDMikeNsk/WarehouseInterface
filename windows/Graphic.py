import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg, NavigationToolbar2Tk
import matplotlib.pyplot as plt


MONTH_TWO_LETTERS = ['Ян', 'Фе', 'Мр', 'Ап', 'Мй', 'Ин', 'Ил', 'Ав', 'Се', 'Ок', 'Но', 'Де']
MONTH_SHORT = ['Янв', 'Фев', 'Мар', 'Апр', 'Май', 'Июнь',
               'Июль', 'Авг', 'Сен', 'Окт', 'Ноя', 'Дек']
YEARS = [x for x in range(1950, 2010)]


class Graphic(tk.Toplevel):

    def __init__(self, my_root, data_to_display: list):
        super().__init__(my_root)
        self.root = my_root
        self.init_iu(data_to_display)

    def init_iu(self, data_to_display):
        self.title('График покупки товаров клиентом')
        self.geometry('900x900+100+50')
        k = len(data_to_display)

        month = MONTH_TWO_LETTERS
        if k >= 3:
            row = 2
            column = 2
        elif k == 2:
            row = 1
            column = 2
        else:
            row = 1
            column = 1
            month = MONTH_SHORT

        figure = plt.figure(dpi=90)
        i = 0
        for data in data_to_display:
            i += 1
            graphic = figure.add_subplot(int(str(row) + str(column) + str(i)))
            user_name = data['user_name']
            graphic.plot(month, data['values'], color='blue', marker='o')
            graphic.set(xlabel='ПЕРИОД', ylabel='КОЛИЧЕСТВО ТОВАРА', title=f'{user_name}')
            graphic.grid()

        canvas = FigureCanvasTkAgg(figure, self)
        canvas.get_tk_widget().pack(side=tk.BOTTOM, fill=tk.BOTH, expand=True)

        toolbar = NavigationToolbar2Tk(canvas, self)
        toolbar.update()
        canvas._tkcanvas.pack(side=tk.TOP, fill=tk.BOTH, expand=True)
