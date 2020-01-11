/**
 * 将表单序列化为json对象
 * @returns {{}}
 */
$.fn.serializeObject = function () {
    var o = {};
    var a = this.serializeArray();
    $.each(a, function () {
        if (o[this.name]) {
            if (!o[this.name].push) {
                o[this.name] = [o[this.name]];
            }
            o[this.name].push(this.value || '');
        } else {
            o[this.name] = this.value || '';
        }
    });
    return o;
};

$.extend({
    /**
     * 延时关闭layui自身
     */
    lay_close_self: function () {
        setTimeout(function () {
            parent.location.reload(true);//刷新父级页面
            var index = parent.layer.getFrameIndex(window.name);
            parent.layer.close(index);
        }, 1100)
    },

    /**
     * 及时关闭模态框
     */
    lay_close_rightnow: function () {
        var index = parent.layer.getFrameIndex(window.name);
        parent.layer.close(index);
    },

    /**
     * 渲染数据
     * @param containerid   容器id
     * @param templateid    模板的编号
     * @param data          数据list
     */
    renderData: function (containerid, templateid, data) {
        $("#" + containerid).html(template(templateid, {item: data}))
    },


    /**
     * 渲染分页
     * @param pageCurrent   当前页号
     * @param pageSum       总的页面数
     * @param callback      点击回调函数
     * @param queryObj      查询的对象:{}
     * @param pagekey:str   查询对象页号的key
     */
    renderPager: function (pageCurrent, pageSum, callback, queryObj, pagekey) {
        $(".pagination").bootstrapPaginator({
            bootstrapMajorVersion: 3,
            currentPage: pageCurrent,
            totalPages: pageSum == 0 ? 1 : pageSum,
            alignment: "center",
            numberOfPages: 6,
            // shouldShowPage: true,
            itemTexts: function (type, page, current) {
                switch (type) {
                    case "first":
                        return "首页";
                    case "prev":
                        return "上一页";
                    case "next":
                        return "下一页";
                    case "last":
                        return "末页";
                    case "page":
                        return page;
                }
            },
            onPageClicked: function (event, originalEvent, type, page) {
                queryObj[pagekey] = page;
                callback && callback(queryObj)
            }
        })
    },

    /**
     * 分页查询闭包
     * @param url           后台访问接口
     * @param pagekey       page的键名
     * @param containerid   容器的编号
     * @param templateid    模板的编号
     * @returns {doquery}   返回查询的方法
     */
    pageQuery: function (url, pagekey, containerid, templateid) {
        doquery = function (queryparams) {
            $.ajax({
                url: url,
                type: 'post',
                dataType: 'json',
                async: false,
                contentType: 'application/json; charset=utf-8',
                data: JSON.stringify(queryparams),
                success: function (result) {
                    if (result.re_code == "0") {
                        // 渲染数据
                        $.renderData(containerid, templateid, result.pagedInfo)
                        // 渲染pager
                        $.renderPager(result.pagedInfo.page, result.pagedInfo.pages, doquery, queryparams, pagekey)
                    } else {
                        swal(result.msg, {
                            icon: 'error',
                            button: false,
                            timer: 1200,
                        })
                    }
                }
            });
        };
        return doquery;
    }


});

// 验证所有表单
function valie_all_input() {
    var errs = 0;
    $(".valie-input").each(function () {
        curval = $(this).val();
        if (!curval) {
            $("#" + $(this).attr("name") + "-err span").html($(this).attr("placeholder"));
            $("#" + $(this).attr("name") + "-err").show();
            errs++;
        }
    });
    return errs;
}


$(function () {
    // 当获取焦点时
    $(".valie-input").focus(function () {
        curname = $(this).attr("name");
        $("#" + curname + "-err").hide();
    });

    // 关闭模态框
    $("[data-lay-close=true]").click(function () {
        console.log("关闭模态框");
        $.lay_close_rightnow()
    });
});