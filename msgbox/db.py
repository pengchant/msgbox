import logging

import click
from flask.cli import with_appcontext
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine, MetaData
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from msgbox import config

convention = {
    "ix": 'ix_%(column_0_label)s',
    "uq": "uq_%(table_name)s_%(column_0_name)s",
    "ck": "ck_%(table_name)s_%(constraint_name)s",
    "fk": "fk_%(table_name)s_%(column_0_name)s_%(referred_table_name)s",
    "pk": "pk_%(table_name)s"
}

engine = create_engine(config.config[config.APP_ENV].SQLALCHEMY_DATABASE_URI)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

metadata = MetaData(naming_convention=convention)
db = SQLAlchemy(metadata=metadata)

Base = declarative_base()
Base.query = db_session.query_property()


def init_app(app):
    '''初始化app'''
    global db
    db.init_app(app)
    app.cli.add_command(init_db_command)
    # init_db()  # 初始化数据库


def init_db():
    '''初始化数据库'''
    import msgbox.models
    Base.metadata.create_all(bind=engine)
    logging.info("数据库初始化完毕...")


@click.command("init-db")
@with_appcontext
def init_db_command():
    """建立数据库表格"""
    init_db()
    click.echo("初始化数据库完毕....")
