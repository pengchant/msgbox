"""接入系统管理"""
from flask import render_template, request

from msgbox import login_required
from msgbox.backendapp import bn


@bn.route("/sysmanage", methods=['GET'])
def gosysmanage():
    """请求用户管理页面"""
    render_obj = {"url": "sysmanage", "title": "接入系统管理"}  # 渲染的页面
    return render_template('msbox/sysmanage.html', render_obj=render_obj)


@bn.route("/systemadd", methods=['GET', 'POST'])
@login_required
def systemadd():
    """添加接入系统"""
    if request.method == "GET":
        render_obj = {"type": "add"}
        return render_template('msbox/sysmanage-sys.html', render_obj=render_obj)
    else:
        pass
