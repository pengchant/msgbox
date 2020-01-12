// ztree的配置
var setting = {
    view: {
        dblClickExpand: false
    },
    data: {
        simpleData: {
            enable: true
        }
    },
    callback: {
        onClick: onClick // 点击事件的回调
    }
};
// ztree的节点
var zNodes = [];

/**
 * 抓取组织结构数据
 * @param handler 抓取数据后的回调函数,可以为NULL
 */
function fetchOrg(handler) {
    $.ajax({
        url: '/allorg',
        type: 'post',
        dataType: 'json',
        async: false,
        contentType: 'application/json; charset=utf-8',
        success: function (result) {
            if (result.re_code == "0") {
                zNodes = result.data
                if (handler && handler instanceof Function) {
                    handler()
                }
            } else {
                swal("请求加载组织失败，请稍后重试", {
                    buttons: false,
                    timer: 1200
                })
            }
        }
    })
}


// 点击之后的时间回调
function onClick(e, treeId, treeNode) {
    var zTree = $.fn.zTree.getZTreeObj("treeDemo"),
        nodes = zTree.getSelectedNodes();
    id = nodes[0].id
    depname = nodes[0].name
    $("#curdep_name").text(depname)
    $("#curdep_id").val(id)
    // 取消错误验证
    $("#curdep_id-err").hide();

}


$(function () {
    fetchOrg();
    $.fn.zTree.init($("#treeDemo"), setting, zNodes);

    // 如果是修改用户,设置选中
    if (modi_type == 'modi' && cur_depid) {
        // 设置默认选中
        zTree_Menu = $.fn.zTree.getZTreeObj("treeDemo");
        var node = zTree_Menu.getNodeByParam("id", cur_depid);
        zTree_Menu.selectNode(node, true);//指定选中ID的节点
        zTree_Menu.expandNode(node, true, false);//指定选中ID节点展开
    }

    // 当获取焦点时
    $("input.vali-input").focus(function () {
        curname = $(this).attr("name");
        $("#" + curname + "-err").hide();
    });

    // 验证所有表单
    function vali_all() {
        var errs = 0;
        $("input.vali-input").each(function () {
            // 如果是修改状态，则忽略password的校验
            if (modi_type == 'modi' && $(this).attr("type") == "password") {
                return true
            }
            curval = $(this).val();
            if (!curval) {
                $("#" + $(this).attr("name") + "-err span").html($(this).attr("placeholder"));
                $("#" + $(this).attr("name") + "-err").show();
                errs++;
            }
        });
        return errs;
    }


    // 提交用户
    $("#btn_createusr").click(function () {
        if (vali_all() > 0) {
            return;
        }
        usrobj = $("#usrform").serializeObject();
        usrobj['password'] = md5(usrobj['password'])
        $.post("/usradd", usrobj, function (result) {
            console.log(result);
            if (result && result.re_code == "0") {
                // 弹出消息框
                swal(result.msg, {
                    button: false,
                    timer: 1200,
                    icon: 'success'
                });
                // 延时关闭
                $.lay_close_self()
            } else {
                swal(result.msg, {
                    icon: 'error',
                    button: false,
                    timer: 1200
                })
            }
        })
    });

    // 点击取消，关闭模态框
    $("#btn_cancelusr").click(function () {
        console.log("关闭模态框")
        $.lay_close_rightnow()
    });


    // 修改用户信息
    $("#btn_updateusr").click(function () {
        if (vali_all() > 0) {
            return;
        }
        usrobj = $("#usrform").serializeObject();
        if ($.trim(usrobj['password'])) {
            usrobj['password'] = md5($.trim(usrobj['password']))
        }
        $.post("/usrmodi?usrid=" + cur_usrid, usrobj, function (result) {
            console.log(result);
            if (result && result.re_code == "0") {
                // 弹出消息框
                swal(result.msg, {
                    button: false,
                    timer: 1200,
                    icon: 'success'
                });
                // 延时关闭
                $.lay_close_self()
            } else {
                swal(result.msg, {
                    icon: 'error',
                    button: false,
                    timer: 1200
                })
            }
        })
    });
});
