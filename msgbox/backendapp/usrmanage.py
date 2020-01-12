from flask import render_template, request, jsonify

from msgbox import login_required, db_session
from msgbox.backendapp import bn
from msgbox.models import User
from msgbox.utils.common import page_helper_getparam, page_helper_filter
from msgbox.utils.response_code import RET


@bn.route("/usrmanage", methods=['GET'])
@login_required
def gousrmanage():
    """请求用户管理页面"""
    render_obj = {"url": "usrmanage", "title": "用户管理"}  # 渲染的页面
    return render_template('msbox/usrmanage.html', render_obj=render_obj)


@bn.route("/usradd", methods=['GET', 'POST'])
@login_required
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
@login_required
def usrmodi():
    """修改用户信息"""
    usrid = request.args.get("usrid")
    u = User.query.filter(User.id == usrid).first()
    if u is None:
        return "对不起，你的访问异常"

    if request.method == "GET":
        render_obj = {"type": "modi", 'cur_usr': u.to_detail_dict()}
        return render_template('msbox/usrmanage-usr.html', render_obj=render_obj)
    else:
        workerid = request.form.get("workerid")
        usrname = request.form.get("usrname")
        depid = request.form.get("curdep_id")
        password = request.form.get("password")
        
        if not all([workerid, usrname, depid]):
            return jsonify(re_code=RET.PARAMERR, msg="提交用户参数有误")

        try:
            u.workerid = workerid
            u.real_name = usrname
            u.dep_id = depid
            if password is not None and password != '':
                u.password_hash = password
            db_session.commit()
            return jsonify(re_code=RET.OK, msg="修改用户成功")
        except Exception as e:
            return jsonify(re_code=RET.DBERR, msg="修改用户失败，请稍后重试")


@bn.route("/usrdel", methods=['POST'])
@login_required
def usrdel():
    """删除用户信息"""
    usrid = request.args.get("usrid")
    u = User.query.filter(User.id == usrid).first()
    if u is None:
        return jsonify(re_code=RET.NODATA, msg="用户不存在")
    try:
        db_session.delete(u)
        db_session.commit()
    except Exception as e:
        return jsonify(re_code=RET.PARAMERR, msg="删除失败")
    return jsonify(re_code=RET.OK, msg="删除成功!")


@bn.route("/modifypass", methods=['GET'])
@login_required
def gomodifypass():
    """请求修改密码页面"""
    render_obj = {"url": "modifypass", "title": "修改密码"}  # 渲染的页面
    return render_template('msbox/modifypass.html', render_obj=render_obj)


@bn.route("/filterusrinfo", methods=['GET', 'POST'])
@login_required
def filterusrinfo():
    """
    过滤查询用户的信息
    :return:
    """
    conditions = []  # 保留模糊查询的条件
    filterobj = page_helper_getparam(request)

    if filterobj is None:
        return jsonify(re_code=RET.PARAMERR, msg="参数不完整")
    filter_cond = filterobj['condition']

    if filter_cond.get('usrname', '') != '':
        conditions.append(User.real_name.like('%' + filter_cond['usrname'] + '%'))

    if filter_cond.get('workerid', '') != '':
        conditions.append(User.workerid.like('%' + filter_cond['workerid'] + '%'))

    if filter_cond.get('orgid', '') != '':
        conditions.append(User.dep_id == filter_cond['orgid'])

    # 剔除管理员
    conditions.append(User.usrrole != 'ADMIN')

    result = page_helper_filter(
        User.query.filter(*conditions),
        filterobj,
        lambda usrs: [v.to_dict() for v in usrs]
    )
    if result is None:
        return jsonify(re_code=RET.DBERR, msg="查询失败，请稍后重试")
    return jsonify(re_code=RET.OK, pagedInfo=result)
