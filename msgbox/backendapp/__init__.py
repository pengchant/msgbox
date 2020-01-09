from flask import Blueprint

bn = Blueprint('bn', __name__, url_prefix="/")

from . import orgmanage, auth, sysmanage, usrmanage
