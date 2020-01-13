$(function () {

    // 修改密码
    $("#btn_modifypass").click(function () {
        if (valie_all_input() > 0) {
            return;
        }
        pwdobj = $("#changepwdform").serializeObject()
        pwdobj["oripass"] = md5(pwdobj["oripass"])
        pwdobj["newpass"] = md5(pwdobj["newpass"])
        pwdobj["surepass"] = md5(pwdobj["surepass"])
        $.post("/changepwd", pwdobj, function (result) {
            if (result && result.re_code == "0") {
                // 弹出消息框
                swal(result.msg, {
                    button: false,
                    timer: 1200,
                    icon: 'success'
                });
                // 延时关闭，并重新登录
                setTimeout(function () {
                    location.href = "/login"
                }, 1100)
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