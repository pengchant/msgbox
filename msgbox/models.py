"""cssrc消息盒子建模"""
from datetime import datetime

from sqlalchemy import Column, Integer, String, Text, Enum, DateTime, ForeignKey
from sqlalchemy.orm import relationship, backref
from werkzeug.security import generate_password_hash, check_password_hash

from msgbox.db import Base


class BaseModel(object):
    """模型基类"""
    create_time = Column(DateTime, default=datetime.utcnow())  # 记录模型的创建时间
    update_time = Column(DateTime, default=datetime.now(), onupdate=datetime.now())  # 记录模型更新时间


class Organization(Base, BaseModel):
    """系统部门组织结构"""
    __tablename__ = "msgbox_originzation"

    id = Column(Integer, primary_key=True, autoincrement=True)
    depname = Column(String(255), nullable=False)  # 系统部门的名称
    pid = Column(Integer, default=None)  # 父节点编号
    users = relationship('User', backref='msgbox_originzation', lazy='dynamic')  # 该部门下的所有的用户


class ServiceSystem(Base, BaseModel):
    """服务系统"""
    __tablename__ = "msgbox_servicesystem"

    id = Column(Integer, primary_key=True, autoincrement=True)
    sysname = Column(String(255), nullable=False)  # 系统名称
    sysdescription = Column(Text)  # 系统描述
    sysip = Column(String(100))  # 系统ip地址
    sysport = Column(String(100))  # 系统端口
    sysurl = Column(String(255))  # 系统url
    appkey = Column(String(255), unique=True)  # app的key
    appsecrect = Column(String(255), unique=True)  # app的秘钥
    status = Column(
        Enum(
            "CLOSED",  # 已关闭
            "OPENING",  # 已开启
        ),
        default="CLOSED", index=True
    )
    pushed_msglist = relationship("SystemMessage", backref="msgbox_servicesystem", lazy="dynamic")  # 某系统下所有推送的消息


class User(Base, BaseModel):
    """用户实体类"""
    __tablename__ = "msgbox_userinfo"

    id = Column(Integer, primary_key=True, autoincrement=True)
    real_name = Column(String(32))  # 用户名
    workerid = Column(String(30), unique=True)  # 工号
    password = Column(String(255), nullable=False)  # 加密的密码
    phone_num = Column(String(100))  # 手机号(预留)
    avatar_url = Column(String(255))  # 用户头像(预留)
    dep_id = Column(Integer, ForeignKey('msgbox_originzation.id'), nullable=False)  # 所在部门的编号
    status = Column(  # 性别(备用)
        Enum(
            "MAILE",  # 男
            "FEMAILE",  # 女
        ),
        default="MAILE", index=True
    )

    pushed_msglist = relationship("SystemMessage", backref="msgbox_userinfo", lazy="dynamic")  # 当前用户下的所有的消息

    @property
    def password_hash(self):
        raise AttributeError(u'不能访问该属性')

    @password_hash.setter
    def password_hash(self, value):
        self.password = generate_password_hash(value)

    def check_password(self, password):
        """校验密码的正确性"""
        return check_password_hash(self.password, password)


class SystemMessage(Base, BaseModel):
    """系统推送的消息"""
    __tablename__ = "msgbox_sysmessage"

    id = Column(Integer, primary_key=True, autoincrement=True)
    msg_title = Column(String(255), nullable=False)  # 消息的标题
    from_sys_id = Column(Integer, ForeignKey('msgbox_servicesystem.id'), nullable=False)  # 消息所属的系统编号
    to_usr_id = Column(Integer, ForeignKey("msgbox_userinfo.id"), nullable=False)  # 推送的用户对象编号
    msg_push_time = Column(DateTime, default=datetime.utcnow())  # 推送消息的时间
    msg_read_time = Column(DateTime, default=datetime.utcnow())  # 推送给用户消息查看的时间
    msg_url = Column(String(255), nullable=False)  # 消息浏览器打开的路径
    msg_status = Column(  # 消息的状态
        Enum(
            "WAITTING_SEND",  # 待发送
            "WAITTING_READ",  # 已发送，待阅读
            "HAVE_READED",  # 已阅读
        ),
        default="WAITTING_SEND", index=True
    )
