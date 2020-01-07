import click
from flask.cli import with_appcontext
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import scoped_session, sessionmaker

from msgbox import config

engine = create_engine(config.config[config.APP_ENV].SQLALCHEMY_DATABASE_URI)
db_session = scoped_session(sessionmaker(autocommit=False, autoflush=False, bind=engine))

Base = declarative_base()
Base.query = db_session.query_property()


def init_app(app):
    '''初始化app'''
    # app.teardown_appcontext(db_session.remove)
    app.cli.add_command(init_db_command)
    return db_session


def init_db():
    '''初始化数据库'''
    import msgbox.models
    Base.metadata.create_all(bind=engine)


@click.command("init-db")
@with_appcontext
def init_db_command():
    '''建立数据库表格'''
    init_db()
    click.echo("初始化数据库完毕....")
