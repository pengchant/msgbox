$(function () {
    // 点击退出登录
    $("#msgbox_exit").click(function () {
        swal({
            icon: "info",
            text: "确定要退出登录吗？",
            closeOnClickOutside: false, // 是否在其他地方点击关闭
            buttons: {
                cancel: {
                    text: "取消",
                    visible: true,
                    className: 'btn',
                    closeModal: true,
                },
                confirm: {
                    text: "确定",
                    className: 'btn btn-primary',
                    closeModal: true,
                }
            }
        }).then(function (result) {
            if (result) {
                // 请求退出登录
                $.get("/logout", function (data) {
                    if (data.re_code == "0") {
                        window.location.href = "/login"
                    } else {
                        swal("退出失败，请稍后重试", {
                            button: false,
                            timer: 1200
                        })
                    }
                })
            }
        });
    });
});