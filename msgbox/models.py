'''消息盒子模型'''
from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, ForeignKey, DateTime, Table
from sqlalchemy.orm import relationship

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


class Category(Base):
    """文章的类别"""
    __tablename__ = 'category'

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))

    def __init__(self, name):
        self.name = name


class Post(Base):
    """文章"""
    __tablename__ = "post"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(80))
    body = Column(Text)
    pub_date = Column(DateTime, default=datetime.utcnow())
    category_id = Column(Integer, ForeignKey('category.id'))
    category = relationship('Category', backref='posts', lazy='dynamic')

    def __init__(self, title, body, category, pub_date=None):
        self.title = title
        self.body = body
        self.category = category
        if pub_date is None:
            pub_date = datetime.utcnow()
        self.pub_date = pub_date


# 一对多的关系 Person -> (address1, address2, address3, ...)
class Address(Base):
    """地址(多)"""
    __tablename__ = 'address'
    id = Column(Integer, primary_key=True, autoincrement=True)
    email = Column(String(50))
    person_id = Column(Integer, ForeignKey('person.id'))


class Person(Base):
    """人实体类(一)"""
    __tablename__ = "person"
    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(50))
    addresses = relationship('Address', backref="person", lazy="dynamic")


# 多对多的关系 假设 Page 与 Tag 是多对多的关系
class Tag(Base):
    __tablename__ = "tag"
    id = Column(Integer, primary_key=True, autoincrement=True)


tags = Table('tags',
             Base.metadata,
             Column('tag_id', Integer, ForeignKey('tag.id')),
             Column('page_id', Integer, ForeignKey('page.id')))


class Page(Base):
    __tablename__ = "page"
    id = Column(Integer, primary_key=True, autoincrement=True)
    tags = relationship('Tag', secondary=tags)
