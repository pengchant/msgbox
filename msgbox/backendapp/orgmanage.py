from flask import request, jsonify
from sqlalchemy import exists

from msgbox import db_session, login_required
from msgbox.backendapp import bn
from msgbox.models import Organization
from msgbox.utils.response_code import RET


@bn.route("/allorg", methods=['GET', 'POST'])
@login_required
def getallorg():
    """获取所有的组织"""
    orgs = db_session.query(Organization).filter(Organization.pid >= 0).all()
    result = [v.to_dict() for v in orgs]
    return jsonify(re_code=RET.OK, data=result, msg="请求组织成功")


@bn.route("/addorg", methods=['POST'])
@login_required
def addorg():
    """新增组织:
    0.校验请求参数
    1.添加组织
    3.返回相应结果
    """
    depname = request.form.get('orgname')
    pid = request.form.get('pid')
    # 校验数据
    if not all([depname, pid]):
        return jsonify(re_code=RET.PARAMERR, msg="传递参数有误")

    # 判断父节点是否存在
    exit = True
    if pid != '0':
        exit = db_session.query(exists().where(Organization.id == pid)).scalar()

    if exit:
        newOrg = Organization(depname=depname, pid=pid)
        try:
            db_session.add(newOrg)
            db_session.commit()
            # 查询新的组织结构
            orgs = db_session.query(Organization).filter(Organization.pid >= 0).all()
            result = [v.to_dict() for v in orgs]
            return jsonify(re_code=RET.OK, msg="新增组织成功", data=result)
        except Exception as e:
            return jsonify(re_code=RET.DBERR, msg="保存组织失败")
    else:
        return jsonify(re_code=RET.PARAMERR, msg="父节点不存在")


@bn.route("/modiorg", methods=['POST'])
@login_required
def modiorg():
    """修改组织名称"""
    id = request.form.get("id")
    orgname = request.form.get("orgname")
    if not all([id, orgname]):
        return jsonify(re_code=RET.PARAMERR, msg="参数有误")
    else:
        try:
            org = Organization.query.filter(Organization.id == id).first()
            org.depname = orgname
            db_session.commit()
            # 查询新的组织结构
            orgs = db_session.query(Organization).filter(Organization.pid >= 0).all()
            result = [v.to_dict() for v in orgs]
            return jsonify(re_code=RET.OK, msg="修改组织成功", data=result)
        except Exception as e:
            return jsonify(re_code=RET.DBERR, msg="更新组织失败")


@bn.route("/delorg", methods=["POST"])
@login_required
def delorg():
    """删除组织"""
    id = request.args.get("orgid")
    if id is None:
        return jsonify(re_code=RET.PARAMERR, msg="组织编号有误")

    try:
        Organization.query.filter(Organization.id == id).delete()
        db_session.commit()
        # 查询新的组织结构
        orgs = db_session.query(Organization).filter(Organization.pid >= 0).all()
        result = [v.to_dict() for v in orgs]
        return jsonify(re_code=RET.OK, msg="删除组织成功", data=result)
    except Exception as e:
        return jsonify(re_code=RET.DBERR, msg="删除组织失败，请检查该组织下是否有用户")
