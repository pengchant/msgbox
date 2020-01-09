"""接入系统管理"""
from flask import render_template

from msgbox.backendapp import bn


@bn.route("/sysmanage", methods=['GET'])
def gosysmanage():
    """请求用户管理页面"""
    render_obj = {"url": "sysmanage", "title": "接入系统管理"}  # 渲染的页面
    return render_template('msbox/sysmanage.html', render_obj=render_obj)
