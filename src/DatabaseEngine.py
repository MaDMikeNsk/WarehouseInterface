from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from src.TableItems import User, Goods


class DatabaseEngine:
    def __init__(self):
        self.engine = create_engine('sqlite:///database/Warehouse.db', echo=True)
        session = sessionmaker(bind=self.engine)
        self.session = session()

    def record_user(self, user):
        self.session.add(user)
        self.session.commit()
        month = ['Январь', 'Февраль', 'Март', 'Апрель', 'Май', 'Июнь',
                 'Июль', 'Август', 'Сентябрь', 'Октябрь', 'Ноябрь', 'Декабрь']
        for x in range (12):
            goods = Goods(user.id, month[x], goods=25)
            self.session.add(goods)
        self.session.commit()

    def delete_user(self, user_id):
        for user in self.session.query(User).filter(User.id == user_id).all():
            self.session.delete(user)
            self.session.commit()

    def record_goods(self, goods):
        self.session.add(goods)
        self.session.commit()

    def reset_goods(self, goods_id):
        for goods in self.session.query(Goods).filter(Goods.id == goods_id).all():
            goods.goods = 0
            self.session.commit()

    def delete_goods(self, user_id):
        for goods in self.session.query(Goods).filter(Goods.user_id == user_id).all():
            self.session.delete(goods)
            self.session.commit()

    def update_goods(self, user_id, month, goods_amount: int):
        for goods in self.session.query(Goods).filter(Goods.user_id == user_id, Goods.month == month).all():
            res = int(goods.goods) + goods_amount
            goods.goods = res

