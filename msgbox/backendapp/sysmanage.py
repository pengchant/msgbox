"""接入系统管理"""
import uuid

from flask import render_template, request, jsonify

from msgbox import login_required, db_session, config, APP_ENV
from msgbox.backendapp import bn
from msgbox.models import ServiceSystem
from msgbox.utils.common import page_helper_getparam, page_helper_filter, generate_secrectkey
from msgbox.utils.response_code import RET


@bn.route("/sysmanage", methods=['GET'])
@login_required
def gosysmanage():
    """请求系统管理页面"""
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
        sysname = request.form.get("sysname")
        sysip = request.form.get("sysip")
        sysport = request.form.get('sysport')
        sysurl = request.form.get('sysurl')
        sysdesc = request.form.get('sysdesc')
        if not all([sysname, sysip, sysport, sysurl, sysdesc]):
            return jsonify(re_code=RET.PARAMERR, msg="参数不完整")
        try:
            newsys = ServiceSystem(
                sysname=sysname, sysip=sysip, sysport=sysport, sysurl=sysurl, sysdescription=sysdesc)
            newsys.status = "CLOSED"  # 默认关闭
            # 生成appkey和appsecrect
            newsys.appkey = str(uuid.uuid4())
            newsys.appsecrect = generate_secrectkey(newsys.appkey, config[APP_ENV].SECRET_KEY)  # appsecrect
            db_session.add(newsys)
            db_session.commit()
            return jsonify(re_code=RET.OK, msg="添加系统成功")
        except Exception as e:
            return jsonify(re_code=RET.DBERR, msg="添加系统失败，请稍后重试!")


@bn.route("/filtersys", methods=['GET', 'POST'])
@login_required
def filtersys():
    """过滤查询系统"""
    conditions = []  # 保留模糊查询的条件
    filterobj = page_helper_getparam(request)

    if filterobj is None:
        return jsonify(re_code=RET.PARAMERR, msg="参数不完整")
    filter_cond = filterobj['condition']

    if filter_cond.get('status', '') != '':
        conditions.append(ServiceSystem.status == filter_cond['status'])

    if filter_cond.get('sysname', '') != '':
        conditions.append(ServiceSystem.sysname.like('%' + filter_cond['sysname'] + '%'))

    result = page_helper_filter(
        ServiceSystem.query.filter(*conditions),
        filterobj,
        lambda sysinfo: [v.to_dict() for v in sysinfo]
    )
    if result is None:
        return jsonify(re_code=RET.DBERR, msg="查询失败，请稍后重试")
    return jsonify(re_code=RET.OK, pagedInfo=result)


@bn.route("/getappkey", methods=['GET', 'POST'])
@login_required
def getappkey():
    """
    获取appkey和appsecrect
    :return:
    """
    id = request.args.get("sysid")
    if id is None:
        return jsonify(re_code=RET.PARAMERR, msg="获取appkey和appsecrect失败")
    sys = ServiceSystem.query.filter(ServiceSystem.id == id).first()
    if sys is None:
        return jsonify(re_code=RET.PARAMERR, msg="不存在该系统")
    appkey = {
        "appkey": sys.appkey,
        "apptoken": sys.appsecrect
    }
    return render_template('msbox/sysappkey.html', appkey=appkey)


@bn.route("/removesys", methods=['POST'])
@login_required
def removesys():
    """删除系统"""
    sysid = request.args.get("sysid")
    if sysid is None:
        return jsonify(re_code=RET.PARAMERR, msg="获取appkey和appsecrect失败")
    sys = ServiceSystem.query.filter(ServiceSystem.id == sysid).first()
    if sys is None:
        return jsonify(re_code=RET.PARAMERR, msg="不存在该系统")

    if sys.status == "OPENING":
        return jsonify(re_code=RET.PARAMERR, msg="已运行的系统不能删除")

    try:
        db_session.delete(sys)
        db_session.commit()
    except Exception as e:
        return jsonify(re_code=RET.DBERR, msg="删除系统失败")
    return jsonify(re_code=RET.OK, msg="删除成功")


@bn.route("/modisys", methods=['GET', 'POST'])
@login_required
def modisys():
    """修改系统信息"""
    sysid = request.args.get("sysid")
    sys = ServiceSystem.query.filter(ServiceSystem.id == sysid).first()
    if sys is None:
        return jsonify(re_code=RET.PARAMERR, msg="不存在该系统")

    if sysid is None:
        return jsonify(re_code=RET.PARAMERR, msg="获取appkey和appsecrect失败")

    if request.method == 'GET':
        render_obj = {"type": "modi", "cursys": sys}
        return render_template("msbox/sysmanage-sys.html", render_obj=render_obj)
    else:
        sysname = request.form.get("sysname")
        sysip = request.form.get("sysip")
        sysport = request.form.get('sysport')
        sysurl = request.form.get('sysurl')
        sysdesc = request.form.get('sysdesc')
        if not all([sysname, sysip, sysport, sysurl, sysdesc]):
            return jsonify(re_code=RET.PARAMERR, msg="参数不完整")
        try:
            sys.sysname = sysname
            sys.sysip = sysip
            sys.sysport = sysport
            sys.sysurl = sysurl
            sys.sysdesc = sysdesc
            sys.appkey = str(uuid.uuid4())
            sys.appsecrect = generate_secrectkey(sys.appkey, config[APP_ENV].SECRET_KEY)  # appsecrect
            db_session.commit()

            return jsonify(re_code=RET.OK, msg="修改系统成功,appkey和appsecrect已被重置!")
        except Exception as e:
            return jsonify(re_code=RET.DBERR, msg="修改系统失败，请稍后重试!")


@bn.route("/startsys", methods=['GET', 'POST'])
@login_required
def startsys():
    """开启系统"""
    sysid = request.args.get("sysid")
    sys = ServiceSystem.query.filter(ServiceSystem.id == sysid).first()
    if sys is None:
        return jsonify(re_code=RET.PARAMERR, msg="不存在该系统")

    try:
        sys.status = "OPENING"
        db_session.commit()
        return jsonify(re_code=RET.OK, msg="开启系统成功")
    except Exception as e:
        return jsonify(re_code=RET.DBERR, msg="开启系统失败")


@bn.route("/stopsys", methods=['GET', 'POST'])
@login_required
def stopsys():
    """关闭系统"""
    sysid = request.args.get("sysid")
    sys = ServiceSystem.query.filter(ServiceSystem.id == sysid).first()
    if sys is None:
        return jsonify(re_code=RET.PARAMERR, msg="不存在该系统")

    try:
        sys.status = "CLOSED"
        db_session.commit()
        return jsonify(re_code=RET.OK, msg="关闭系统成功")
    except Exception as e:
        return jsonify(re_code=RET.DBERR, msg="关闭系统失败")
