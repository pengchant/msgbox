/**
 * 定义查询的条件
 * @type {{}}
 */
var queryParams = {
    page: 1,
    pagesize: 10,
    condition: {
        usrname: '',
        workerid: '',
        orgid: '',
    }
};

// 获取封装的查询方法
var query = $.pageQuery("/filterusrinfo", "page", "usrtbody", "tableTemp");

$(function () {
    // 初始化分页查询
    query(queryParams);

    // 点击查询按钮查询
    $("#filterquery").click(function () {
        usrname = $.trim($("#usrname").val()) // 用户名
        workerid = $.trim($("#workerid").val()) // 工号
        queryParams.condition.usrname = usrname
        queryParams.condition.workerid = workerid
        query(queryParams)
    });

    $("#btn_refreshusr").click(function () {
        location.reload();
    });


});