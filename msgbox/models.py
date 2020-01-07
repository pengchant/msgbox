'''消息盒子模型'''
from sqlalchemy import Column, Integer, String

from msgbox.db import Base


class User(Base):
    '''测试用户模型'''
    __tablename__ = 'users'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50), unique=True)
    email = Column(String(100), unique=True)

    def __init__(self, name, email):
        self.name = name
        self.email = email

    def __repr__(self):
        return '<User %r> ' % (self.name)
