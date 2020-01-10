from flask import render_template

from msgbox import login_required
from msgbox.backendapp import bn


@bn.route("/usrmanage", methods=['GET'])
@login_required
def gousrmanage():
    """请求用户管理页面"""
    render_obj = {"url": "usrmanage", "title": "用户管理"}  # 渲染的页面
    return render_template('msbox/usrmanage.html', render_obj=render_obj)



@bn.route("/modifypass", methods=['GET'])
def gomodifypass():
    """请求修改密码页面"""
    render_obj = {"url": "modifypass", "title": "修改密码"}  # 渲染的页面
    return render_template('msbox/modifypass.html', render_obj=render_obj)
