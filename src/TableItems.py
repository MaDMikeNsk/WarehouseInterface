from sqlalchemy import Column, Integer, TEXT, create_engine
from sqlalchemy.ext.declarative import declarative_base


engine = create_engine('sqlite:///database/Warehouse.db', echo=True)
Base = declarative_base()


class User(Base):
    __tablename__ = 'User'
    id = Column(Integer, autoincrement=True, unique=True, primary_key=True)
    last_name = Column(TEXT)
    first_name = Column(TEXT)
    birthday = Column(TEXT)

    def __init__(self, last_name, first_name, birthday):
        self.last_name = last_name
        self.first_name = first_name
        self.birthday = birthday


class Goods(Base):
    __tablename__ = 'Goods'
    id = Column(Integer, autoincrement=True, unique=True, primary_key=True)
    user_id = Column(Integer)
    month = Column(TEXT)
    goods = Column(TEXT)

    def __init__(self, user_id, month, goods):
        self.user_id = user_id
        self.month = month
        self.goods = goods


Base.metadata.create_all(engine)
