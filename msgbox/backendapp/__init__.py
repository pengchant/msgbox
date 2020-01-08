from flask import Blueprint

bn = Blueprint('bn', __name__)

from . import orgmanage, password, sysmanage, usrmanage
