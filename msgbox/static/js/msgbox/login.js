$(function () {
    $("#workerid").focus(function () {
        $("#workerid-err").hide();
    });
    $("#password").focus(function () {
        $("#password-err").hide();
    }).bind('keydown', function (event) {
        if (event.keyCode == "13") {
            $("#login").click();
        }
    });


    // 登录
    $("#login").click(function () {
        workerid = $("#workerid").val();
        password = $("#password").val();
        if (!workerid) {
            $("#workerid-err span").html("请输入工号");
            $("#workerid-err").show();
            return;
        }
        if (!password) {
            $("#password-err span").html("请填写密码");
            $("#password-err").show();
            return;
        }
        var params = {
            "workerid": workerid,
            "password": md5(password)
        };
        $.post("/login", params, function (data) {
            if (data && data.re_code == "0") {
                window.location.href = "/"; // 登录成功跳转到首页
            } else {
                swal(data.msg, {
                    icon: 'error',
                    button: false,
                    timer: 1200,
                })
            }
        });
    });
});