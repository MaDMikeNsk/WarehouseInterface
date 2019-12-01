from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.TableItems import User, Goods

MONTH = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
         'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']


class DatabaseEngine:
    def __init__(self):
        self.engine = create_engine('sqlite:///database/Warehouse.db', echo=False)
        session = sessionmaker(bind=self.engine)
        self.session = session()

    def record_user(self, user):
        # Добавляем пользователя user в таблицу User...
        self.session.add(user)
        self.session.commit()

        # ...и 12 записей в таблицу Goods по его ID
        for x in range(12):
            goods = Goods(user.id, MONTH[x], goods=25)
            self.record_goods(goods)

    def update_user(self, user_id, first_name, last_name, birthday):
        for user in self.session.query(User).filter(User.id == user_id):
            user.first_name = first_name
            user.last_name = last_name
            user.birthday = birthday
        self.session.commit()

    def delete_user(self, user_id):
        for user in self.session.query(User).filter(User.id == user_id).all():
            self.session.delete(user)
            self.session.commit()

    def record_goods(self, goods):
        self.session.add(goods)
        self.session.commit()

    def reset_goods(self, user_id, month):
        for goods in self.session.query(Goods).filter(Goods.user_id == user_id,
                                                      Goods.month == month).all():
            goods.goods = 0
        self.session.commit()

    def delete_goods(self, user_id):
        for goods in self.session.query(Goods).filter(Goods.user_id == user_id).all():
            self.session.delete(goods)
            self.session.commit()

    def add_goods_for_this_month(self, user_id, month, goods: int):
        for record in self.session.query(Goods).filter(Goods.user_id == user_id, Goods.month == month).all():
            record.goods = int(record.goods) + goods
        self.session.commit()

    def update_goods(self, user_id, month, goods):
        for record in self.session.query(Goods).filter(Goods.user_id == user_id, Goods.month == month).all():
            record.goods = goods
        self.session.commit()

    # КОСТЫЛЬ! функция нужна для отображени текущего значения goods
    # для пользователя при выборе месяца в окне 'Редактировать товар'
    def get_goods_amount(self, user_id, month):
        result = ''
        for record in self.session.query(Goods).filter(Goods.user_id == user_id, Goods.month == month).all():
            result = record.goods
        return result
