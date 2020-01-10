from flask import render_template, request, jsonify

from msgbox import login_required, db_session
from msgbox.backendapp import bn
from msgbox.models import User
from msgbox.utils.response_code import RET


@bn.route("/usrmanage", methods=['GET'])
@login_required
def gousrmanage():
    """请求用户管理页面"""
    render_obj = {"url": "usrmanage", "title": "用户管理"}  # 渲染的页面
    return render_template('msbox/usrmanage.html', render_obj=render_obj)


@bn.route("/usradd", methods=['GET', 'POST'])
def usradd():
    """添加用户"""
    if request.method == "GET":
        render_obj = {"type": "add"}
        return render_template('msbox/usrmanage-usr.html', render_obj=render_obj)
    else:
        workerid = request.form.get("workerid")
        usrname = request.form.get("usrname")
        password = request.form.get("password")
        depid = request.form.get("curdep_id")
        if not all([workerid, usrname, password, depid]):
            return jsonify(re_code=RET.PARAMERR, msg="提交用户参数有误")

        # 查询是否已经存在workerid
        stored_u = User.query.filter(User.workerid == workerid).first()
        if stored_u is not None:
            return jsonify(re_code=RET.PARAMERR, msg="该用户工号已被注册")

        u = User()
        u.workerid = workerid
        u.real_name = usrname
        u.password_hash = password
        u.dep_id = depid
        u.usrrole = "COMMON"
        try:
            db_session.add(u)
            db_session.commit()
            return jsonify(re_code=RET.OK, msg="添加用户成功")
        except Exception as e:
            pass
        return jsonify(re_code=RET.DBERR, msg="添加用户失败")


@bn.route("/usrmodi", methods=['GET', 'POST'])
def usrmodi():
    """修改用户信息"""
    if request.method == "GET":
        render_obj = {"type": "modi"}
        return render_template('msbox/usrmanage-usr.html', render_obj=render_obj)
    else:
        return jsonify(re_code=RET.OK, msg="添加用户成功")


@bn.route("/modifypass", methods=['GET'])
def gomodifypass():
    """请求修改密码页面"""
    render_obj = {"url": "modifypass", "title": "修改密码"}  # 渲染的页面
    return render_template('msbox/modifypass.html', render_obj=render_obj)
