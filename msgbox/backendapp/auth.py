"""后端应用通行证"""
from flask import render_template, url_for, request

from msgbox.backendapp import bn
from msgbox.utils.common import login_required


@bn.route("/login", methods=['GET', 'POST'])
def login():
    """用户登录"""
    if request.method == 'GET':
        return render_template('auth/login.html')
