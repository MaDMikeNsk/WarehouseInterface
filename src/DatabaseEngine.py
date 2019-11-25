from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker


class DatabaseEngine:
    def __init__(self):
        self.engine = create_engine('sqlite:///database/Warehouse.db', echo=True)
        session = sessionmaker(bind=self.engine)
        self.session = session()

    def insert_user(self, user):
        self.session.add(user)
        self.session.commit()