$(function () {

    // 添加系统
    $("#btn_createsys").click(function () {
        if (valie_all_input() > 0) {
            return;
        }
        sysobj = $("#sysform").serializeObject();
        $.post('/systemadd', sysobj, function (result) {
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

    // 修改系统
    $("#btn_updatesys").click(function () {
        if (valie_all_input() > 0) {
            return;
        }
        sysobj = $("#sysform").serializeObject();
        $.post('/modisys?sysid=' + cur_sysid, sysobj, function (result) {
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