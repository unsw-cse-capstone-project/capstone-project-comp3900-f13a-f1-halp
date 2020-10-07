from sqlalchemy import create_engine, MetaData, Table, Column, Integer, String, Date
from flask_login import UserMixin
from bankDetails import BankDetails

class User(UserMixin):
    
    def __init__(self,login_name, password, address, date_of_birth):
        self._login_name = login_name
        self._password = password
        self._address= address
        self._date_of_birth = date_of_birth
        self._bank_details = None

        self.id = login_name

def init_db():
    engine = create_engine('sqlite:///user.db', echo = True)
    meta = MetaData()
    users = Table(
        'users', meta, 
        Column('login_name', Integer, primary_key = True), 
        Column('password', String), 
        Column('address', String),
        Column('date_of_birth',Date),
        )
    meta.create_all(engine)
    return users

users=init_db()
    
